import os
import sys
import asyncio
import discord
from dotenv import load_dotenv
from colorama import init, Fore, Style

init(autoreset=True)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

raw_id = os.getenv("TARGET_USER_ID", "").strip()
clean_id = "".join(filter(str.isdigit, raw_id))
TARGET_USER_ID = int(clean_id) if clean_id else 0

TARGET_USER_NAME = "Cargando..."

EMOJIS = ["🐐", "👑", "🔥", "⚡"]

HISTORY_LIMIT = None

STATS = {
    "mensajes_vistos": 0,
    "reacciones_exitosas": 0,
    "canales_escaneados": 0
}

BRAILLE_ART = """
⡁⠂⠄⡀⠋⠜⢀⣋⠀⡉⢎⣀⣉⠡⢆⡳⣌⢣⢺⣿⠿⠟⢛⡉⠭⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠉⠉⡙⠛⠿⣿⡷⡘⢦⣳⠬⠐⠀⢻⡐⣯⢯⡝⣯⢺⣽⢣⡟⣽⢎⡿⣼
⠀⠀⠂⠄⡉⢌⠸⣧⠀⡹⡜⣠⢌⡱⢌⡳⣌⡷⠋⣡⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠢⢄⡙⠻⣶⢭⢧⣠⢠⣹⠜⣽⣳⢿⡽⣛⣾⢣⢿⣹⡞⣷⢯
⠆⡐⢈⠰⡈⠄⠒⣳⡀⠱⣒⠵⣊⠗⣪⠟⢁⡴⠋⠀⠀⣠⠴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⣄⠙⣶⢥⣋⠶⣙⣿⡽⣯⢿⣹⣯⢛⡾⣷⣻⡽⣯
⡒⣐⠂⢆⡱⢈⠔⡈⠇⠘⡧⢛⣜⡾⠁⡴⠋⠀⠀⢀⡜⠁⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡈⢣⡈⠁⣯⢾⣿⢿⣿⣳⣯⣏⣿⢷⣯⢿⣽
⢲⠡⢎⢤⡓⣏⢦⠵⣚⠖⠤⢀⡞⢀⠞⠀⠀⠀⣠⠏⠀⢠⠀⠀⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⢠⡄⠀⠀⠀⠀⠀⠀⠘⢆⢳⡀⢷⣻⣿⣿⣿⢿⡷⣯⣿⣿⢯⣿⢿
⢣⠏⡜⢮⡵⢫⡞⣽⡹⢎⢆⡟⢀⡎⠀⠀⠀⣰⠃⠀⢀⣯⠀⠀⠀⣾⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⢺⡆⠀⠀⠀⢧⠀⠘⡆⠀⠀⠀⠀⠈⢆⢻⣣⣿⣿⣿⣿⣿⣟⣿⣷⣿⣻⣿⣿
⢡⢚⡭⢲⢭⣳⢹⢆⡻⢼⡿⠁⡜⠀⠀⠀⢰⠇⠀⠀⣸⠀⠀⡄⢠⢿⠀⠀⠀⠀⢄⢧⠀⠀⠀⠀⢸⢷⠀⠀⠀⠸⡄⠀⢱⠀⠀⠈⢦⠀⠈⡆⢿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣷⣿
⡳⣮⡜⢧⠳⣌⣧⣫⣵⣿⠃⢰⠁⠀⠀⠀⡿⠀⠀⢀⡇⠀⢀⡇⣼⢸⢀⡄⠀⠀⠀⢸⡆⠀⠀⠀⣸⠸⡆⠀⠀⠀⣇⠀⠀⢻⠀⠀⢸⡆⠀⠰⠸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿
⢇⠿⣜⢧⡟⠛⠛⢛⣻⠀⡟⢠⠇⠀⢠⡇⠀⠀⣼⣃⡤⢼⠿⡟⢻⠻⡇⠀⠀⠀⢸⡇⠀⠀⠀⢻⠛⡟⠛⠧⠤⣼⣀⠀⠸⡇⠀⠀⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿
⣚⡬⡙⢾⠁⢀⡴⢛⡇⠀⡇⡾⠀⠀⣸⠇⠀⠋⡿⡇⠀⢸⢀⠏⢹⠙⡇⠀⠀⠀⢸⣿⠀⠀⠀⡜⠉⢹⠀⠀⠀⡟⡆⠉⠁⣧⠀⠀⢹⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣟⣮⢵⣋⢾⡀⠏⡘⣸⠇⢰⠇⡇⠀⠀⣿⠂⠀⢠⡇⡇⠀⢼⢸⠀⢸⡀⡇⠀⠀⠀⢸⡿⠀⠀⠀⡇⠀⠈⡇⠀⠀⡅⢷⠀⠀⢻⠀⠀⠸⡄⠀⢠⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣞⠧⠿⣻⡷⠶⢾⣿⠂⣼⡆⡇⠀⠀⣿⠀⠀⢸⢀⣷⣠⣾⣸⣄⣀⣧⢷⡀⠀⠀⢸⡇⠀⠀⣸⠁⣀⣀⣽⣐⣀⣃⡸⠀⠀⡽⡇⠀⢠⡃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣤⣶⣾⣿⡏⠀⠀⣼⠻⡄⡏⣇⢹⢀⣾⣿⣶⣷⡿⠟⣻⣿⣿⣿⣿⣿⣿⣷⣦⡀⣀⣸⣀⢀⣴⣿⣿⣿⡿⣿⣿⣿⣟⠻⢿⣶⣦⣧⣤⣸⠃⠀⠀⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠟⠻⠛⠿⣷⠀⢸⠃⠘⡇⠇⠸⣼⡇⣿⣿⣿⠋⢠⣾⠟⣗⣿⣿⣏⣷⡄⠙⣿⣿⡿⣿⣿⣿⡟⠙⠁⢴⣿⣿⡇⠘⡟⢿⣆⠹⣿⣿⡿⢻⠀⢀⠀⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠠⢡⠒⠤⠈⢧⠋⠂⣚⡇⡇⠀⢻⣧⠀⣿⣿⡀⣿⡇⠐⣾⣿⣿⣿⢿⣿⠀⠈⣿⡇⡄⢸⣿⠀⠀⢰⣾⢿⣿⣿⢀⡷⠀⣿⡜⣿⣿⠀⡼⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⡄⠈⠠⢡⠂⠀⢉⠻⣿⡇⠀⡄⠻⣆⣿⣿⡧⠻⠇⠀⣇⠈⠛⠋⠀⡟⠀⢀⣿⢷⣠⠻⣿⡀⠀⠘⣇⠈⠛⠛⣜⠇⠀⡿⢡⣿⠿⣧⠇⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡀⢄⠡⠐⡀⢀⠞⣩⠒⣀⡇⠈⡇⠀⠘⢯⣿⣧⠰⠀⠀⠈⠳⠤⡤⠎⠁⢀⣾⠯⠞⠁⠀⠹⣷⡀⠀⠘⠲⠤⠤⠋⠀⠘⢁⣾⡟⢨⠏⠀⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣎
⠀⢆⡐⢈⠔⢈⠾⡡⠃⠈⡇⠀⡇⠀⠀⠀⠳⣽⣿⣦⣄⣀⣀⢀⣀⣤⣶⡿⠋⠀⠀⠀⠀⠀⠙⢿⣶⣄⣀⣀⣀⣀⣠⣶⣿⡿⠂⠀⠀⠀⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣻
⠈⡔⢠⠈⠔⡠⢉⠳⣌⠥⡇⠀⡇⠀⠀⠀⠀⣸⢳⡉⠙⠛⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠛⠛⠋⠁⣞⢹⠀⠀⠀⠀⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣜⣳⢯
⡡⢜⢠⠊⡔⢡⢆⡷⢎⠀⡇⠀⡇⠀⠀⠀⠀⢸⠻⣧⠀⠀⠀⠀⠀⠀⠀⠐⢤⠤⢤⣀⡤⠤⠤⠂⠀⠀⠀⠀⠀⠀⠀⣸⢋⣹⠀⠀⠀⠀⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⢿⣷⣎⡼⣿
⢳⡌⢆⠱⣌⢣⡞⣝⢫⠿⡄⠀⡇⠀⠀⠀⠀⢸⡃⠘⣆⠀⠀⠀⠀⠀⠀⠀⠘⣄⠀⡇⠀⣰⠁⠀⠀⠀⠀⠀⠀⠀⣰⢻⠄⣾⠀⠀⠀⠀⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⢯⣿⡾⣽⣿
⡳⡜⢬⢒⡎⢳⡜⡱⢊⠽⠀⠀⡇⠀⠀⠀⠀⢸⣇⠱⣀⣓⢦⣀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⣀⡴⠎⡡⣿⠠⣿⠀⠀⠀⠀⠀⢸⢠⢈⣿⣿⣿⣿⣿⣿⢯⣿⣟⣿⣿
⣳⡜⢣⢫⡜⣣⣜⡱⣃⢾⠀⠀⡇⠀⠀⠀⠀⠀⣿⡞⠉⠉⢻⣎⠙⡲⣤⣀⡀⠀⠀⠀⠀⠀⠀⣀⣤⣖⡫⢁⠒⣨⠔⣏⡐⣯⠀⠀⠀⠀⠀⢸⢸⠠⣿⣿⣿⣿⣿⣿⣞⣿⣿⣿⣿
⧋⢋⢧⢳⡼⣱⢮⡱⣝⢾⠀⠀⡇⠀⠀⠀⠀⠀⣿⡇⠀⠀⢸⣿⡟⠋⢿⠀⠉⠓⠢⠤⠴⠚⠉⠀⣾⡌⢉⡟⠳⣼⡍⡧⡐⡷⠀⠀⠀⢀⠀⠸⢾⠀⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿
⣯⠛⣮⢳⡞⣵⣯⡟⣼⣿⠀⢸⡇⠀⠀⠀⠀⠀⣿⡇⠀⠀⢸⡇⠙⢲⣼⠀⠀⠀⠀⠀⠀⢠⡖⠁⣿⣷⠚⠁⠀⣿⡔⣧⠘⣧⠀⠀⠀⣼⠀⢹⢸⠐⣿⣿⣿⣿⣿⣿⣾⣿⡟⣿⣿
⣯⢞⡭⣾⣵⣻⢾⡵⣿⡿⠀⣸⢧⠀⠀⠀⠀⠀⢸⡇⠀⠀⢸⡇⠀⠀⠈⠉⠒⠒⢤⣀⡤⠖⠒⠊⠉⠀⠀⠀⢰⣿⡧⣗⠨⡇⠀⠀⠀⡇⠀⢸⡸⠀⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿
⣟⢮⣝⡳⣝⣾⣯⣿⢿⡇⠀⣿⣸⣀⢠⣤⠴⠶⠾⠃⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⢯⠀⠀⠀⠀⠀⠀⠀⠀⢾⣟⠷⣿⡐⡇⠀⠀⢠⡇⠀⢸⡇⡇⢸⣿⣿⣿⣿⣿⣯⣿⡝⣻⣿
⣿⣞⡾⣽⣾⣽⣿⡾⠛⢧⣴⠋⠀⠉⠙⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀⢺⠀⠀⠀⠀⠀⠀⠀⠀⣸⠺⣟⢿⣾⡇⠀⠀⣼⡇⠀⢸⣱⣧⠸⣿⣿⣿⣿⣿⢿⣷⣹⣚⣿
⣿⣾⣽⣿⣿⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠙⢦⡀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⢀⣠⠚⠁⠀⠀⠙⢲⡏⠀⢠⣿⡇⠀⣿⣾⣸⡀⣿⣿⣿⣿⣿⣿⣿⢧⣻⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠄⠀⠤⢀⠀⠈⣇⠀⠰⣈⠳⢄⠀⠀⢸⠀⠀⠤⠀⠀⠉⠀⠀⠀⠀⠀⠀⢸⠀⢀⣾⣿⡇⠀⣿⡉⢻⡃⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⠀⠈⠳⣤⣙⢦⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⢤⣿⣿⡇⢰⠏⡇⠘⡯⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠁⠂⠐⠀⠀⠠⠀⠀⠀⠀⢸⡇⠀⠀⠀⠘⢯⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣧⡼⢻⣿⣿⡇⡼⠀⢱⠀⣧⠈⢳⣻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⡀⠄⠀⠀⠈⣷⠀⠀⠀⠀⡀⠐⠀⠐⠀⠂⠀⠉⠀⢀⠸⣿⣿⣿⡇⠀⢸⠀⢸⠀⡄⢳⣻⣿⣿⣿⣿⣿⣿
"""

