import time, random
from lora_channel import VirtualLoRa
from node_sim import Node
from gateway_sim import Gateway
from server_sim import Server
import matplotlib.pyplot as plt

# ----------------- Setup -----------------
server = Server()
channel = VirtualLoRa(loss_rate=0.2, delay_range=(0.1, 0.8))
gateway = Gateway(channel, server)

# Create multiple nodes
nodes = [Node(f"N{i+1}", channel) for i in range(5)]
messages = ["Flood detected", "Fire alert", "Building collapse", "Landslide risk"]

# Track retries for analysis
total_retries = 0

# ----------------- Run Simulation -----------------
print("\n=== Starting Disaster Communication Simulation ===\n")
start = time.time()

for i in range(20):  # total message rounds
    node = random.choice(nodes)
    msg = random.choice(messages)
    packet = node.send_alert(msg, max_retries=2)
    gateway.receive(packet)
    # Count retries: retries = sent - delivered for this message
    total_retries += max(0, node.sent - node.delivered)
    time.sleep(0.5)

end = time.time()

# ----------------- Metrics -----------------
total_sent = sum(n.sent for n in nodes)
total_delivered = server.received
pdr = (total_delivered / total_sent) * 100
avg_delay = (end - start) / total_sent
total_time = end - start
throughput = total_delivered / total_time  # packets/sec

# ----------------- Print Summary -----------------
print("\n=== Simulation Summary ===")
print(f"Total Packets Sent: {total_sent}")
print(f"Packets Delivered: {total_delivered}")
print(f"Packet Delivery Ratio: {pdr:.2f}%")
print(f"Average Delay per Packet: {avg_delay:.2f} s")
print(f"Throughput: {throughput:.2f} packets/sec")
print(f"Total Retries Due to Packet Loss: {total_retries}")

# ----------------- Graphs -----------------
plt.figure(figsize=(8,5))

# Sent vs Delivered
plt.subplot(1,2,1)
plt.bar(["Sent", "Delivered"], [total_sent, total_delivered], color=['orange', 'green'])
plt.title("Packets Sent vs Delivered")
plt.ylabel("Count")

# Retries Graph
plt.subplot(1,2,2)
plt.bar(["Retries"], [total_retries], color='red')
plt.title("Total Retries Due to Packet Loss")

plt.tight_layout()
plt.show()
