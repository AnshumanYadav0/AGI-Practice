import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame
import speech_recognition as sr
import threading
from client import send_command # Import the client's send_command function

class VedicApp(tk.Tk):
    """
    A Tkinter GUI Client for the Vedic 5.0 Assistant Service.
    """
    def __init__(self):
        super().__init__()

        self.title("Vedic 5.0 Client")
        self.geometry("750x550")

        # --- Main Frame ---
        main_frame = Frame(self)
        main_frame.pack(padx=10, pady=10, expand=True, fill='both')

        # --- Widgets ---
        self.output_box = scrolledtext.Text(main_frame, state='disabled', wrap=tk.WORD, bg="#2b2b2b", fg="white", font=("Consolas", 10))

        self.input_box = Entry(main_frame, bg="#404040", fg="white", font=("Consolas", 11), insertbackground='white')
        self.input_box.bind("<Return>", self.send_command_event)

        # Frame for buttons
        button_frame = Frame(main_frame)
        self.send_button = Button(button_frame, text="Send", command=self.send_command, bg="#555", fg="white", width=10)
        self.speak_button = Button(button_frame, text="Speak", command=self.listen_for_command, bg="#007acc", fg="white", width=10)

        # --- Layout ---
        self.output_box.pack(expand=True, fill='both')
        self.input_box.pack(pady=5, fill='x')
        button_frame.pack(fill='x')
        self.send_button.pack(side='right', padx=2)
        self.speak_button.pack(side='right')

        self.log_to_gui("Vedic 5.0 Client initialized.")
        self.log_to_gui("NOTE: The main service must be running in a separate terminal (`py service.py`).")
        self.log_to_gui("This window is for sending commands. Detailed logs will appear in the service terminal.")

    def log_to_gui(self, message):
        """Thread-safe method to append a message to the GUI's output box."""
        def append():
            self.output_box.config(state='normal')
            self.output_box.insert(tk.END, str(message) + "\n")
            self.output_box.config(state='disabled')
            self.output_box.see(tk.END)
        self.after(0, append)

    def send_command_event(self, event=None):
        self.send_command()

    def send_command(self):
        """Gets command from input box and sends it to the service via the client logic."""
        command_text = self.input_box.get()
        if not command_text:
            return

        self.log_to_gui(f"\n> Sending command: '{command_text}'")
        send_command(command_text) # Use the imported client function
        self.input_box.delete(0, tk.END)

    def listen_for_command(self):
        """Listens for a voice command in a new thread."""
        self.speak_button.config(state='disabled', text="Listening...")
        self.log_to_gui("\n[Voice] Listening...")
        threading.Thread(target=self._recognize_speech).start()

    def _recognize_speech(self):
        """Handles the speech recognition process."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.log_to_gui("[Voice] Recognizing...")

                text = recognizer.recognize_google(audio)
                self.log_to_gui(f"[Voice] Heard: \"{text}\"")

                # Place recognized text in the input box and send it
                self.input_box.delete(0, tk.END)
                self.input_box.insert(0, text)
                self.send_command()

            except Exception as e:
                self.log_to_gui(f"[Voice] Error: {e}")
            finally:
                self.speak_button.config(state='normal', text="Speak")


if __name__ == "__main__":
    app = VedicApp()
    app.mainloop()
