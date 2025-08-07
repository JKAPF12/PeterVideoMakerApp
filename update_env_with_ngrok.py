import requests
from dotenv import set_key
from pathlib import Path

def update_env_with_ngrok():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json().get("tunnels", [])
        https_tunnel = next((t for t in tunnels if t["proto"] == "https"), None)

        if not https_tunnel:
            raise Exception("No HTTPS tunnel found")

        ngrok_url = https_tunnel["public_url"]
        env_path = Path(".env").resolve()

        if not env_path.exists():
            print(f".env not found at {env_path}")
            return

        set_key(str(env_path), "VITE_API_BASE", ngrok_url)
        print(f"✅ Updated VITE_API_BASE={ngrok_url} in {env_path}")
    except Exception as e:
        print(f"❌ Failed to update .env: {e}")

if __name__ == "__main__":
    update_env_with_ngrok()