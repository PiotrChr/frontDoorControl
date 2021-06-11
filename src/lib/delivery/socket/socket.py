import websocket


class Socket:
    def __init__(self, host):
        self.host = host
        self.connection = None

    def create(self):
        self.connection = websocket.create_connection(self.host)

    def send(self, data):
        self.connection.send(data)
