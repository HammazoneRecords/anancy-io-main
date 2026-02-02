# Run AnancyIO Without Docker (Conda)

Run AnancyIO on your machine with Conda—no Docker required. Uses the same Flask web UI and backend as the Docker setup.

## Prerequisites

- **Conda** (Miniconda or Anaconda). Install from [conda.io](https://docs.conda.io/en/latest/miniconda.html).
- **Windows:** If `pip install -r requirements.txt` fails with "Microsoft Visual C++ 14.0 or greater is required", install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Desktop development with C++), then run the install again inside the Conda env.

## Quick start

### Windows (PowerShell)

```powershell
.\run-web.ps1
```

### macOS / Linux

```bash
chmod +x run-web.sh
./run-web.sh
```

The script creates a Conda env named `anancyio` (Python 3.12), installs dependencies if needed, and starts the app. First run may take several minutes. Then open **http://localhost:5000** in your browser.

---

## Manual setup (Conda)

If you prefer to run steps yourself:

```bash
# Create env
conda create -n anancyio python=3.12 -y
conda activate anancyio

# From the project root
pip install -r requirements.txt
playwright install chromium   # optional, for browser agent
python run_ui.py
```

Then open **http://localhost:5000**. To use another port:

```bash
python run_ui.py --port=5555
```

Or set `WEB_UI_PORT=5555` in a `.env` file in the project root.

---

## Configuration

Create a **`.env`** file in the project root (same folder as `run_ui.py`) to configure:

| Variable        | Description                    | Default   |
|----------------|--------------------------------|-----------|
| `WEB_UI_PORT`  | Port for the web UI            | `5000`    |
| `WEB_UI_HOST`  | Bind address                   | `localhost` |
| `AUTH_LOGIN`   | Web UI username (optional)     | —         |
| `AUTH_PASSWORD`| Web UI password (optional)    | —         |

Add API keys in the Web UI under **Settings** after first run, or in `.env` (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).

**Local Ollama:** In Settings, set the API base URL to `http://127.0.0.1:11434` (or `http://localhost:11434`) instead of `host.docker.internal`.

**Access from other devices (e.g. phone on same network):** Set `WEB_UI_HOST=0.0.0.0` in `.env`, or run `python run_ui.py --host=0.0.0.0`, then open `http://<your-PC-IP>:5000` from the other device.

---

## Differences from Docker

- **No Docker image:** You run the app with Conda and Python only.
- **Code execution tool:** Safe code execution that uses Docker containers will not work unless Docker is installed and running; other features work without it.
- **Root password / SSH:** For the Docker environment only; not used when running with Conda.
- **SearXNG / Redis:** Not required for basic chat and tools.

---

## Troubleshooting

- **Conda not found:** Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda and ensure `conda` is on your PATH.
- **Port in use:** Use `--port=5555` or `WEB_UI_PORT=5555` in `.env`.
- **Module not found:** Activate the env (`conda activate anancyio`) and run `pip install -r requirements.txt`.
- **Playwright errors:** Run `playwright install chromium` inside the Conda env.
- **Login loop / auth:** Use the same `AUTH_LOGIN` and `AUTH_PASSWORD` from `.env` in the Web UI login.
- **Windows: "Microsoft Visual C++ 14.0 or greater is required":** Install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Desktop development with C++), restart your terminal, then `conda activate anancyio` and `pip install -r requirements.txt` again.

For more help, see [docs/troubleshooting.md](docs/troubleshooting.md) and the project’s Discord/GitHub.
