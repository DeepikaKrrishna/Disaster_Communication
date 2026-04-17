import json, time

class Gateway:
    def __init__(self, channel, server):
        self.channel = channel
        self.server = server

    def receive(self, packet):
        if not packet:
            return False
        data = json.loads(packet)
        print(f"[Gateway] ⇐ Received from {data['id']}: {data['msg']}")
        time.sleep(0.1)
        self.ack(data)
        self.forward_to_server(data)
        return True

    def ack(self, data):
        print(f"[Gateway] → ACK sent for seq {data['seq']}")

    def forward_to_server(self, data):
        self.server.process_message(data)
