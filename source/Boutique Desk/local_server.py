from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import webbrowser


ROOT = Path(__file__).resolve().parent
APP_ROOT = ROOT / "app"
HOST = "127.0.0.1"
PORT = 4173
URL = f"http://{HOST}:{PORT}/"


class BoutiqueHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        requested = self.path.split("?", 1)[0].split("#", 1)[0]
        last_segment = requested.rsplit("/", 1)[-1]
        if "." not in last_segment:
            file_path = Path(self.translate_path(requested))
            if not file_path.exists():
                self.path = "/index.html"
        super().do_GET()

    def do_HEAD(self):
        requested = self.path.split("?", 1)[0].split("#", 1)[0]
        last_segment = requested.rsplit("/", 1)[-1]
        if "." not in last_segment:
            file_path = Path(self.translate_path(requested))
            if not file_path.exists():
                self.path = "/index.html"
        super().do_HEAD()

    def log_message(self, format_string, *args):
        print("[Boutique Desk] " + format_string % args)


def main():
    if not (APP_ROOT / "index.html").is_file():
        raise SystemExit("The app files are missing. Re-extract the complete download.")

    server = ThreadingHTTPServer(
        (HOST, PORT), partial(BoutiqueHandler, directory=str(APP_ROOT))
    )
    print(f"Boutique Desk is running on this computer at {URL}")
    print("Keep this window open while using the app. Press Ctrl+C to stop it.")
    threading.Timer(0.8, lambda: webbrowser.open(URL)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBoutique Desk stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
