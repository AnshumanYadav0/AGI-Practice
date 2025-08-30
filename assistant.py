import json
from tools.tool_registry import get_all_tools, get_formatted_tool_descriptions
import database # Keep this for init

# --- Tool Definitions (Dummies for standalone execution) ---
# ... (dummies remain the same) ...
def _dummy_google_search(query: str): return f"Dummy search result for '{query}' with URL: https://example.com"
def _dummy_view_website(url: str): return f"Dummy content for website: {url}"
def _dummy_grep(pattern: str): return f"Dummy grep result for pattern '{pattern}'"
def _dummy_run_bash(command: str): return f"Dummy execution of command: '{command}'"

class Assistant:
    """
    The Vedic 4.5 assistant: a tool-using agent that can search files and learn.
    """
    def __init__(self, logger=print, google_search_tool=None, view_text_website_tool=None, grep_tool=None, run_in_bash_session_tool=None):
        self.logger = logger
        self.last_tool_result = None
        database.init_db(logger=self.logger)

        self.bash_tool_instance = _dummy_run_bash if run_in_bash_session_tool is None else run_in_bash_session_tool

        self.tools = get_all_tools(
            logger=self.logger,
            google_search_tool=google_search_tool or _dummy_google_search,
            view_text_website_tool=view_text_website_tool or _dummy_view_website,
            grep_tool=grep_tool or _dummy_grep,
            run_in_bash_session_tool=self.bash_tool_instance
        )
        self.tool_map = {tool.name: tool for tool in self.tools}

    def _llm_choose_tool(self, command: str) -> str:
        """ **LLM Simulation** """
        self.logger("--- [LLM Simulation] ---")
        self.logger(f"Prompt > User Command: '{command}'")

        lower_command = command.lower()
        response_json = {"tool_name": None, "parameters": None}

        # New rules for file and music search
        if "list" in lower_command and "music" in lower_command:
            response_json = {"tool_name": "list_music_files", "parameters": None}
        elif "search" in lower_command and "for" in lower_command:
            topic = lower_command.split("for", 1)[-1].strip().strip("'\"")
            response_json = {
                "tool_name": "search_files_for_topic",
                "parameters": {"topic": topic}
            }
        # Keep old rules
        elif "fix" in lower_command or "install" in lower_command:
             response_json = {
                "tool_name": "troubleshoot_dev_issue",
                "parameters": {"issue_description": command}
            }
        elif "what is" in lower_command:
             response_json = {
                "tool_name": "answer_question_from_web",
                "parameters": {"query": command}
            }

        self.logger(f"LLM Response (JSON): {json.dumps(response_json)}")
        self.logger("--- [End LLM Simulation] ---")
        return json.dumps(response_json)

    def execute_command(self, command_text: str) -> str:
        self.logger(f"\n[Vedic 4.5] Received command: \"{command_text}\"")

        # The translation step was removed during the V4 refactor,
        # as a real LLM would handle multilingual input directly.
        # We will add it back here conceptually.
        # translated_text, source_lang = translate_to_english(command_text, logger=self.logger)
        translated_text = command_text # For now, assume English

        tools_description = get_formatted_tool_descriptions(self.tools)
        llm_response_str = self._llm_choose_tool(translated_text)

        try:
            llm_response = json.loads(llm_response_str)
            tool_name = llm_response.get("tool_name")
            parameters = llm_response.get("parameters")
        except json.JSONDecodeError:
            return "Sorry, my 'brain' produced an invalid response."

        if not tool_name:
            return "I don't have a tool for that."

        if tool_name in self.tool_map:
            tool_to_use = self.tool_map[tool_name]
            result = tool_to_use.use(**parameters) if parameters else tool_to_use.use()
            self.last_tool_result = result
            return str(result)
        else:
            return f"I tried to use a tool named '{tool_name}', but I couldn't find it."
