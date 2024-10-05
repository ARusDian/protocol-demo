import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import json
import threading

# MQTT Settings
BROKER = "broker.hivemq.com"
PORT = 1883


class MQTTClient:
    def __init__(self, parent):
        self.parent = parent
        self.client = mqtt.Client()
        self.is_connected = False

        self.setup_ui()
        self.create_diagram()  # Add the communication diagram
        self.connect_mqtt()

    def setup_ui(self):
        # Add a connection status label
        self.status_label = tk.Label(self.parent, text="Status: Disconnected", fg="red")
        self.status_label.pack(pady=5)

        mqtt_username_frame = tk.Frame(self.parent)
        mqtt_username_frame.pack(pady=10)
        mqtt_username_label = tk.Label(mqtt_username_frame, text="Username:")
        mqtt_username_label.pack(side=tk.LEFT, padx=5)
        self.username_entry = tk.Entry(mqtt_username_frame, width=20)
        self.username_entry.pack(side=tk.LEFT, padx=5)

        mqtt_topic_frame = tk.Frame(self.parent)
        mqtt_topic_frame.pack(pady=10)
        mqtt_topic_label = tk.Label(mqtt_topic_frame, text="Topic:")
        mqtt_topic_label.pack(side=tk.LEFT, padx=5)
        self.topic_entry = tk.Entry(mqtt_topic_frame, width=30)
        self.topic_entry.pack(side=tk.LEFT, padx=5)

        mqtt_publisher_frame = tk.Frame(self.parent)
        mqtt_publisher_frame.pack(pady=10)
        mqtt_publisher_label = tk.Label(mqtt_publisher_frame, text="Message:")
        mqtt_publisher_label.pack(side=tk.LEFT, padx=5)
        self.publisher_entry = tk.Entry(mqtt_publisher_frame, width=30)
        self.publisher_entry.pack(side=tk.LEFT, padx=5)
        mqtt_publisher_button = tk.Button(
            mqtt_publisher_frame, text="Publish", command=self.start_publish_thread
        )
        mqtt_publisher_button.pack(side=tk.LEFT, padx=5)

        mqtt_subscriber_frame = tk.Frame(self.parent)
        mqtt_subscriber_frame.pack(pady=10)
        mqtt_subscriber_label = tk.Label(mqtt_subscriber_frame, text="Subscriber Log:")
        mqtt_subscriber_label.pack()
        self.subscriber_textbox = scrolledtext.ScrolledText(
            mqtt_subscriber_frame, width=60, height=15, state=tk.DISABLED
        )
        self.subscriber_textbox.pack(pady=5)
        mqtt_subscribe_button = tk.Button(
            self.parent, text="Subscribe", command=self.start_subscribe_thread
        )
        mqtt_subscribe_button.pack(pady=10)

    def create_diagram(self):
        # Create a canvas for the communication diagram
        self.canvas = tk.Canvas(self.parent, width=400, height=200, bg="white")
        self.canvas.pack(pady=20)

        # Draw the diagram
        self.client_box = self.canvas.create_rectangle(
            50, 50, 150, 100, fill="lightblue"
        )
        self.broker_box = self.canvas.create_rectangle(
            250, 50, 350, 100, fill="lightgreen"
        )
        self.canvas.create_text(100, 75, text="Client", font=("Arial", 12))
        self.canvas.create_text(300, 75, text="Broker", font=("Arial", 12))

        # Create two arrows for publish and receive actions
        self.publish_arrow = self.canvas.create_line(
            150, 55, 250, 55, arrow=tk.LAST, fill="blue", width=2
        )
        self.receive_arrow = self.canvas.create_line(
            250, 95, 150, 95, arrow=tk.LAST, fill="green", width=2
        )

        # Initially hide the receive arrow
        self.canvas.itemconfig(self.receive_arrow, state=tk.HIDDEN)

    def on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        msg_data = json.loads(msg)
        sender_message = msg_data.get("message", "No message")
        sender_name = msg_data.get("username", "Unknown")

        self.parent.after(0, self.update_subscriber_log, sender_name, sender_message)

    def connect_mqtt(self):
        try:
            self.client.connect(BROKER, PORT)
            self.is_connected = True
            self.status_label.config(text="Status: Connected", fg="green")
            self.client.on_message = self.on_message
            self.client.loop_start()
        except Exception as e:
            print(f"Connection failed: {e}")
            self.status_label.config(text="Status: Disconnected", fg="red")

    def mqtt_publish_message(self):
        msg = self.publisher_entry.get()
        user = self.username_entry.get()
        topic = self.topic_entry.get()
        if msg and user and topic:
            full_message = {
                "username": user,
                "message": msg,
            }
            self.client.publish(topic, json.dumps(full_message))
            self.publisher_entry.delete(0, tk.END)
            self.animate_publish()  # Call animation for publishing

    def start_publish_thread(self):
        threading.Thread(target=self.mqtt_publish_message, daemon=True).start()

    def mqtt_subscribe_topic(self):
        topic = self.topic_entry.get()
        if topic:
            self.client.subscribe(topic)
            self.subscriber_textbox.config(state=tk.NORMAL)
            self.subscriber_textbox.insert(tk.END, f"Subscribed to topic: {topic}\n")
            self.subscriber_textbox.config(state=tk.DISABLED)

    def start_subscribe_thread(self):
        threading.Thread(target=self.mqtt_subscribe_topic, daemon=True).start()

    def update_subscriber_log(self, username, message):
        self.subscriber_textbox.config(state=tk.NORMAL)
        self.subscriber_textbox.insert(tk.END, f"{username}: {message}\n")
        self.subscriber_textbox.see(tk.END)  # Automatically scroll to the bottom
        self.subscriber_textbox.config(state=tk.DISABLED)

        self.animate_message_received(
            username, message
        )  # Call animation for receiving message

    def animate_publish(self):
        self.canvas.itemconfig(
            self.receive_arrow, state=tk.HIDDEN
        )  # Hide receive arrow
        self.canvas.itemconfig(self.publish_arrow, fill="blue")  # Change arrow to blue
        self.parent.after(
            100, lambda: self.canvas.itemconfig(self.publish_arrow, fill="lightblue")
        )  # Return to original color

    def animate_message_received(self, username, message):
        self.canvas.itemconfig(
            self.publish_arrow, state=tk.HIDDEN
        )  # Hide publish arrow
        self.canvas.itemconfig(
            self.receive_arrow, state=tk.NORMAL
        )  # Show receive arrow
        self.canvas.itemconfig(
            self.receive_arrow, fill="green"
        )  # Change arrow to green
        self.parent.after(
            100, lambda: self.canvas.itemconfig(self.receive_arrow, fill="lightgreen")
        )  # Return to original color

    def reset_status(self):
        self.status_label.config(text="Status: Connected", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MQTT Client with Visual Representation")
    mqtt_client = MQTTClient(root)
    root.mainloop()
