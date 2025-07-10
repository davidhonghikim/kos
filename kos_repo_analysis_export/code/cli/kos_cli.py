import typer
import requests
import json

app = typer.Typer()

BASE = "http://localhost:8000"

@app.command()
def health():
    res = requests.get(f"{BASE}/admin/health")
    print(res.json())

@app.command()
def vault(key: str):
    res = requests.get(f"{BASE}/admin/vault/{key}")
    print(res.json())

@app.command()
def send(intent: str, payload: str):
    parsed = json.loads(payload)
    res = requests.post(f"{BASE}/admin/klf/send", json={"intent": intent, "payload": parsed})
    print(res.json())

if __name__ == "__main__":
    app() 