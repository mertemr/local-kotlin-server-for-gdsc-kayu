import os
import server
import waitress

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8002")

if __name__ == "__main__":
    waitress.serve(server.app, host=HOST, port=PORT, threads=4)