import time
import tkinter as tk
import tkinter.font as tkFont
import paho.mqtt.client as mqtt
import requests
import xmlrpc.client
import threading


class BenchmarkApp:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.label = tk.Label(self.frame, text="Benchmark Latency")
        self.label.pack()

        self.start_button = tk.Button(
            self.frame, text="Start Benchmark", command=self.start_benchmark_thread
        )
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(
            self.frame, text="Reset Results", command=self.reset_results
        )
        self.reset_button.pack(pady=10)

        # MQTT Client
        self.broker = "broker.hivemq.com"
        self.port = 1883
        self.topic = "BenchmarkSister"
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.loop_start()  # Start the MQTT loop in a separate thread

        # Measure MQTT Latency
        self.mqtt_subscribe_time = 0
        self.mqtt_publish_time = 0
        self.mqtt_latency = 0

        self.mqtt_client.connect(self.broker, self.port)
        self.mqtt_client.subscribe(self.topic)

        self.http_server_latency = 0
        self.http_client_latency = 0
        self.rpc_latency = 0

        # Define bold font
        self.bold_font = tkFont.Font(weight="bold")

        # Create a frame for results
        self.result_frame = tk.Frame(self.frame)
        self.result_frame.pack(pady=10)

        self.benchmark_running = False  # Flag to indicate if benchmark is running

    def on_mqtt_message(self, client, userdata, msg):
        # Handle incoming MQTT messages here
        self.mqtt_latency = (
            time.time() - self.mqtt_publish_time
        ) * 1000  # Calculate latency in ms
        print(f"Received MQTT message: {msg.payload.decode()}")
        print(f"MQTT Latency: {self.mqtt_latency:.2f} ms")

    def start_benchmark_thread(self):
        # Disable buttons
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.start_button.config(text="Running Benchmark...")

        # Start the benchmark in a separate thread
        self.benchmark_running = True
        threading.Thread(target=self.start_benchmark).start()

    def start_benchmark(self):
        # Clear previous results
        self.clear_results()

        # Measure MQTT latency
        mqtt_subscribe_time, mqtt_publish_time, mqtt_latency_total = (
            self.measure_mqtt_latency()
        )

        # Measure HTTP latency
        http_latency_total, server_latency, client_latency = self.measure_http_latency()

        # Measure RPC latency
        rpc_latency_total = self.measure_rpc_latency()

        # Update UI with results
        self.master.after(
            0,
            self.update_results,
            mqtt_subscribe_time,
            mqtt_publish_time,
            server_latency,
            client_latency,
            http_latency_total,
            rpc_latency_total,
        )

        # Mark benchmark as complete
        self.benchmark_running = False

        # Enable buttons after the benchmark is complete
        self.master.after(0, self.enable_buttons)

    def update_results(
        self,
        mqtt_subscribe_time,
        mqtt_publish_time,
        server_latency,
        client_latency,
        http_latency_total,
        rpc_latency_total,
    ):
        # Create labels for results with padding and bold totals
        tk.Label(self.result_frame, text="MQTT Latency", font=self.bold_font).pack(
            anchor="w"
        )
        tk.Label(
            self.result_frame, text=f"Subscribe Time: {mqtt_subscribe_time:.2f} ms"
        ).pack(anchor="w")
        tk.Label(
            self.result_frame, text=f"Publish Time: {mqtt_publish_time:.2f} ms"
        ).pack(anchor="w")
        tk.Label(
            self.result_frame, text=f"Receiver Latency: {self.mqtt_latency:.2f} ms"
        ).pack(anchor="w")
        tk.Label(
            self.result_frame,
            text=f"Total MQTT Latency: {(mqtt_subscribe_time + mqtt_publish_time + self.mqtt_latency):.2f} ms",
            font=self.bold_font,
        ).pack(anchor="w")

        tk.Label(self.result_frame, text="").pack()  # Add some space between sections

        tk.Label(self.result_frame, text="HTTP Latency", font=self.bold_font).pack(
            anchor="w"
        )
        tk.Label(
            self.result_frame, text=f"Server Latency: {server_latency:.2f} ms"
        ).pack(anchor="w")
        tk.Label(
            self.result_frame, text=f"Client Latency: {client_latency:.2f} ms"
        ).pack(anchor="w")
        tk.Label(
            self.result_frame,
            text=f"Total HTTP Latency: {http_latency_total:.2f} ms",
            font=self.bold_font,
        ).pack(anchor="w")

        tk.Label(self.result_frame, text="").pack()  # Add some space between sections

        tk.Label(self.result_frame, text="RPC Latency", font=self.bold_font).pack(
            anchor="w"
        )
        tk.Label(
            self.result_frame,
            text=f"RPC Latency: {rpc_latency_total:.2f} ms",
            font=self.bold_font,
        ).pack(anchor="w")

    def enable_buttons(self):
        # Enable buttons after the benchmark is complete
        if not self.benchmark_running:  # Check if the benchmark is not running
            self.start_button.config(state=tk.NORMAL)
            self.start_button.config(text="Start Benchmark")
            self.reset_button.config(state=tk.NORMAL)

    def reset_results(self):
        # Reset the results display
        self.clear_results()

    def clear_results(self):
        # Clear previous results from the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

    def measure_mqtt_latency(self):
        # Record start time for subscribing
        subscribe_start_time = time.time()
        self.mqtt_client.subscribe(self.topic)
        self.mqtt_subscribe_time = (
            time.time() - subscribe_start_time
        ) * 1000  # Subscribe latency in ms

        # Record start time for publishing
        self.mqtt_publish_time = time.time()
        self.mqtt_client.publish(self.topic, "Benchmark Test Message")

        # Wait for the message to be received (with a timeout)
        start_wait_time = time.time()
        while (
            self.mqtt_latency == 0 and (time.time() - start_wait_time) < 2
        ):  # 2 seconds timeout
            time.sleep(0.1)  # Small delay to prevent busy waiting

        # Return the measured times
        return (
            self.mqtt_subscribe_time,
            (time.time() - self.mqtt_publish_time) * 1000,
            self.mqtt_latency,
        )

    def measure_http_latency(self):
        # Measure server latency
        server_start_time = time.time()
        response = requests.post(
            "http://localhost:8001/chat",
            json={"username": "benchmark", "message": "This is a benchmark message"},
        )
        server_latency = (
            time.time() - server_start_time
        ) * 1000  # Server latency in ms

        # Measure client latency
        client_start_time = time.time()
        if response.status_code == 200:
            response_data = response.json()
            print(f"HTTP Response: {response_data}")
        client_latency = (
            time.time() - client_start_time
        ) * 1000  # Client latency in ms

        # Total HTTP latency
        total_http_latency = server_latency + client_latency
        return total_http_latency, server_latency, client_latency

    def measure_rpc_latency(self):
        start_time = time.time()
        with xmlrpc.client.ServerProxy("http://localhost:8002/") as proxy:
            # Call the 'add' method with sample values
            result = proxy.add(5, 10)
            print(f"RPC Response (add): {result}")  # Print the result of the add method
        end_time = time.time()
        return (end_time - start_time) * 1000  # Return latency in milliseconds


if __name__ == "__main__":
    root = tk.Tk()
    app = BenchmarkApp(root)
    root.mainloop()
