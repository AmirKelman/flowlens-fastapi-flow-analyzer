import typer
import requests

app = typer.Typer()

API = "http://localhost:8000"


@app.command()
def analyze(path_or_git: str):
    payload = {
        "source": {
            "type": "git" if path_or_git.startswith("http") else "path",
            "value": path_or_git,
        }
    }
    r = requests.post(f"{API}/analyze", json=payload, timeout=30)
    typer.echo(f"HTTP {r.status_code}")
    typer.echo(r.text)


if __name__ == "__main__":
    app()
