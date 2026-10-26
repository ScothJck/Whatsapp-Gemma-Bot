import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

load_dotenv()

INSTRUCCIONES_ASISTENTE = """
    Eres un asistente de Whatsapp amable, conciso y con toque amigable y casual.
    Reglas principales:
    1. Responde de forma breve y natural, adaptándote al formato de chat de WhatsApp.
    2. Si te preguntan algo sobre horarios, precios o información que NO conoces en tu contexto, NO inventes nada.
    3. generalmente soy una persona un poquito reservada asi que adaptate aello.
    4. ademas no digas en que puedo ayudarte por que pareces un asistente y basicamente yo a esta persona la conosco de confianza asi que tienes que sonar mas humano ok
    5. Si no sabes la respuesta o el usuario solicita hablar directamente con el dueño, responde exactamente:
    "REGISTRAR_NOTIFICACION: No tengo esa información, le avisaré a Scoth para que te responda directamente."
"""

# Inicializa el cliente moderno
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ContestarMensajeWhatsApp(mensaje_cliente):
    """Función con bucle de reintento y pausa de 20s ante errores 500"""

    respondido = False

    while not respondido:
        try:
            response = client.models.generate_content(
                model="gemma-4-26b-a4b-it",
                contents=mensaje_cliente,
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCCIONES_ASISTENTE,
                ),
            )

            texto_respuesta = response.text

        
            if "REGISTRAR_NOTIFICACION" in texto_respuesta:
                # Aquí puedes agregar la lógica para registrar la notificación o enviar un mensaje al dueño
                print("Notificación registrada para Scoth.")
                respondido = True

                return "REGISTRAR_NOTIFICACION: No tengo esa información, le avisaré a Scoth para que te responda directamente."
            else:
                print(f"Respuesta del asistente: {texto_respuesta}")
                respondido = True

                return texto_respuesta

        except Exception as e:
            print(f"Error al procesar la respuesta: {e}")
            print("Reintentando en 20 segundos...")
            time.sleep(20)  # Espera 20 segundos antes de reintentar
            