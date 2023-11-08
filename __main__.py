import server

HOST = server.os.getenv("HOST", "localhost")
PORT = server.os.getenv("PORT", "8002")

if __name__ == "__main__":
    server.app.run(host=HOST, port=PORT, debug=True)
