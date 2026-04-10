import asyncio
import os
import shutil
from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Cargamos credenciales
load_dotenv()
client = Anthropic()

async def iniciar_agente_web():
    print("🚀 Arrancando el Servidor MCP de Puppeteer...")
    
    # Buscamos npx de forma segura en Windows
    ruta_npx = shutil.which("npx")
    if not ruta_npx:
        print("❌ Error: No se pudo encontrar npx en tu sistema.")
        return

    # Parámetros limpios y exactos
    server_params = StdioServerParameters(
        command=ruta_npx,
        args=["-y", "@modelcontextprotocol/server-puppeteer"],
        env=os.environ.copy()
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ ¡Conectado al servidor MCP con éxito!")

                herramientas_mcp = await session.list_tools()
                nombres_herramientas = [t.name for t in herramientas_mcp.tools]
                print(f"🛠️  Herramientas web disponibles: {nombres_herramientas}\n")

                tools_para_claude = [
                    {"name": t.name, "description": t.description, "input_schema": t.inputSchema}
                    for t in herramientas_mcp.tools
                ]

                print("🧠 Pidiendo a Claude que navegue por internet...")
                respuesta = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=500,
                    tools=tools_para_claude,
                    messages=[
                        {"role": "user", "content": "Navega a la web 'https://example.com' y dime exactamente qué texto aparece en el título principal de la página."}
                    ]
                )

                if respuesta.stop_reason == "tool_use":
                    tool_call = next(block for block in respuesta.content if block.type == "tool_use")
                    print(f"🤖 Claude ejecutando: {tool_call.name} con parámetros: {tool_call.input}\n")
                    
                    # Llamamos a la herramienta en el servidor
                    resultado = await session.call_tool(tool_call.name, tool_call.input)
                    print("=== LO QUE VIO EL NAVEGADOR ===")
                    print(resultado.content[0].text)
                else:
                    print("Respuesta de Claude sin usar herramientas:")
                    print(respuesta.content[0].text)
                    
    except Exception as e:
        print(f"💥 Error al conectar: {e}")

if __name__ == "__main__":
    asyncio.run(iniciar_agente_web())