from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel
import os
from dotenv import load_dotenv
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


@app.get("/webhook")
def VerificarWebHook(
    mode : str = Query(None, alias="hub_mode"),
    token : str = Query(None, alias="hub.verify_token"),
    challenge : str = Query(None, alias="hub.challenge")
):
    if(mode == "subscribe" and token == VERIFY_TOKEN):
        return Response(content=challenge, media_type="text/plane")

    raise HTTPException(status_code=403, detail="Verificacion Falid.")



@app.post("/webhook")
def RecibirMensajeWhatsApp(data: MensajeWhatsApp):
    """Recibe un mensaje de WhatsApp y devuelve la respuesta del asistente"""

    print(f"\n[Nuevo mensaje de {data.sender}]: {data.message}")

    respuesta_ia = ContestarMensajeWhatsApp(data.message)

    return {"status" : "success", "respuesta": respuesta_ia}
