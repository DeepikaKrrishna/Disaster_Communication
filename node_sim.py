import json, time

class Node:
    def __init__(self, node_id, channel):
        self.node_id = node_id
        self.channel = channel
        self.seq = 0             # Sequence number for packets
        self.sent = 0            # Total packets sent
        self.delivered = 0       # Total successfully delivered

    def send_alert(self, message, max_retries=2):
        """
        Sends an alert message over the virtual LoRa channel.
        Retries up to max_retries times if packet is lost.
        """
        pkt = {
            "type": "ALERT",
            "id": self.node_id,
            "seq": self.seq,
            "msg": message,
            "timestamp": time.time()
        }
        self.sent += 1

        for attempt in range(max_retries + 1):
            print(f"[Node {self.node_id}] → Sending (seq {self.seq}, attempt {attempt+1}): {pkt}")
            tx = self.channel.transmit(json.dumps(pkt))

            if tx:  # Packet successfully transmitted
                self.delivered += 1
                break
            else:
                # Packet lost, simulate retransmission
                print(f"[Node {self.node_id}] ⚠ Packet lost! Retrying... ({attempt+1}/{max_retries})")
                time.sleep(0.2)  # small wait before retry

        self.seq += 1
        return tx
