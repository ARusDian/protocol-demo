import tkinter as tk
from tkinter import ttk
import xmlrpc.client
import threading
import time


class RPCClientApp:
    def __init__(self, parent):
        self.parent = parent
        # Menghubungkan ke server RPC di localhost pada port 8002
        self.rpc_server = xmlrpc.client.ServerProxy("http://localhost:8002")

        # Menyimpan status koneksi server
        self.server_status = False

        # Menyiapkan antarmuka pengguna
        self.setup_ui()

        # Memulai thread untuk memeriksa koneksi server
        self.connection_thread = threading.Thread(
            target=self.connect_to_server, daemon=True
        )
        self.connection_thread.start()

    def connect_to_server(self):
        while True:
            try:
                # Mengirim permintaan ping ke server untuk memeriksa koneksi
                self.rpc_server.ping()  # Mengasumsikan 'ping' adalah metode yang tersedia di server Anda
                self.server_status = True
                # Memperbarui label status koneksi ke 'Connected'
                self.update_status_label("Connected", "green")
                break  # Keluar dari loop jika koneksi berhasil
            except:
                self.server_status = False
                # Memperbarui label status koneksi ke 'Disconnected'
                self.update_status_label("Disconnected, retrying...", "red")
                time.sleep(5)  # Tunggu selama 5 detik sebelum mencoba lagi

    def update_status_label(self, message, color):
        # Memperbarui label status koneksi di antarmuka pengguna
        self.parent.after(0, lambda: self.status_label.config(text=message, fg=color))

    def setup_ui(self):
        # Membuat label dan entri untuk input angka pertama
        self.label_x = tk.Label(self.parent, text="Number 1:")
        self.label_x.pack(pady=5)
        self.entry_x = tk.Entry(self.parent)
        self.entry_x.pack(pady=5)

        # Membuat label dan entri untuk input angka kedua
        self.label_y = tk.Label(self.parent, text="Number 2:")
        self.label_y.pack(pady=5)
        self.entry_y = tk.Entry(self.parent)
        self.entry_y.pack(pady=5)

        # Variabel untuk menentukan operasi yang dipilih oleh pengguna
        self.operation = tk.StringVar(value="add")
        self.dropdown = ttk.Combobox(
            self.parent, textvariable=self.operation, values=["add", "multiply"]
        )
        self.dropdown.pack(pady=5)

        # Tombol untuk mengeksekusi RPC
        self.execute_button = tk.Button(
            self.parent, text="Execute RPC", command=self.start_rpc_thread
        )
        self.execute_button.pack(pady=5)

        # Label untuk menampilkan hasil dari operasi
        self.result_label = tk.Label(self.parent, text="Result:")
        self.result_label.pack(pady=5)

        # Label untuk menunjukkan status koneksi server
        self.status_label = tk.Label(
            self.parent, text="Server Status: Connecting...", fg="orange"
        )
        self.status_label.pack(pady=5)

        # Label untuk menunjukkan loading saat RPC dieksekusi
        self.loading_label = tk.Label(self.parent, text="")
        self.loading_label.pack(pady=5)

        # Kanvas untuk menggambar diagram alir
        self.canvas = tk.Canvas(self.parent, width=400, height=200)
        self.canvas.pack(pady=10)
        # Menggambar diagram alir yang menunjukkan aliran pemanggilan RPC
        self.arrow_id = (
            self.draw_flow_diagram()
        )  # Mendapatkan ID panah untuk digunakan nanti

    def draw_flow_diagram(self):
        # Menggambar diagram alir sederhana pada kanvas untuk menunjukkan aliran RPC
        self.client_arrow = self.canvas.create_line(
            50, 150, 150, 150, arrow=tk.LAST, fill="black"
        )  # Panah yang menunjukkan posisi Klien
        self.canvas.create_text(100, 160, text="Client")

        self.rpc_call_arrow = self.canvas.create_line(
            150, 150, 150, 50, arrow=tk.LAST, fill="black"
        )  # Panah yang menunjukkan pemanggilan RPC
        self.canvas.create_text(160, 100, text="RPC Call")

        self.server_arrow = self.canvas.create_line(
            150, 50, 250, 50, arrow=tk.LAST, fill="black"
        )  # Panah yang menunjukkan posisi Server
        self.canvas.create_text(200, 40, text="Server")

        self.result_arrow = self.canvas.create_line(
            250, 50, 250, 150, arrow=tk.LAST, fill="black"
        )  # Panah yang menunjukkan aliran hasil kembali ke Klien
        self.canvas.create_text(260, 100, text="Result")

        self.client_return_arrow = self.canvas.create_line(
            250, 150, 350, 150, arrow=tk.LAST, fill="black"
        )  # Panah yang menunjukkan hasil yang dikembalikan ke Klien
        self.canvas.create_text(300, 160, text="Client")

        return self.client_arrow  # Mengembalikan ID panah pertama

    def start_rpc_thread(self):
        # Memulai thread baru untuk eksekusi RPC agar tidak menghalangi antarmuka pengguna
        threading.Thread(target=self.execute_rpc, daemon=True).start()

    def execute_rpc(self):
        # Memeriksa apakah server terhubung sebelum melakukan panggilan RPC
        if not self.server_status:
            # Menampilkan pesan kesalahan jika server tidak terhubung
            self.show_error("Cannot execute RPC, server not connected.")
            return

        # Mengganti warna panah untuk menunjukkan bahwa RPC sedang dieksekusi
        self.canvas.itemconfig(self.client_arrow, fill="red")
        time.sleep(0.5)  # Tunggu sejenak untuk visualisasi

        self.loading_label.config(text="Executing...")  # Menampilkan pesan loading

        # Kembalikan warna panah ke normal setelah jeda
        self.canvas.itemconfig(self.client_arrow, fill="black")
        self.canvas.itemconfig(
            self.rpc_call_arrow, fill="red"
        )  # Tandai pemanggilan RPC
        time.sleep(0.5)  # Tunggu sejenak

        try:
            # Mengambil nilai dari entri dan mengubahnya menjadi integer
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())

            self.canvas.itemconfig(
                self.rpc_call_arrow, fill="black"
            )  # Kembalikan warna panah pemanggilan RPC
            self.canvas.itemconfig(self.server_arrow, fill="red")  # Tandai server

            operation = (
                self.operation.get()
            )  # Mengambil jenis operasi yang dipilih pengguna

            # Memanggil metode RPC berdasarkan operasi yang dipilih oleh pengguna
            if operation == "add":
                result = self.rpc_server.add(x, y)  # Panggil metode 'add' di server
            elif operation == "multiply":
                result = self.rpc_server.multiply(
                    x, y
                )  # Panggil metode 'multiply' di server

            # Memperbarui label hasil dengan hasil dari RPC
            self.parent.after(0, self.update_result, result)
        except Exception as e:
            # Menangani kesalahan yang mungkin terjadi selama eksekusi RPC
            self.parent.after(0, self.show_error, str(e))
        finally:
            # Menghapus pesan loading dan mengembalikan warna panah
            self.loading_label.config(text="")  # Menghapus pesan loading
            self.canvas.itemconfig(
                self.server_arrow, fill="black"
            )  # Kembalikan warna panah server
            self.canvas.itemconfig(
                self.result_arrow, fill="red"
            )  # Tandai hasil yang dikembalikan
            time.sleep(0.2)  # Tunggu sejenak
            self.canvas.itemconfig(
                self.result_arrow, fill="black"
            )  # Kembalikan warna panah hasil
            self.canvas.itemconfig(
                self.client_return_arrow, fill="red"
            )  # Tandai panah hasil kembali ke Klien
            time.sleep(0.3)  # Tunggu sejenak
            self.canvas.itemconfig(
                self.client_return_arrow, fill="black"
            )  # Kembalikan warna panah ke normal

    def update_result(self, result):
        # Memperbarui label hasil dengan nilai hasil RPC
        self.result_label.config(text=f"Result: {result}")

    def show_error(self, error):
        # Menampilkan pesan kesalahan jika terjadi masalah saat eksekusi RPC
        self.result_label.config(text="Error executing RPC")


if __name__ == "__main__":
    root = tk.Tk()  # Membuat jendela utama
    root.title("RPC Client")  # Menetapkan judul jendela
    rpc_client_app = RPCClientApp(root)  # Membuat instansi aplikasi klien RPC
    root.mainloop()  # Memulai loop utama untuk antarmuka pengguna
