import sys
import os

# The command queue file must match the one in service.py
COMMAND_QUEUE_FILE = "command_queue.txt"

def send_command(command_string: str):
    """
    Sends a command to the running VedicService by writing to the queue file.
    """
    if os.path.exists(COMMAND_QUEUE_FILE):
        print("Error: A command is already pending. Please wait a moment and try again.")
        return

    with open(COMMAND_QUEUE_FILE, 'w') as f:
        f.write(command_string)

    print(f"Sent command to service: '{command_string}'")

if __name__ == "__main__":
    # Check if a command was provided as a command-line argument
    if len(sys.argv) > 1:
        # Join all arguments to form the command string
        command = " ".join(sys.argv[1:])
        send_command(command)
    else:
        print("Usage: python client.py <your command here>")
        print("Example: python client.py list all my music files")
