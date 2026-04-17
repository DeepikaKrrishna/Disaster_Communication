import random
import time

class VirtualLoRa:
    def __init__(self, loss_rate=0.2, delay_range=(0.1, 1.0)):
        self.loss_rate = loss_rate
        self.delay_range = delay_range

    def transmit(self, packet):
        # simulate dynamic delay
        dynamic_delay = random.uniform(*self.delay_range) * random.uniform(0.5, 1.5)
        time.sleep(dynamic_delay)
        # simulate packet loss
        if random.random() < self.loss_rate:
            return None
        return packet
