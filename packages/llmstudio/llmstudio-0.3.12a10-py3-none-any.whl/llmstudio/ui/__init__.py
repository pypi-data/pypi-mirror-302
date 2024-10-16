import os
import subprocess
from pathlib import Path
import threading
from threading import Event

from llmstudio.config import UI_PORT


def run_bun_in_thread():
    ui_dir = Path(os.path.join(os.path.dirname(__file__)))
    try:
        subprocess.run(["bun", "install", "--silent"], cwd=ui_dir, check=True)
        subprocess.run(
            ["bun", "dev", "--port", UI_PORT],
            cwd=ui_dir,
            check=True,
        )
    except Exception as e:
        print(f"Error running LLMstudio UI: {e}")


def run_ui_app(started_event: Event):
    thread = threading.Thread(target=run_bun_in_thread)
    thread.start()
    started_event.set() #just here for compatibility
