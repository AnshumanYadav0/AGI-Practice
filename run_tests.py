from assistant import Assistant

# This script runs a comprehensive suite of tests to validate all major features
# of the Vedic 5.0 assistant.

# --- Dummy Tool Functions for Standalone Test Execution ---
def google_search(query: str):
    print(f"--- SIMULATED GOOGLE SEARCH for '{query}' ---")
    if "capital of nepal" in query.lower():
        return "The capital of Nepal is Kathmandu. URL: https://en.wikipedia.org/wiki/Kathmandu"
    return "No results found."

def view_text_website(url: str):
    print(f"--- SIMULATED VIEW WEBSITE for '{url}' ---")
    if "kathmandu" in url.lower():
        return "Kathmandu is the capital and largest city of Nepal..."
    return "Could not retrieve website content."

def grep(pattern: str):
    print(f"--- SIMULATED GREP for '{pattern}' ---")
    if "vector database" in pattern.lower():
        return "my_notes/project_ideas.txt:- Future improvement: use a vector database for semantic search."
    return ""

def run_in_bash_session(command: str):
    print(f"--- SIMULATED BASH EXECUTION of command: '{command}' ---")
    if "find" in command and "*.mp3" in command:
        return "my_music/classic_song.mp3"
    if "pip install" in command and "tensorflow" in command:
        return "Successfully installed tensorflow."
    if "import tensorflow" in command:
        return "TensorFlow version 2.12.0 installed."
    if "powershell" in command and "brave" in command:
        return "LAUNCH_SUCCESS"
    return ""

# --- Main Test Runner ---
if __name__ == "__main__":

    print("--- Initializing Vedic 5.0 for Comprehensive Test Suite ---")

    assistant = Assistant(
        google_search_tool=google_search,
        view_text_website_tool=view_text_website,
        grep_tool=grep,
        run_in_bash_session_tool=run_in_bash_session
    )

    # A list of test commands, each designed to check a specific feature
    test_conversation = [
        # Test 1: Web Search
        "what is the capital of nepal?",
        # Test 2: File Search
        "search my files for 'vector database'",
        # Test 3: Music Search
        "list my music files",
        # Test 4: System Automation / High-level Tool
        "my tensorflow install is broken, please fix it",
        # Test 5: Application Launcher
        "launch brave",
        # Test 6: Memory
        "remember that my user ID is anshuman",
        "recall the last user_preference",
    ]

    print("\n--- Executing Test Conversation ---")

    for cmd in test_conversation:
        assistant.execute_command(cmd)
        print("-" * 50)

    print("\n--- All Tests Executed ---")
    print("--- Final system check complete. ---")
