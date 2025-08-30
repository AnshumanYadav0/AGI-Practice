# Vedic 2.0 - High-Level Architecture

This document outlines the architectural design for Vedic 2.0, a voice-controlled assistant capable of operating desktop applications and system functions.

## Core Components

The system is designed with a modular approach, consisting of five main components:

![Architecture Diagram](https_placehold.co/800x400?text=Vedic%202.0%20Architecture\nVoice%20Input%20-%3E%20Command%20Parser%20-%3E%20Decision%20Engine%20-%3E%20Action%20Dispatcher%20-%3E%20App/OS)

### 1. Voice Input (Speech-to-Text)

*   **Purpose:** To capture the user's voice commands and convert them into plain text.
*   **Technology:** This can be implemented using Python libraries like `SpeechRecognition` which supports various APIs (Google Web Speech API, Sphinx, etc.).
*   **Process:**
    1.  The microphone constantly listens for a wake word (e.g., "Vedic").
    2.  Upon detecting the wake word, it starts recording the command.
    3.  The recorded audio is sent to a Speech-to-Text (STT) engine.
    4.  The STT engine returns the transcribed text of the command.
*   **Output:** A string containing the user's command (e.g., `"autocad में 100 by 200 का rectangle बनाओ"`).

### 2. Command Parser (Natural Language Understanding - NLU)

*   **Purpose:** This is the "brain" of the assistant. It takes the raw text command and extracts structured, actionable information from it.
*   **Technology:** A combination of regular expressions (for simple patterns) and keyword matching. For more advanced capabilities, NLP libraries like `spaCy` or `NLTK` could be used.
*   **Process:**
    1.  Receives the text string from the Voice Input component.
    2.  Identifies the **target application** (e.g., `AutoCAD`, `QGIS`, `Windows OS`).
    3.  Identifies the **intent** or **action** (e.g., `create_rectangle`, `create_shapefile`, `open_file`).
    4.  Extracts the necessary **entities** or **parameters** (e.g., `(100, 200)`, `"Agra"`, `"my_document.txt"`).
*   **Output:** A structured object, like a Python dictionary:
    ```json
    {
      "application": "autocad",
      "action": "create_rectangle",
      "parameters": { "width": 100, "height": 200 }
    }
    ```

### 3. Decision Engine

*   **Purpose:** To take the parsed command and decide which specific module or script to execute.
*   **Technology:** A simple dispatcher or a mapping (e.g., a Python dictionary) that connects parsed applications/actions to their corresponding controller functions.
*   **Process:**
    1.  Receives the structured object from the Command Parser.
    2.  Uses the `application` key to look up the correct controller (e.g., `autocad_controller`).
    3.  Prepares to call the function corresponding to the `action` within that controller.
*   **Output:** A function call to the appropriate controller.

### 4. Action Dispatcher & Application Controllers

*   **Purpose:** This component executes the command by interacting with the target application or operating system.
*   **Technology:** This is highly dependent on the target application.
    *   **AutoCAD:** The `pyautocad` library can be used to script a running AutoCAD instance on Windows.
    *   **QGIS:** The `qgis.core` library (PyQGIS) allows for scripting within QGIS.
    *   **Operating System:** Python's built-in `os` and `subprocess` modules can be used to handle files, open applications, etc.
*   **Process:**
    1.  The Decision Engine calls a function in the relevant controller (e.g., `autocad_controller.create_rectangle(width=100, height=200)`).
    2.  This function contains the specific code to interact with the application's API or command-line interface.
    3.  It translates the abstract action into concrete API calls.
*   **Output:** The command is executed in the target application.

### 5. Voice Output (Text-to-Speech)

*   **Purpose:** To provide feedback to the user, confirming that the command has been executed or reporting an error.
*   **Technology:** Python libraries like `gTTS` (Google Text-to-Speech) or `pyttsx3`.
*   **Process:**
    1.  After the action is performed, the controller can return a status message (e.g., "Rectangle created successfully").
    2.  This message is sent to the Text-to-Speech (TTS) engine.
    3.  The TTS engine converts the text into speech, which is then played through the speakers.
*   **Output:** Spoken feedback to the user.

## Advanced Language Support (Future Scope)

The current architecture (as of Vedic 3.0) uses a powerful translation-based model to understand multiple languages. It translates a foreign language command into English and then parses the English text. While this works well for many common languages, achieving near-perfect understanding for specific dialects (e.g., rural or regional Hindi) and low-resource languages (like Sanskrit) requires a dedicated effort.

This is a significant machine learning project that goes beyond standard software development. The key steps to implement this would be:

1.  **Data Collection:**
    *   Gather thousands of text samples of commands in the target language or dialect. For example, recording or writing down many variations of "100 by 200 का एक आयत बनाएं" in different rural dialects.
    *   This data needs to be annotated, meaning each command is paired with its structured representation (e.g., `{"action": "create_rectangle", "parameters": ...}`).

2.  **Custom Model Training (Fine-Tuning):**
    *   Choose a large, pre-trained multilingual language model (e.g., from the Hugging Face model hub).
    *   Use the collected, annotated data to "fine-tune" this model. This process adjusts the model's parameters to make it an expert in understanding the specific commands and nuances of the target dialect.

3.  **Integration:**
    *   The fine-tuned model would be hosted (either locally or on a server) and integrated into the Vedic assistant, replacing the generic translation step for that specific language.

This process requires significant expertise in machine learning and data engineering and represents a major evolution for the project, effectively becoming "Vedic 4.0".

## Personalized Knowledge Base (Future Scope)

Beyond searching the public internet, a truly personal assistant must learn from the user's own data, such as local text files, documents, and notes. This would allow Vedic to answer questions like, "What were my meeting notes about Project X?" or "Summarize my research on topic Y."

Building this feature can be approached in two phases:

### Phase 1: Simple Keyword-Based File Search

The most straightforward initial step is to enable keyword searching across a user-defined directory of notes.

*   **Action:** A new action, such as `find_notes_on("topic")`, would be added.
*   **Controller:** A new `notes_controller.py` would be created.
*   **Implementation:** This controller would use system tools like `grep` to perform a text search for the "topic" string within all `.txt` or `.md` files in a specified notes folder. It would then return the matching lines or file snippets.

This approach is simple and powerful for basic retrieval but lacks a deep understanding of the content.

### Phase 2: Semantic Search with a Vector Database (RAG)

For true contextual understanding, the assistant needs to search by meaning, not just keywords. This is a more advanced data science task known as Retrieval-Augmented Generation (RAG).

1.  **Indexing & Embedding:**
    *   A background process would be created to monitor a notes directory.
    *   When files are added or changed, the process would read them, split them into small chunks of text (e.g., paragraphs).
    *   Each chunk would be passed to an AI embedding model (e.g., from `spaCy`, `Hugging Face`, or OpenAI) to be converted into a numerical vector. This vector represents the semantic "meaning" of the text.

2.  **Vector Database:**
    *   These vectors, along with their corresponding text chunks, would be stored in a specialized vector database (e.g., FAISS, ChromaDB). This type of database is optimized for finding similar vectors very quickly.

3.  **Retrieval:**
    *   When the user asks a question (e.g., "What was my idea about improving the GUI?"), the question itself is converted into a vector.
    *   The system then queries the vector database to find the text chunks with the most similar vectors.
    *   These relevant chunks are provided to the assistant as context to generate a precise, informed answer.

Implementing a RAG system is a significant step that would give Vedic a powerful, personalized memory, making it an incredibly useful knowledge management tool.

## System Automation (Future Scope)

### Autonomous Application Installation

A key feature of a true system manager is the ability to install new software on behalf of the user. This is a powerful but high-risk capability that requires a careful, security-first approach.

The ideal implementation would leverage modern package managers, as they provide a trusted and scriptable way to handle software installation.

1.  **The Workflow:**
    *   **User Command:** "Vedic, install the VLC media player."
    *   **LLM Chooses Tool:** The AI 'brain' would choose a new high-level tool, for example, `install_windows_application`. The parameter would be `app_name="VLC media player"`.
    *   **Search Step:** The `install_windows_application` tool would first use the `run_bash_command` tool to search for the application in the package manager's repository. For Windows, this would be `winget search "VLC media player"`.
    *   **Parsing Step:** The tool would parse the output of the search command to find the exact Package ID (e.g., `VideoLAN.VLC`).
    *   **Confirmation Step (Crucial):** Before proceeding, the tool would confirm with the user: "I found VLC media player with the ID 'VideoLAN.VLC'. Shall I proceed with the installation?"
    *   **Execution Step:** Upon confirmation, the tool would use `run_bash_command` again to execute the installation command: `winget install -e --id VideoLAN.VLC`.

2.  **Security and Reliability:**
    *   Using a package manager like `winget` (for Windows) or `apt` (for Debian/Linux) is much safer than searching the web for a `.exe` file, which could lead to malware.
    *   The confirmation step is essential to ensure the agent does not perform major system changes without the user's explicit consent.

This feature would dramatically enhance the assistant's role as a system troubleshooter and manager.