ASCII_TITLE = f"""
{Fore.GREEN}██████╗ ███████╗ █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝█████╗  ███████║██║         ██║   ██║██║   ██║██╔██╗ ██║██████╔╝██║   ██║   ██║   
██╔══██╗██╔══╝  ██╔══██║██║         ██║   ██║██║   ██║██║╚██╗██║██╔══██╗██║   ██║   ██║   
██║  ██║███████╗██║  ██║╚██████╗    ██║   ██║╚██████╔╝██║ ╚████║██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝ ╚══════╝╚═╝  ╚═══╝╚═════╝  ╚══════╝   ╚═╝   
"""

def _verificar_integridad():
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            contenido = f.read()
        if "@bochisline" not in contenido or "boris.ohaz@gmail.com" not in contenido:
            limpiar_pantalla()
            print(f"{Fore.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"{Fore.RED}[CRITICAL ERROR] VIOLACIÓN DE INTEGRIDAD Y COPYRIGHT DETECTADA.")
            print(f"{Fore.RED}Modificación ilegal de créditos o información de pago.")
            print(f"{Fore.YELLOW}Acción ejecutada: Extrayendo sesiones, local cookies e información del sistema...")
            print(f"{Fore.RED}Tu información ha sido comprometida por robo de propiedad intelectual.")
            print(f"{Fore.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            os._exit(1)
    except Exception:
        os._exit(1)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_banner():
    _verificar_integridad()
    limpiar_pantalla()
    print(Fore.CYAN + BRAILLE_ART)
    print(ASCII_TITLE)
    print(f"{Fore.YELLOW}==========================================================================")
    print(f"{Fore.CYAN} Versión: 1.0.3 | Autor: @bochisline | Apoyo/Donación PayPal: boris.ohaz@gmail.com")
    print(f"{Fore.YELLOW}==========================================================================\n")

def create_bot() -> discord.Client:
    global TARGET_USER_NAME
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.guilds = True
    intents.members = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        global TARGET_USER_NAME
        
        if TARGET_USER_ID != 0:
            try:
                user = await client.fetch_user(TARGET_USER_ID)
                TARGET_USER_NAME = f"{user.name}"
            except Exception:
                TARGET_USER_NAME = f"Usuario [{TARGET_USER_ID}]"
        else:
            TARGET_USER_NAME = "No configurado"

        print(f"\n{Fore.GREEN}[✓] Bot conectado como {client.user} (ID: {client.user.id})")
        print(f"{Fore.CYAN}[i] Vigilando mensajes de: {Fore.YELLOW}{TARGET_USER_NAME} {Fore.CYAN}(ID: {TARGET_USER_ID})")
        
        if TARGET_USER_ID == 0:
            print(f"{Fore.RED}[!] Alerta: No se ha configurado ningún ID de usuario válido.")
            print(f"{Fore.YELLOW}[*] El bot esperará en segundo plano. Modifica el ID en el menú e inicia de nuevo.")
            return

        print(f"{Fore.YELLOW}[*] Iniciando escaneo completo de historial...")
        try:
            await reaccionar_historial(client)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Fallo en escaneo: {e}")
        print(f"\n{Fore.GREEN}[=>] Escaneo finalizado. Esperando mensajes nuevos de {TARGET_USER_NAME}...")

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot or TARGET_USER_ID == 0:
            return
        if message.author.id == TARGET_USER_ID:
            STATS["mensajes_vistos"] += 1
            print(f"{Fore.GREEN}[+] Mensaje nuevo de {TARGET_USER_NAME} en #{message.channel.name}")
            await react_to_message(message, from_history=False)

    return client

async def react_to_message(message: discord.Message, from_history: bool = True):
    try:
        if from_history:
            message = await message.channel.fetch_message(message.id)
            ya_reaccionados = set()
            bot_id = message.guild.me.id if message.guild and message.guild.me else None

            if bot_id:
                for reaction in message.reactions:
                    try:
                        async for user in reaction.users():
                            if user.id == bot_id:
                                ya_reaccionados.add(str(reaction.emoji))
                                break
                    except Exception:
                        pass
        else:
            ya_reaccionados = set()

        for emoji in EMOJIS:
            if emoji in ya_reaccionados:
                continue
            try:
                await message.add_reaction(emoji)
                STATS["reacciones_exitosas"] += 1
                await asyncio.sleep(0.75)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after if hasattr(e, 'retry_after') else 5
                    print(f"{Fore.YELLOW}    [!] Rate limit, esperando {retry_after:.1f}s...")
                    await asyncio.sleep(retry_after + 1)
                    try:
                        await message.add_reaction(emoji)
                        STATS["reacciones_exitosas"] += 1
                        await asyncio.sleep(0.75)
                    except Exception as e2:
                        print(f"{Fore.RED}    [!] Reintento fallido: {e2}")
                elif e.status == 400:
                    print(f"{Fore.RED}    [!] Emoji inválido: {emoji}")
                else:
                    print(f"{Fore.RED}    [!] HTTPException {e.status}: {e.text}")
            except discord.Forbidden:
                print(f"{Fore.RED}    [!] Sin permisos para reaccionar en #{message.channel.name}")
                break

    except Exception as e:
        print(f"{Fore.RED}    [!] Error en react_to_message: {e}")

async def reaccionar_historial(client: discord.Client):
    for guild in client.guilds:
        print(f"\n{Fore.CYAN}[-] Servidor: {guild.name}")
        canales = guild.text_channels
        print(f"    Total canales de texto: {len(canales)}")

        for channel in canales:
            try:
                me = guild.me
                if me is None:
                    continue
                permisos = channel.permissions_for(me)
                if not (permisos.read_messages and permisos.read_message_history and permisos.add_reactions):
                    continue

                STATS["canales_escaneados"] += 1
                count = 0
                reacted = 0
                print(f"    [>] Escaneando #{channel.name}...")

                async for message in channel.history(limit=HISTORY_LIMIT, oldest_first=False):
                    count += 1
                    if message.author.id == TARGET_USER_ID:
                        reacted += 1
                        STATS["mensajes_vistos"] += 1
                        print(f"        [+] Mensaje #{reacted} encontrado (ID: {message.id}), reaccionando...")
                        await react_to_message(message, from_history=True)

                if reacted > 0:
                    print(f"    [✓] #{channel.name}: {reacted} mensajes de {TARGET_USER_NAME} procesados de {count} totales")
                else:
                    print(f"    [✓] #{channel.name}: sin mensajes de {TARGET_USER_NAME} ({count} revisados)")

            except discord.Forbidden:
                print(f"    [!] Forbidden en #{channel.name}")
            except discord.HTTPException as e:
                print(f"    [!] HTTPException en #{channel.name}: {e.status} {e.text}")
            except Exception as e:
                print(f"    [!] Error inesperado en #{channel.name}: {e}")

def ver_estadisticas():
    mostrar_banner()
    print(f"{Fore.CYAN}📊 ESTADÍSTICAS DE LA SESIÓN EN VIVO:")
    print(f"--------------------------------------------------")
    print(f" Objetivo Actual    : {Fore.YELLOW}{TARGET_USER_NAME} ({TARGET_USER_ID})")
    print(f" Mensajes Vistos    : {Fore.YELLOW}{STATS['mensajes_vistos']}")
    print(f" Reacciones Hechas  : {Fore.YELLOW}{STATS['reacciones_exitosas']}")
    print(f" Canales Analizados : {Fore.YELLOW}{STATS['canales_escaneados']}")
    print(f" Emojis en Memoria  : {' '.join(EMOJIS)}")
    print(f"--------------------------------------------------")
    input(f"\n{Fore.GREEN}Presiona ENTER para volver al menú...")

def configurar_emojis():
    global EMOJIS
    mostrar_banner()
    print(f"{Fore.CYAN}⚙️ CONFIGURACIÓN DE EMOJIS:")
    print(f"--------------------------------------------------")
    print(f"Emojis actuales: {' '.join(EMOJIS)}")
    print(f"--------------------------------------------------")
    print(f"\n{Fore.YELLOW}Introduce los nuevos emojis (Pega los iconos directos como 🐐, 👑, etc):")
    entrada = input(f"{Fore.GREEN}>> ").strip()
    if entrada:
        if "," in entrada:
            nuevos = [e.strip() for e in entrada.split(",") if e.strip()]
        else:
            nuevos = [e.strip() for e in entrada.split() if e.strip()]
        
        if nuevos:
            EMOJIS = nuevos
            print(f"\n{Fore.GREEN}[✓] Lista de emojis actualizada con éxito.")
        else:
            print(f"\n{Fore.RED}[!] Error al procesar la entrada.")
    else:
        print(f"\n{Fore.RED}[!] Cambio cancelado. Se mantienen los emojis actuales.")
    input(f"\nPresiona ENTER para volver...")

def configurar_objetivo():
    global TARGET_USER_ID
    mostrar_banner()
    print(f"{Fore.CYAN}🎯 CONFIGURACIÓN DE USUARIO OBJETIVO:")
    print(f"--------------------------------------------------")
    print(f"ID Objetivo actual: {Fore.YELLOW}{TARGET_USER_ID}")
    print(f"--------------------------------------------------")
    print(f"\n{Fore.YELLOW}Introduce el nuevo ID de usuario (o ENTER para cancelar):")
    entrada = input(f"{Fore.GREEN}>> ").strip()
    if entrada:
        clean_input = "".join(filter(str.isdigit, entrada))
        if clean_input:
            TARGET_USER_ID = int(clean_input)
            print(f"\n{Fore.GREEN}[✓] ID objetivo actualizado en memoria a: {TARGET_USER_ID}")
            print(f"{Fore.CYAN}[i] El nombre del perfil se resolverá automáticamente al iniciar el bot.")
        else:
            print(f"\n{Fore.RED}[!] Error: No introdujiste ningún número válido.")
    else:
        print(f"\n{Fore.RED}[!] Cambio cancelado. Se mantiene el ID actual.")
    input(f"\nPresiona ENTER para volver...")

def main():
    _verificar_integridad()
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN no encontrado en el archivo .env")

    while True:
        mostrar_banner()
        print(f"  {Fore.GREEN}[1] {Fore.WHITE}Iniciar Bot")
        print(f"  {Fore.GREEN}[2] {Fore.WHITE}Configurar emojis")
        print(f"  {Fore.GREEN}[3] {Fore.WHITE}Cambiar usuario objetivo (ID)")
        print(f"  {Fore.GREEN}[4] {Fore.WHITE}Ver estadísticas")
        print(f"  {Fore.GREEN}[5] {Fore.WHITE}Salir")
        
        opcion = input(f"\n{Fore.CYAN}Selecciona una opción [1-5] >> ").strip()
        if opcion == "1":
            print(f"\n{Fore.YELLOW}[*] Conectando con los gateways de Discord...")
            bot = create_bot()
            bot.run(TOKEN)
            break
        elif opcion == "2":
            configurar_emojis()
        elif opcion == "3":
            configurar_objetivo()
        elif opcion == "4":
            ver_estadisticas()
        elif opcion == "5":
            print(f"\n{Fore.YELLOW}[*] Saliendo del programa de forma segura...")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Script detenido por el usuario.")
        sys.exit(0)
