import random
from client import GameClient

def debug_registration():
    pid = f"debug_bot_{random.randint(100, 999)}"
    client = GameClient()
    print(f"Registering {pid}...")
    reg = client.register(pid, "DebugBot", location="remote")
    print(f"Registration Response: {reg}")

if __name__ == "__main__":
    debug_registration()
