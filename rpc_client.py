import tkinter as tk
from tkinter import ttk
import xmlrpc.client
import threading
import time


class RPCClientApp:
    def __init__(self, parent):
        self.parent = parent
        self.rpc_server = xmlrpc.client.ServerProxy("http://localhost:8002")

        # Set initial connection status
        self.server_status = False

        # Set up UI components
        self.setup_ui()

        # Start the connection thread
        self.connection_thread = threading.Thread(
            target=self.connect_to_server, daemon=True
        )
        self.connection_thread.start()

    def connect_to_server(self):
        while True:
            try:
                # Attempt to ping the server
                self.rpc_server.ping()  # Assuming 'ping' is a method available on your server
                self.server_status = True
                self.update_status_label("Connected", "green")
                break  # Exit loop if connection is successful
            except:
                self.server_status = False
                self.update_status_label("Disconnected, retrying...", "red")
                time.sleep(5)  # Wait for 5 seconds before retrying

    def update_status_label(self, message, color):
        self.parent.after(0, lambda: self.status_label.config(text=message, fg=color))

    def setup_ui(self):
        self.label_x = tk.Label(self.parent, text="Number 1:")
        self.label_x.pack(pady=5)
        self.entry_x = tk.Entry(self.parent)
        self.entry_x.pack(pady=5)

        self.label_y = tk.Label(self.parent, text="Number 2:")
        self.label_y.pack(pady=5)
        self.entry_y = tk.Entry(self.parent)
        self.entry_y.pack(pady=5)

        self.operation = tk.StringVar(value="add")
        self.dropdown = ttk.Combobox(
            self.parent, textvariable=self.operation, values=["add", "multiply"]
        )
        self.dropdown.pack(pady=5)

        self.execute_button = tk.Button(
            self.parent, text="Execute RPC", command=self.start_rpc_thread
        )
        self.execute_button.pack(pady=5)

        self.result_label = tk.Label(self.parent, text="Result:")
        self.result_label.pack(pady=5)

        # Status Label
        self.status_label = tk.Label(
            self.parent, text="Server Status: Connecting...", fg="orange"
        )
        self.status_label.pack(pady=5)

        # Loading Indicator
        self.loading_label = tk.Label(self.parent, text="")
        self.loading_label.pack(pady=5)

        # Canvas for flow diagram
        self.canvas = tk.Canvas(self.parent, width=400, height=200)
        self.canvas.pack(pady=10)
        self.arrow_id = (
            self.draw_flow_diagram()
        )  # Get the ID of the arrow for later use

    def draw_flow_diagram(self):
        # Drawing a simple flow diagram on the canvas
        self.client_arrow = self.canvas.create_line(
            50, 150, 150, 150, arrow=tk.LAST, fill="black"
        )  # Arrow 1
        self.canvas.create_text(100, 160, text="Client")

        self.rpc_call_arrow = self.canvas.create_line(
            150, 150, 150, 50, arrow=tk.LAST, fill="black"
        )  # Arrow 2
        self.canvas.create_text(160, 100, text="RPC Call")

        self.server_arrow = self.canvas.create_line(
            150, 50, 250, 50, arrow=tk.LAST, fill="black"
        )  # Arrow 3
        self.canvas.create_text(200, 40, text="Server")

        self.result_arrow = self.canvas.create_line(
            250, 50, 250, 150, arrow=tk.LAST, fill="black"
        )  # Arrow 4
        self.canvas.create_text(260, 100, text="Result")

        self.client_return_arrow = self.canvas.create_line(
            250, 150, 350, 150, arrow=tk.LAST, fill="black"
        )  # Arrow 5
        self.canvas.create_text(300, 160, text="Client")

        return self.client_arrow  # Return the ID of the first arrow

    def start_rpc_thread(self):
        threading.Thread(target=self.execute_rpc, daemon=True).start()

    def execute_rpc(self):
        if not self.server_status:
            self.show_error("Cannot execute RPC, server not connected.")
            return

        # Highlight the arrow before executing RPC
        self.canvas.itemconfig(self.client_arrow, fill="red")
        time.sleep(0.5)
        self.loading_label.config(text="Executing...")

        self.canvas.itemconfig(self.client_arrow, fill="black")
        self.canvas.itemconfig(self.rpc_call_arrow, fill="red")
        time.sleep(0.5)

        try:
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())

            self.canvas.itemconfig(self.rpc_call_arrow, fill="black")
            self.canvas.itemconfig(self.server_arrow, fill="red")
            operation = self.operation.get()

            if operation == "add":
                result = self.rpc_server.add(x, y)
            elif operation == "multiply":
                result = self.rpc_server.multiply(x, y)
            self.parent.after(0, self.update_result, result)
        except Exception as e:
            self.parent.after(0, self.show_error, str(e))
        finally:
            self.loading_label.config(text="")  # Clear loading message
            self.canvas.itemconfig(self.server_arrow, fill="black")
            self.canvas.itemconfig(self.result_arrow, fill="red")
            time.sleep(0.2)
            self.canvas.itemconfig(self.result_arrow, fill="black")
            self.canvas.itemconfig(self.client_return_arrow, fill="red")
            time.sleep(0.3)
            self.canvas.itemconfig(self.client_return_arrow, fill="black")

    def update_result(self, result):
        self.result_label.config(text=f"Result: {result}")

    def show_error(self, error):
        self.result_label.config(text="Error executing RPC")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RPC Client")
    rpc_client_app = RPCClientApp(root)
    root.mainloop()
