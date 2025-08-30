import json
from typing import Callable

class SearchFilesTool:
    """A tool to search for a topic across all user-indexed directories."""
    name = "search_files_for_topic"
    description = "Performs a case-insensitive keyword search for a given `topic` across all user-configured directories (documents, notes, etc.)."

    def __init__(self, logger: Callable = print, grep_tool: Callable = None):
        self.logger = logger
        self.grep_tool = grep_tool

    def use(self, topic: str):
        self.logger(f"--- File Search Tool: Searching for '{topic}' ---")

        if not self.grep_tool:
            self.logger("ERROR: Grep tool was not provided to the file search tool.")
            return "Sorry, the file search tool is not available at the moment."

        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
            # Read the list of directories to search
            indexed_dirs = config.get("indexed_directories", [])

            if not indexed_dirs:
                return "Configuration Error: No directories are configured for searching. Please update `config.json`."

            self.logger(f"Searching for '{topic}' in directories: {indexed_dirs}")

            # The grep tool searches the whole repo, so we search for the topic once
            # and then filter the results to see if they are in any of the indexed directories.
            search_results = self.grep_tool(pattern=topic)

            all_filtered_results = []
            for line in search_results.splitlines():
                # Check if the line belongs to any of the indexed directories
                if any(line.startswith(dir_path) for dir_path in indexed_dirs):
                    all_filtered_results.append(line)

            if not all_filtered_results:
                self.logger(f"No files found containing '{topic}'.")
                return f"I couldn't find any files in your indexed directories mentioning '{topic}'."

            self.logger(f"Found {len(all_filtered_results)} matching lines across all directories.")
            return "I found the following matches in your files:\n" + "\n".join(all_filtered_results)

        except FileNotFoundError:
            self.logger("ERROR: config.json not found.")
            return "Configuration Error: The `config.json` file was not found."
        except Exception as e:
            self.logger(f"An error occurred during file search: {e}")
            return "I'm sorry, an unexpected error occurred while searching your files."


class ListMusicFilesTool:
    """A tool to find and list all music files in the indexed directories."""
    name = "list_music_files"
    description = "Searches all configured directories to find and list all audio files (e.g., .mp3, .flac, .wav)."

    def __init__(self, logger: Callable = print, bash_tool: Callable = None):
        self.logger = logger
        self.bash_tool = bash_tool

    def use(self):
        self.logger("--- Music Finder Tool: Searching for audio files ---")

        if not self.bash_tool:
            self.logger("ERROR: Bash tool was not provided to the music finder tool.")
            return "Sorry, the file search tool is not available at the moment."

        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
            indexed_dirs = config.get("indexed_directories", [])

            if not indexed_dirs:
                return "Configuration Error: No directories are configured for searching."

            self.logger(f"Searching for music in: {indexed_dirs}")

            # Construct a find command to search for multiple file types
            # e.g., find my_notes my_music -type f \( -name "*.mp3" -o -name "*.flac" \)
            path_string = " ".join(indexed_dirs)
            find_command = f'find {path_string} -type f \\( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" \\)'

            search_results = self.bash_tool.use(command=find_command)

            if not search_results.strip():
                self.logger("No music files found.")
                return "I couldn't find any music files in your indexed directories."

            self.logger(f"Found music files.")
            return "I found the following music files:\n" + search_results.strip()

        except FileNotFoundError:
            self.logger("ERROR: config.json not found.")
            return "Configuration Error: The `config.json` file was not found."
        except Exception as e:
            self.logger(f"An error occurred during music search: {e}")
            return "I'm sorry, an unexpected error occurred while searching for your music."
