import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import json
import threading

# MQTT Settings
BROKER = "broker.hivemq.com"  # URL broker MQTT
PORT = 1883  # Port untuk koneksi MQTT


class MQTTClient:
    def __init__(self, parent):
        self.parent = parent
        self.client = mqtt.Client()  # Inisialisasi client MQTT
        self.is_connected = False  # Status koneksi

        self.setup_ui()  # Mengatur tampilan antarmuka pengguna
        self.create_diagram()  # Menambahkan diagram komunikasi
        self.connect_mqtt()  # Menghubungkan ke broker MQTT

    def setup_ui(self):
        # Membuat label untuk status koneksi
        self.status_label = tk.Label(self.parent, text="Status: Disconnected", fg="red")
        self.status_label.pack(pady=5)

        # Frame untuk username
        mqtt_username_frame = tk.Frame(self.parent)
        mqtt_username_frame.pack(pady=10)
        mqtt_username_label = tk.Label(mqtt_username_frame, text="Username:")
        mqtt_username_label.pack(side=tk.LEFT, padx=5)
        self.username_entry = tk.Entry(mqtt_username_frame, width=20)
        self.username_entry.pack(side=tk.LEFT, padx=5)

        # Frame untuk topic
        mqtt_topic_frame = tk.Frame(self.parent)
        mqtt_topic_frame.pack(pady=10)
        mqtt_topic_label = tk.Label(mqtt_topic_frame, text="Topic:")
        mqtt_topic_label.pack(side=tk.LEFT, padx=5)
        self.topic_entry = tk.Entry(mqtt_topic_frame, width=30)
        self.topic_entry.pack(side=tk.LEFT, padx=5)

        # Frame untuk publisher
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

        # Frame untuk subscriber log
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
        # Membuat canvas untuk diagram komunikasi MQTT
        self.canvas = tk.Canvas(self.parent, width=400, height=200, bg="white")
        self.canvas.pack(pady=20)

        # Menggambar kotak untuk client dan broker
        self.client_box = self.canvas.create_rectangle(
            50, 50, 150, 100, fill="lightblue"
        )
        self.broker_box = self.canvas.create_rectangle(
            250, 50, 350, 100, fill="lightgreen"
        )
        self.canvas.create_text(100, 75, text="Client", font=("Arial", 12))
        self.canvas.create_text(300, 75, text="Broker", font=("Arial", 12))

        # Membuat dua panah untuk aksi publish dan receive
        self.publish_arrow = self.canvas.create_line(
            150, 55, 250, 55, arrow=tk.LAST, fill="blue", width=2
        )
        self.receive_arrow = self.canvas.create_line(
            250, 95, 150, 95, arrow=tk.LAST, fill="green", width=2
        )

        # Secara awal menyembunyikan panah receive
        self.canvas.itemconfig(self.receive_arrow, state=tk.HIDDEN)

    def on_message(self, client, userdata, message):
        # Callback ketika menerima pesan dari broker
        msg = message.payload.decode("utf-8")  # Decode payload pesan
        msg_data = json.loads(msg)  # Mengubah JSON menjadi dictionary
        sender_message = msg_data.get("message", "No message")  # Mengambil pesan
        sender_name = msg_data.get("username", "Unknown")  # Mengambil username pengirim

        # Memperbarui log subscriber di antarmuka pengguna
        self.parent.after(0, self.update_subscriber_log, sender_name, sender_message)

    def connect_mqtt(self):
        # Menghubungkan client MQTT ke broker
        try:
            self.client.connect(BROKER, PORT)  # Mencoba menghubungkan
            self.is_connected = True
            self.status_label.config(
                text="Status: Connected", fg="green"
            )  # Memperbarui status
            self.client.on_message = (
                self.on_message
            )  # Menetapkan callback untuk pesan masuk
            self.client.loop_start()  # Memulai loop untuk menangani pesan
        except Exception as e:
            print(f"Connection failed: {e}")  # Menampilkan kesalahan koneksi
            self.status_label.config(
                text="Status: Disconnected", fg="red"
            )  # Memperbarui status

    def mqtt_publish_message(self):
        # Fungsi untuk menerbitkan pesan ke topik
        msg = self.publisher_entry.get()  # Mengambil pesan dari entry
        user = self.username_entry.get()  # Mengambil username dari entry
        topic = self.topic_entry.get()  # Mengambil topik dari entry
        if msg and user and topic:
            # Membentuk payload pesan sebagai dictionary
            full_message = {
                "username": user,
                "message": msg,
            }
            self.client.publish(
                topic, json.dumps(full_message)
            )  # Menerbitkan pesan ke broker
            self.publisher_entry.delete(
                0, tk.END
            )  # Menghapus pesan setelah diterbitkan
            self.animate_publish()  # Memanggil animasi untuk publikasi

    def start_publish_thread(self):
        # Memulai thread untuk fungsi publish agar tidak mengganggu antarmuka pengguna
        threading.Thread(target=self.mqtt_publish_message, daemon=True).start()

    def mqtt_subscribe_topic(self):
        # Fungsi untuk berlangganan ke topik
        topic = self.topic_entry.get()  # Mengambil topik dari entry
        if topic:
            self.client.subscribe(topic)  # Berlangganan ke topik
            self.subscriber_textbox.config(state=tk.NORMAL)
            self.subscriber_textbox.insert(
                tk.END, f"Subscribed to topic: {topic}\n"
            )  # Menampilkan pesan di log
            self.subscriber_textbox.config(state=tk.DISABLED)

    def start_subscribe_thread(self):
        # Memulai thread untuk fungsi subscribe agar tidak mengganggu antarmuka pengguna
        threading.Thread(target=self.mqtt_subscribe_topic, daemon=True).start()

    def update_subscriber_log(self, username, message):
        # Memperbarui log subscriber dengan pesan yang diterima
        self.subscriber_textbox.config(state=tk.NORMAL)
        self.subscriber_textbox.insert(
            tk.END, f"{username}: {message}\n"
        )  # Menampilkan pesan baru
        self.subscriber_textbox.see(tk.END)  # Menggulung ke bagian bawah
        self.subscriber_textbox.config(state=tk.DISABLED)

        # Memanggil animasi untuk pesan yang diterima
        self.animate_message_received(username, message)

    def animate_publish(self):
        # Animasi untuk menunjukkan publikasi pesan
        self.canvas.itemconfig(
            self.receive_arrow, state=tk.HIDDEN
        )  # Menyembunyikan panah receive
        self.canvas.itemconfig(
            self.publish_arrow, fill="blue"
        )  # Mengubah warna panah publish
        self.parent.after(
            100, lambda: self.canvas.itemconfig(self.publish_arrow, fill="lightblue")
        )  # Kembali ke warna awal setelah 100ms

    def animate_message_received(self, username, message):
        # Animasi untuk menunjukkan penerimaan pesan
        self.canvas.itemconfig(
            self.publish_arrow, state=tk.HIDDEN
        )  # Menyembunyikan panah publish
        self.canvas.itemconfig(
            self.receive_arrow, state=tk.NORMAL
        )  # Menampilkan panah receive
        self.canvas.itemconfig(
            self.receive_arrow, fill="green"
        )  # Mengubah warna panah receive
        self.parent.after(
            100, lambda: self.canvas.itemconfig(self.receive_arrow, fill="lightgreen")
        )  # Kembali ke warna awal setelah 100ms

    def reset_status(self):
        # Mengatur ulang status koneksi
        self.status_label.config(text="Status: Connected", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MQTT Client with Visual Representation")  # Judul aplikasi
    mqtt_client = MQTTClient(root)  # Membuat instance MQTTClient
    root.mainloop()  #
