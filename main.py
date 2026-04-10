import os
import subprocess
from dotenv import load_dotenv
from anthropic import Anthropic

# Cargar variables ocultas
load_dotenv()
client = Anthropic()

# 1. El Cerebro (Memoria)
def leer_contexto():
    try:
        with open("agents.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Eres un asistente de programación."

# 2. LA NUEVA HABILIDAD: Leer la realidad de tu ordenador
def obtener_git_status():
    try:
        # Esto ejecuta 'git status' en tu terminal y guarda el texto que devuelve
        resultado = subprocess.run(['git', 'status'], capture_output=True, text=True, check=True)
        return resultado.stdout
    except Exception as e:
        return f"Error leyendo git status: {e}"

def probar_agente():
    print("Iniciando Agente de Desarrollo Local...\n")
    
    reglas_del_agente = leer_contexto()
    
    print("👀 El agente está leyendo tu 'git status' real...")
    estado_git = obtener_git_status()
    
    print("🧠 Agente pensando...\n")
    
    # 3. Le pasamos la realidad al modelo, no una simulación
    respuesta = client.messages.create(
        model="claude-sonnet-4-6", 
        max_tokens=300,
        system=reglas_del_agente,
        messages=[
            {"role": "user", "content": f"Basado en tus reglas, analiza este 'git status' real de mi repositorio y redacta el comando exacto de git commit para los cambios pendientes:\n\n{estado_git}"}
        ]
    )
    
    print("=== RESPUESTA DEL AGENTE ===")
    print(respuesta.content[0].text)

if __name__ == "__main__":
    probar_agente()