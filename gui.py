import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame
from assistant import Assistant
import speech_recognition as sr
import threading

class VedicApp(tk.Tk):
    """
    A Tkinter GUI for the Vedic 2.0 Assistant with Voice Input.
    """
    def __init__(self):
        super().__init__()

        self.title("Vedic 4.0 Assistant")
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

        # --- Initialize Assistant ---
        # The assistant will use its internal dummy tools since we are not passing any.
        self.assistant = Assistant(logger=self.log_to_gui)
        self.log_to_gui("Vedic 4.0 (Tool-Using Agent) initialized. Please enter a command or press 'Speak'.")

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
        """Gets command from input box and executes it in a new thread."""
        command_text = self.input_box.get()
        if not command_text:
            return
        self.input_box.delete(0, tk.END)
        # Run assistant in a thread to avoid freezing the GUI
        threading.Thread(target=self.assistant.execute_command, args=(command_text,)).start()

    def listen_for_command(self):
        """Listens for a voice command in a new thread."""
        self.speak_button.config(state='disabled', text="Listening...")
        self.log_to_gui("\n[Voice] Listening for your command...")
        threading.Thread(target=self._recognize_speech).start()

    def _recognize_speech(self):
        """Handles the speech recognition process."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.log_to_gui("[Voice] Recognizing speech...")

                # Use Google Web Speech API
                text = recognizer.recognize_google(audio)
                self.log_to_gui(f"[Voice] You said: \"{text}\"")

                # Put recognized text in the input box and execute
                self.input_box.delete(0, tk.END)
                self.input_box.insert(0, text)
                self.send_command()

            except sr.WaitTimeoutError:
                self.log_to_gui("[Voice] Error: No speech detected. Please try again.")
            except sr.UnknownValueError:
                self.log_to_gui("[Voice] Error: Could not understand the audio. Please speak clearly.")
            except sr.RequestError as e:
                self.log_to_gui(f"[Voice] Error: Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                self.log_to_gui(f"[Voice] An unexpected error occurred: {e}")
            finally:
                # Re-enable the speak button
                self.speak_button.config(state='normal', text="Speak")


if __name__ == "__main__":
    print("GUI script created. To run, execute 'python gui.py' on a desktop system with a microphone.")
    # The following lines are commented out to prevent crashing in the sandbox.
    # app = VedicApp()
    # app.mainloop()
