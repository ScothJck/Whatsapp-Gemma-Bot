from fastapi import FastAPI, HTTPException, Query, Response, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import httpx
from .contestar_whatsapp import ContestarMensajeWhatsApp


# Cargamos las vaariables de entorno
load_dotenv()

# Creamos el punto de entrada de la API
app = FastAPI(title="Whatsapp Gema Bot", version="1.0")

# Definimos la variable o leemos la variable
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")


# creamos la estructura de datos para recibir el mensaje de WhatsApp
class MensajeWhatsApp(BaseModel):
    message: str
    sender: str


@app.get("/")
def Home():
    return {"status": "¡El bot de FastAPI con Gemma está activo y listo! 🚀"}


@app.get("/conection/webhook")
def VerificarWebHook(
    mode : str = Query(None, alias="hub_mode"),
    token : str = Query(None, alias="hub.verify_token"),
    challenge : str = Query(None, alias="hub.challenge")
):
    if(mode == "subscribe" and token == VERIFY_TOKEN):
        return Response(content=challenge, media_type="text/plane")

    raise HTTPException(status_code=403, detail="Verificacion Falid.")



@app.post("/webhook")
async def RecibirMensajeWhatsApp(request: Request):
    """Recibe un mensaje de WhatsApp y devuelve la respuesta del asistente"""

    body = await request.json()

    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})

        if("messages" in value):
            mensaje_obj = value["messages"][0]
            remitente = mensaje_obj.get("from")
            texto_mensaje = mensaje_obj.get("text", {}).get("body")

            print(f"\n[MENSAJE REAL DE WHATSAPP] De: {remitente} | Texto: {texto_mensaje}")

        respuesta_ia = ContestarMensajeWhatsApp(texto_mensaje)

        print("Respuesta IA: ", respuesta_ia)

        WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
        PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

        url_meta = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"

        headers = {
            "Authorization" : f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": remitente,
            "type": "text",
            "text": {"body": respuesta_ia}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url_meta, json=payload, headers=headers)
            print("Respuesta enviada a Meta:", response.json())
        

    except Exception as e:
        print("Error Procesando el Webhook, ", e)


    return {"status" : "success"}
