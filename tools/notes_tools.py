import json
from typing import Callable

class SearchNotesTool:
    """A tool to search for a topic in the user's local notes directory."""
    name = "search_personal_notes"
    description = "Performs a case-insensitive keyword search for a given `topic` within all text files (.txt, .md) in the user's configured notes folder."

    def __init__(self, logger: Callable = print, grep_tool: Callable = None):
        self.logger = logger
        self.grep_tool = grep_tool

    def use(self, topic: str):
        self.logger(f"--- Notes Tool: Searching notes for '{topic}' ---")

        if not self.grep_tool:
            self.logger("ERROR: Grep tool was not provided to the notes tool.")
            return "Sorry, the notes search tool is not available at the moment."

        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
            notes_dir = config.get("notes_directory", ".")

            self.logger(f"Searching in directory: {notes_dir}")

            # The provided grep tool searches the whole repository.
            # We must filter the results to only include matches from the notes directory.
            search_results = self.grep_tool(pattern=topic)

            filtered_results = []
            for line in search_results.splitlines():
                # Ensure the line starts with the notes directory path
                if line.startswith(notes_dir):
                    filtered_results.append(line)

            if not filtered_results:
                self.logger(f"No notes found containing '{topic}'.")
                return f"I couldn't find any notes mentioning '{topic}'."

            self.logger(f"Found {len(filtered_results)} matching lines.")
            return "I found the following notes:\n" + "\n".join(filtered_results)

        except FileNotFoundError:
            self.logger("ERROR: config.json not found.")
            return "Configuration Error: The `config.json` file was not found. I don't know where your notes are."
        except Exception as e:
            self.logger(f"An error occurred during note search: {e}")
            return "I'm sorry, an unexpected error occurred while searching your notes."
