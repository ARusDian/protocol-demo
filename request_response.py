import tkinter as tk
import requests
import time
import threading


class RequestResponseApp:
    def __init__(self, parent):
        self.parent = parent
        self.last_activity_time = (
            time.time()
        )  # Inisialisasi waktu aktivitas terakhir untuk melacak aktivitas pengguna
        self.setup_ui()  # Menyiapkan komponen antarmuka pengguna
        self.create_diagram()  # Membuat representasi visual dari proses permintaan-respons

        # Memulai pengecekan aktivitas dan pengecekan koneksi di thread terpisah
        self.check_activity()  # Memeriksa aktivitas pengguna (untuk manajemen UI)
        self.check_connection()  # Secara berkala memeriksa status koneksi server

    def setup_ui(self):
        # Mengatur elemen UI untuk input username
        request_username_label = tk.Label(self.parent, text="Username:")
        request_username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.parent)  # Kolom input untuk username
        self.username_entry.pack(pady=5)

        # Mengatur elemen UI untuk input pesan
        request_message_label = tk.Label(self.parent, text="Message:")
        request_message_label.pack(pady=5)
        self.message_entry = tk.Entry(self.parent)  # Kolom input untuk pesan
        self.message_entry.pack(pady=5)

        # Tombol untuk mengirim permintaan
        request_send_button = tk.Button(
            self.parent, text="Send", command=self.start_request_thread
        )
        request_send_button.pack(pady=20)

        # Label untuk menampilkan respons dari server
        self.response_label = tk.Label(self.parent, text="Response: ")
        self.response_label.pack(pady=10)

        # Label untuk menampilkan latensi
        self.latency_label = tk.Label(self.parent, text="")
        self.latency_label.pack(pady=10)

        # Label untuk menampilkan status server
        self.status_label = tk.Label(
            self.parent, text="Server Status: Checking...", fg="orange"
        )
        self.status_label.pack(pady=10)

    def create_diagram(self):
        # Membuat kanvas untuk diagram komunikasi
        self.canvas = tk.Canvas(self.parent, width=400, height=200, bg="white")
        self.canvas.pack(pady=20)

        # Menggambar diagram
        self.client_box = self.canvas.create_rectangle(
            50, 50, 150, 100, fill="lightblue"
        )
        self.server_box = self.canvas.create_rectangle(
            250, 50, 350, 100, fill="lightgreen"
        )
        self.canvas.create_text(100, 75, text="Client", font=("Arial", 12))
        self.canvas.create_text(300, 75, text="Server", font=("Arial", 12))

        # Membuat dua panah untuk permintaan dan respons
        self.request_arrow = self.canvas.create_line(
            150, 75, 250, 75, arrow=tk.LAST, fill="lightblue", width=2
        )
        self.response_arrow = self.canvas.create_line(
            250, 75, 150, 75, arrow=tk.FIRST, fill="lightgreen", width=2
        )

        # Awalnya menyembunyikan panah respons
        self.canvas.itemconfig(self.response_arrow, state=tk.HIDDEN)

    def start_request_thread(self):
        # Memulai thread untuk mengirim permintaan
        threading.Thread(target=self.send_request, daemon=True).start()
        self.last_activity_time = time.time()  # Memperbarui waktu aktivitas terakhir

    def send_request(self):
        username = self.username_entry.get()  # Mengambil username dari input
        message = self.message_entry.get()  # Mengambil pesan dari input
        if not username:
            # Menampilkan error jika username kosong
            self.parent.after(0, self.show_error, "Username cannot be empty")
            return

        url = "http://127.0.0.1:8001/chat"  # URL server untuk mengirim permintaan
        try:
            self.animate_sending()  # Memulai animasi pengiriman
            start_time = time.time()  # Mencatat waktu awal untuk menghitung latensi
            response = requests.post(
                url, json={"username": username, "message": message}
            )  # Mengirim permintaan POST ke server
            server_latency = (
                time.time() - start_time
            ) * 1000  # Menghitung latensi server dalam ms
            data = response.json()  # Mengonversi respons server menjadi format JSON
            chatbot_response = data.get(
                "response", "No Response"
            )  # Mendapatkan respons dari chatbot

            client_latency = f"{(time.time() - start_time) * 1000:.2f} ms"  # Menghitung latensi klien

            # Memperbarui respons di UI
            self.parent.after(
                0,
                self.update_response,
                chatbot_response,
                f"{server_latency:.2f} ms",
                client_latency,
            )

        except Exception as e:
            # Menampilkan error jika terjadi kesalahan saat menghubungi server
            self.parent.after(
                0, self.show_error, f"Error connecting to server: {str(e)}"
            )

    def animate_sending(self):
        # Menyembunyikan panah respons
        self.canvas.itemconfig(self.response_arrow, state=tk.HIDDEN)

        # Menganimasi panah permintaan untuk menunjukkan pengiriman pesan
        self.canvas.itemconfig(
            self.request_arrow, fill="blue"
        )  # Mengubah warna panah permintaan
        self.canvas.after(
            100, lambda: self.canvas.itemconfig(self.request_arrow, fill="lightblue")
        )  # Kembali ke warna asli setelah 100ms

    def animate_response(self):
        # Menyembunyikan panah permintaan
        self.canvas.itemconfig(self.request_arrow, state=tk.HIDDEN)

        # Menampilkan panah respons dan menganimasinya
        self.canvas.itemconfig(
            self.response_arrow, state=tk.NORMAL
        )  # Menampilkan panah respons
        self.canvas.itemconfig(
            self.response_arrow, fill="green"
        )  # Mengubah warna menjadi hijau
        self.canvas.after(
            100, lambda: self.canvas.itemconfig(self.response_arrow, fill="lightgreen")
        )  # Kembali ke warna asli setelah 100ms

    def update_response(self, chatbot_response, server_latency, client_latency):
        # Memperbarui respons di UI dan menjalankan animasi panah respons
        self.animate_response()  # Animasi panah respons
        self.response_label.config(
            text=f"Response: {chatbot_response}"
        )  # Memperbarui label respons
        self.latency_label.config(
            text=f"Server Latency: {server_latency} | Client Latency: {client_latency}"
        )  # Memperbarui label latensi
        self.last_activity_time = time.time()  # Memperbarui waktu aktivitas terakhir

    def show_error(self, error):
        # Menampilkan pesan kesalahan pada UI
        self.response_label.config(text="Error connecting to server")
        self.latency_label.config(text="")
        self.last_activity_time = time.time()  # Memperbarui waktu aktivitas terakhir

    def check_activity(self):
        # Memeriksa jika tidak ada aktivitas dalam waktu tertentu
        if time.time() - self.last_activity_time > 3:  # Timeout 3 detik
            self.canvas.itemconfig(
                self.request_arrow, state=tk.HIDDEN
            )  # Menyembunyikan panah permintaan
            self.canvas.itemconfig(
                self.response_arrow, state=tk.HIDDEN
            )  # Menyembunyikan panah respons
        self.parent.after(1000, self.check_activity)  # Memeriksa setiap detik

    def check_connection(self):
        url = "http://127.0.0.1:8001/ping"  # URL untuk memeriksa koneksi
        try:
            # Mengirim permintaan uji untuk memeriksa koneksi
            response = requests.get(url)
            if response.ok:
                # Jika respons OK, tampilkan status terkoneksi
                self.status_label.config(text="Server Status: Connected", fg="green")
            else:
                # Jika tidak OK, tampilkan status terputus
                self.status_label.config(text="Server Status: Disconnected", fg="red")
        except requests.exceptions.RequestException:
            # Jika terjadi kesalahan saat menghubungi server, tampilkan status terputus
            self.status_label.config(text="Server Status: Disconnected", fg="red")

        # Ulangi pengecekan koneksi setiap 5 detik
        self.parent.after(5000, self.check_connection)


if __name__ == "__main__":
    root = tk.Tk()  # Membuat instance Tkinter
    root.title("Request Response App")  # Menetapkan judul jendela
    app = RequestResponseApp(root)  # Membuat instance aplikasi
    root.mainloop()  # Memulai loop utama aplikasi
