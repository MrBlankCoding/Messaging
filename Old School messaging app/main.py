import tkinter as tk
from tkinter import ttk, Menu, messagebox, filedialog, simpledialog
import datetime
import random
from tkinter import PhotoImage
import os

# Set the environment variable to use the "dummy" audio driver
os.environ['SDL_AUDIODRIVER'] = 'dummy'


# Create a class to manage the logic of the Message App
class MessageAppLogic:
    def __init__(self, filename, password):
        # Set the environment variable to use the "dummy" audio driver
        os.environ['SDL_AUDIODRIVER'] = 'dummy'


        self.filename = filename
        self.messages = []
        self.root = root
        self.root.title("Message App")
        self.root.geometry("400x400")
        self.password = password  # Store the password

        # Modern style configuration
        self.style = ttk.Style()
        self.style.theme_use("default")  # Use the default theme

        # Set a modern color scheme
        self.style.configure("TFrame", background="#f2f2f2")  # Light gray background
        self.style.configure("TLabel", background="#f2f2f2", font=("Helvetica", 12))  # Label style
        self.style.configure("TButton", background="#007acc", foreground="white", font=("Helvetica", 12))  # Button style
        self.style.map("TButton", background=[("active", "#0055a4")])  # Button hover color
        self.style.configure("TText", font=("Helvetica", 12))  # Text widget style

    # Function to save a message to a file
    def save_message(self, name, message):
        formatted_message = f"{name}: {message}"
        self.messages.append(formatted_message)
        with open(self.filename, "a") as file:
            file.write(formatted_message + "\n")

    # Function to load messages from a file
    def load_messages(self):
        try:
            with open(self.filename, "r") as file:
                self.messages = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.messages = []

    # Function to get messages
    def get_messages(self):
        return self.messages

    # Function to create the menu bar
    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0, font=("Helvetica", 16))
        menubar.add_cascade(label="File", menu=file_menu)

        # Add icons to the menu items
        file_menu.add_command(label="Open", compound="left", command=self.open_file)
        file_menu.add_command(label="Save", compound="left", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", compound="left", command=self.confirm_exit)

    # Function to verify the password before opening the chat
    def verify_password(self):
        entered_password = simpledialog.askstring("Password", "Enter the password:", show='*')
        return entered_password == self.password

    # Function to open a message file
    def open_file(self):
        if self.verify_password():  # Verify the password before opening the chat
            file_path = filedialog.askopenfilename(title="Open Message File", filetypes=[("Text files", "*.txt")])
            if file_path:
                self.filename = file_path  # Update the filename
                self.load_and_print_messages()
        else:
            messagebox.showwarning("Invalid Password", "Incorrect password. Please try again.")

    # Function to save messages to a file
    def save_file(self):
        file_path = filedialog.asksaveasfilename(title="Save Message File", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write('\n'.join(self.messages))

# Create a class to manage the user interface of the Message App
class MessageAppUI:
    def __init__(self, root, logic):
        self.sender_colors = {}
        self.root = root
        self.logic = logic

        self.root.title("Message App")
        self.root.geometry("400x400")
        self.logic = logic

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.create_menu()
        self.create_input_frame()
        self.create_message_frame()
        self.create_status_bar()
        self.message_entry.focus_set()
        self.load_and_print_messages()
        self.display_timestamp()

    # Function to create the menu bar
    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.confirm_exit)

    # Function to create the input frame
    def create_input_frame(self):
        input_frame = ttk.Frame(self.root, padding=(10, 10))
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.name_label = ttk.Label(input_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky=tk.W)

        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        self.message_label = ttk.Label(input_frame, text="Message:")
        self.message_label.grid(row=1, column=0, sticky=tk.W)

        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        send_button = ttk.Button(input_frame, text="Send Message", command=self.get_user_input)
        send_button.grid(row=2, columnspan=2, pady=(10, 0))

    # Function to create the message display frame
    def create_message_frame(self):
        message_frame = ttk.Frame(self.root, padding=(10, 10))
        message_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.timestamp_label = ttk.Label(message_frame, text="", anchor=tk.W)
        self.timestamp_label.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.messages_text = tk.Text(message_frame, height=10, width=40, wrap=tk.WORD)
        self.messages_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.messages_text.config(state=tk.DISABLED)

    # Function to create the status bar
    def create_status_bar(self):
        status_frame = ttk.Frame(self.root, padding=(10, 0))
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

        self.status_label = ttk.Label(status_frame, text="", anchor=tk.W)
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Function to get user input and save a message
    def get_user_input(self):
        name = self.name_entry.get()
        message = self.message_entry.get()
        if name and message:
            self.logic.save_message(name, message)
            self.message_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.status_label.config(text="Message saved!", foreground="green")
        self.load_and_print_messages()

    # Function to load and print messages
    def load_and_print_messages(self):
        self.logic.load_messages()
        messages = self.logic.get_messages()
        self.messages_text.config(state=tk.NORMAL)
        self.messages_text.delete(1.0, tk.END)
        if messages:
            for message in messages:
                self.add_message_to_text_widget(message)
        else:
            self.messages_text.insert(tk.END, "No messages to display.")
        self.messages_text.config(state=tk.DISABLED)
        self.scroll_to_latest_message()

    # Function to add a message to the text widget
    def add_message_to_text_widget(self, message):
        parts = message.split(" - ", 1) if " - " in message else (None, message)
        if parts:
            timestamp, content = parts
            if timestamp:
                self.messages_text.insert(tk.END, timestamp + " - ", "timestamp")

            if content:
                sender_name, message_text = content.split(":", 1)
                sender_name = sender_name.strip()
                message_text = message_text.strip()

                # Check if the sender already has a color assigned
                if sender_name in self.sender_colors:
                    sender_color = self.sender_colors[sender_name]
                else:
                    # Generate a random color
                    sender_color = "#{:02x}{:02x}{:02x}".format(
                        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                    )
                    # Store the color in the dictionary
                    self.sender_colors[sender_name] = sender_color

                # Apply the sender's color to the message text
                self.messages_text.tag_configure(sender_name, foreground=sender_color)
                self.messages_text.insert(tk.END, sender_name + ":", sender_name)
                self.messages_text.insert(tk.END, message_text + "\n", "message")

    # Function to scroll to the latest message
    def scroll_to_latest_message(self):
        self.messages_text.see(tk.END)

    # Function to display the timestamp
    def display_timestamp(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=f"Messages as of {timestamp}")

    # Function to confirm exit
    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    # Function to open a message file
    def open_file(self):
        file_path = filedialog.askopenfilename(title="Open Message File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.logic = MessageAppLogic(file_path)
            self.load_and_print_messages()

    # Function to save messages to a file
    def save_file(self):
        file_path = filedialog.asksaveasfilename(title="Save Message File", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write('\n'.join(self.logic.get_messages()))

if __name__ == "__main__":
  root = tk.Tk()
  password = "your_password"  # Set your desired password
  app_logic = MessageAppLogic("messages.txt", password)
  app_ui = MessageAppUI(root, app_logic)
  root.mainloop()
