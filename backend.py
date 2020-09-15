import os
from dotenv import load_dotenv
from wakeonlan import send_magic_packet

load_dotenv()
SERVER_MAC = os.getenv('SERVER_MAC')

def do_secret_job():
    send_magic_packet(SERVER_MAC)
