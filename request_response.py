import tkinter as tk
import requests
import time
import threading


class RequestResponseApp:
    def __init__(self, parent):
        self.parent = parent
        self.last_activity_time = time.time()  # Initialize last_activity_time here
        self.setup_ui()
        self.create_diagram()

        # Start the activity checker and connection checker
        self.check_activity()
        self.check_connection()

    def setup_ui(self):
        request_username_label = tk.Label(self.parent, text="Username:")
        request_username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.parent)
        self.username_entry.pack(pady=5)

        request_message_label = tk.Label(self.parent, text="Message:")
        request_message_label.pack(pady=5)
        self.message_entry = tk.Entry(self.parent)
        self.message_entry.pack(pady=5)

        request_send_button = tk.Button(
            self.parent, text="Send", command=self.start_request_thread
        )
        request_send_button.pack(pady=20)

        self.response_label = tk.Label(self.parent, text="Response: ")
        self.response_label.pack(pady=10)

        self.latency_label = tk.Label(self.parent, text="")
        self.latency_label.pack(pady=10)

        self.status_label = tk.Label(
            self.parent, text="Server Status: Checking...", fg="orange"
        )
        self.status_label.pack(pady=10)

    def create_diagram(self):
        # Create a canvas for the communication diagram
        self.canvas = tk.Canvas(self.parent, width=400, height=200, bg="white")
        self.canvas.pack(pady=20)

        # Draw the diagram
        self.client_box = self.canvas.create_rectangle(
            50, 50, 150, 100, fill="lightblue"
        )
        self.server_box = self.canvas.create_rectangle(
            250, 50, 350, 100, fill="lightgreen"
        )
        self.canvas.create_text(100, 75, text="Client", font=("Arial", 12))
        self.canvas.create_text(300, 75, text="Server", font=("Arial", 12))

        # Create two arrows for request and response
        self.request_arrow = self.canvas.create_line(
            150, 75, 250, 75, arrow=tk.LAST, fill="lightblue", width=2
        )
        self.response_arrow = self.canvas.create_line(
            250, 75, 150, 75, arrow=tk.FIRST, fill="lightgreen", width=2
        )

        # Initially hide the response arrow
        self.canvas.itemconfig(self.response_arrow, state=tk.HIDDEN)

    def start_request_thread(self):
        threading.Thread(target=self.send_request, daemon=True).start()
        self.last_activity_time = time.time()  # Update last activity time

    def send_request(self):
        username = self.username_entry.get()
        message = self.message_entry.get()
        if not username:
            self.parent.after(0, self.show_error, "Username cannot be empty")
            return

        url = "http://127.0.0.1:8001/chat"
        try:
            self.animate_sending()  # Start animation
            start_time = time.time()
            response = requests.post(
                url, json={"username": username, "message": message}
            )
            server_latency = (time.time() - start_time) * 1000  # Server latency in ms
            data = response.json()
            chatbot_response = data.get("response", "No Response")

            client_latency = f"{(time.time() - start_time) * 1000:.2f} ms"

            self.parent.after(
                0,
                self.update_response,
                chatbot_response,
                f"{server_latency:.2f} ms",
                client_latency,
            )

        except Exception as e:
            self.parent.after(
                0, self.show_error, f"Error connecting to server: {str(e)}"
            )

    def animate_sending(self):
        # hide the response arrow
        self.canvas.itemconfig(self.response_arrow, state=tk.HIDDEN)

        # Animate the request arrow to show message sending
        self.canvas.itemconfig(self.request_arrow, fill="blue")
        self.canvas.after(
            100, lambda: self.canvas.itemconfig(self.request_arrow, fill="lightblue")
        )

    def animate_response(self):
        # hide the request arrow
        self.canvas.itemconfig(self.request_arrow, state=tk.HIDDEN)

        # Show the response arrow and animate it
        self.canvas.itemconfig(
            self.response_arrow, state=tk.NORMAL
        )  # Show the response arrow
        self.canvas.itemconfig(
            self.response_arrow, fill="green"
        )  # Change color to green
        self.canvas.after(
            100, lambda: self.canvas.itemconfig(self.response_arrow, fill="lightgreen")
        )  # Return to original color

    def update_response(self, chatbot_response, server_latency, client_latency):
        self.animate_response()  # Animate the response arrow
        self.response_label.config(text=f"Response: {chatbot_response}")
        self.latency_label.config(
            text=f"Server Latency: {server_latency} | Client Latency: {client_latency}"
        )
        self.last_activity_time = time.time()  # Update last activity time

    def show_error(self, error):
        self.response_label.config(text="Error connecting to server")
        self.latency_label.config(text="")
        self.last_activity_time = time.time()  # Update last activity time

    def check_activity(self):
        # Check if there's been no activity for a while
        if time.time() - self.last_activity_time > 3:  # 3 seconds timeout
            self.canvas.itemconfig(
                self.request_arrow, state=tk.HIDDEN
            )  # Hide the request arrow
            self.canvas.itemconfig(
                self.response_arrow, state=tk.HIDDEN
            )  # Hide the response arrow
        self.parent.after(1000, self.check_activity)  # Check every second

    def check_connection(self):
        url = "http://127.0.0.1:8001/ping"
        try:
            # Send a test request to check the connection
            response = requests.get(url)
            if response.ok:
                self.status_label.config(text="Server Status: Connected", fg="green")
            else:
                self.status_label.config(text="Server Status: Disconnected", fg="red")
        except requests.exceptions.RequestException:
            self.status_label.config(text="Server Status: Disconnected", fg="red")

        # Repeat the connection check every 5 seconds
        self.parent.after(5000, self.check_connection)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Request Response App")
    app = RequestResponseApp(root)
    root.mainloop()
