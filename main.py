from assistant import Assistant

# --- Tool Definitions (Dummies for standalone execution) ---
# In a real environment, these would be the actual, imported tool functions.
def google_search(query: str):
    print(f"--- SIMULATED GOOGLE SEARCH for '{query}' ---")
    if "capital of mongolia" in query.lower():
        return "Capital of Mongolia is Ulaanbaatar. URL: https://en.wikipedia.org/wiki/Ulaanbaatar"
    if "vector database" in query.lower():
        return "A vector database is a database that stores data as high-dimensional vectors... URL: https://en.wikipedia.org/wiki/Vector_database"
    return "No results found."

def view_text_website(url: str):
    print(f"--- SIMULATED VIEW WEBSITE for '{url}' ---")
    if "ulaanbaatar" in url.lower():
        return "Ulaanbaatar is the capital and largest city of Mongolia..."
    return "Could not retrieve website content."

def grep(pattern: str):
    print(f"--- SIMULATED GREP for '{pattern}' ---")
    if "vector database" in pattern:
        return "my_notes/project_ideas.txt:- Future improvement: use a vector database for semantic search."
    return ""

def run_in_bash_session(command: str):
    print(f"--- SIMULATED BASH EXECUTION of command: '{command}' ---")
    if "pip install" in command:
        return "Successfully installed tensorflow."
    if "import tensorflow" in command:
        return "TensorFlow version 2.12.0 installed."
    if "ls -l" in command:
        return "total 8\n-rw-r--r-- 1 user group 1024 Aug 28 15:20 main.py\n-rw-r--r-- 1 user group 512 Aug 28 15:12 config.json"
    return ""


if __name__ == "__main__":

    # 1. Initialize the Assistant, injecting the dummy tool functions.
    assistant = Assistant(
        google_search_tool=google_search,
        view_text_website_tool=view_text_website,
        grep_tool=grep,
        run_in_bash_session_tool=run_in_bash_session
    )

    print("--- Starting Vedic 4.2 Final Refined Simulation ---")

    # 2. Define a conversation to test the new architecture
    conversation = [
        "remind me to call Anshuman tomorrow at 5pm about the Agra Zone project",
        "recall the last reminder",
        "fix my tensorflow installation please",
        "what is a vector database?",
    ]

    # 3. Loop through commands and execute them
    for cmd in conversation:
        assistant.execute_command(cmd)
        print("-" * 50)

    print("--- Simulation Finished ---")
