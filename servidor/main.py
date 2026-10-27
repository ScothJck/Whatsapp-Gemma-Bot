from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

from .contestar_whatsapp import ContestarMensajeWhatsApp


# Creamos el punto de entrada de la API
app = FastAPI(title="Whatsapp Gema Bot", version="1.0")


# creamos la estructura de datos para recibir el mensaje de WhatsApp
class MensajeWhatsApp(BaseModel):
    message: str
    sender: str


@app.get("/")
def Home():
    return {"status": "¡El bot de FastAPI con Gemma está activo y listo! 🚀"}

@app.post("/webhook")
def RecibirMensajeWhatsApp(data: MensajeWhatsApp):
    """Recibe un mensaje de WhatsApp y devuelve la respuesta del asistente"""

    print(f"\n[Nuevo mensaje de {data.sender}]: {data.message}")

    respuesta_ia = ContestarMensajeWhatsApp(data.message)

    return {"status" : "success", "respuesta": respuesta_ia}
