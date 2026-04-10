import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Cargar variables ocultas
load_dotenv()
client = Anthropic()

# Función para leer el cerebro del agente
def leer_contexto():
    try:
        with open("agents.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Eres un asistente de programación."

def probar_agente():
    print("Iniciando Agente de Desarrollo Local...\n")
    
    # 1. Cargamos tu archivo de reglas
    reglas_del_agente = leer_contexto()
    
    # 2. Simulamos que le pasas un cambio en el código
    cambio_simulado = "He creado el archivo login.py y he añadido la función para validar contraseñas de usuarios."
    
    print(f"Usuario: {cambio_simulado}")
    print("Agente pensando...\n")
    
    # 3. Llamada al modelo inyectando el cerebro
    respuesta = client.messages.create(
        model="claude-sonnet-4-6", # El modelo que detectamos que funciona en tu cuenta
        max_tokens=300,
        system=reglas_del_agente,  # AQUÍ LE INYECTAMOS TU ARCHIVO agents.md
        messages=[
            {"role": "user", "content": f"Basado en tus reglas, redacta el comando exacto de git commit para este cambio: {cambio_simulado}"}
        ]
    )
    
    print("=== RESPUESTA DEL AGENTE ===")
    print(respuesta.content[0].text)

if __name__ == "__main__":
    probar_agente()