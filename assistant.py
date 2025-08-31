import json
import database
from tools.tool_registry import get_all_tools, get_formatted_tool_descriptions
import re

# --- Dummy Tool Functions for Standalone Execution ---
def _dummy_google_search(query: str): return f"Dummy search result for '{query}'"
def _dummy_view_website(url: str): return f"Dummy content for '{url}'"
def _dummy_grep(pattern: str): return f"Dummy grep result for '{pattern}'"
def _dummy_run_bash(command: str): return f"Dummy execution of '{command}'"

class Assistant:
    """
    The core of the Vedic 5.0 architecture: a tool-using agent.
    This class orchestrates turning a user command into an action by using a
    simulated Large Language Model (LLM) to reason about which tool to use.
    """
    def __init__(self, logger=print, **kwargs):
        self.logger = logger
        self.last_tool_result = None # Stores the output of the last executed tool

        database.init_db(logger=self.logger)
        self.custom_commands = self.load_custom_commands()

        # Inject real tools if provided, otherwise use dummies
        injected_tools = {
            "google_search_tool": kwargs.get('google_search_tool', _dummy_google_search),
            "view_text_website_tool": kwargs.get('view_text_website_tool', _dummy_view_website),
            "grep_tool": kwargs.get('grep_tool', _dummy_grep),
            "run_in_bash_session_tool": kwargs.get('run_in_bash_session_tool', _dummy_run_bash)
        }

        self.tools = get_all_tools(logger=self.logger, **injected_tools)
        self.tool_map = {tool.name: tool for tool in self.tools}

    def load_custom_commands(self, filepath="commands.json"):
        """Loads or reloads custom commands from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.logger(f"[Assistant] Loading custom commands from {filepath}")
                return json.load(f)
        except FileNotFoundError:
            self.logger(f"WARNING: '{filepath}' not found. No custom commands loaded.")
            return []

    def _llm_choose_tool(self, command: str) -> str:
        """
        **This is a simulation of a Large Language Model (LLM) call.**
        It uses a prioritized set of rules to choose the best tool for a command.
        """
        self.logger("--- [LLM Brain Simulation] ---")
        self.logger(f"User Command: '{command}'")

        lower_command = command.lower()
        response_json = {"tool_name": None, "parameters": None}

        # Rule Priority:
        # 1. High-intent actions (scheduling, learning)
        # 2. Custom commands defined by the user
        # 3. General purpose tools (file search, app launch, etc.)

        if "remind me to" in lower_command or "schedule" in lower_command:
            match = re.search(r'(remind me to|schedule a task to) (.*) (in .*|at .*)', lower_command)
            if match:
                response_json = {"tool_name": "schedule_task", "parameters": {"task_description": match.group(2), "time_string": match.group(3)}}

        elif "learn" in lower_command and "workflow" in lower_command:
             response_json = {"tool_name": "learn_new_workflow_from_screen", "parameters": {"screen_text": self.last_tool_result}}

        elif "read" in lower_command and "screen" in lower_command:
            response_json = {"tool_name": "read_current_screen", "parameters": None}

        else: # Check custom and general commands only if no high-intent keyword was found
            for cmd_def in self.custom_commands:
                if cmd_def['phrase'] in lower_command:
                    response_json = {"tool_name": cmd_def['action'], "parameters": None}
                    break

            if not response_json.get("tool_name"): # If still no tool found
                if "fix" in lower_command or "install" in lower_command or "is broken" in lower_command:
                    response_json = {"tool_name": "troubleshoot_dev_issue", "parameters": {"issue_description": command}}
                elif "list" in lower_command and "music" in lower_command:
                    response_json = {"tool_name": "list_music_files", "parameters": None}
                elif "search" in lower_command and "for" in lower_command:
                    response_json = {"tool_name": "search_files_for_topic", "parameters": {"topic": lower_command.split("for", 1)[-1].strip().strip("'\"")}}
                elif any(q in lower_command for q in ["what is", "who is", "explain"]):
                    response_json = {"tool_name": "answer_question_from_web", "parameters": {"query": command}}
                elif "remember that" in lower_command:
                    info = command.split("remember that", 1)[1].strip()
                    response_json = {"tool_name": "log_event_to_memory", "parameters": {"event_type": "user_preference", "details": {"info": info}}}
                elif "recall" in lower_command or "what did i ask you to remember" in lower_command:
                    response_json = {"tool_name": "recall_last_event_from_memory", "parameters": {"event_type": "user_preference"}}
                elif any(v in lower_command for v in ["open", "launch", "start"]):
                     app_name = " ".join(lower_command.split()[1:]).replace("the ", "").replace("a ", "")
                     response_json = {"tool_name": "open_windows_app", "parameters": {"app_name": app_name}}

        self.logger(f"LLM Decision: {json.dumps(response_json)}")
        return json.dumps(response_json)

    def execute_command(self, command_text: str) -> str:
        """The main entry point to process a user command."""
        self.logger(f"\n[Vedic 5.0] Received command: \"{command_text}\"")

        llm_response_str = self._llm_choose_tool(command_text)

        try:
            llm_response = json.loads(llm_response_str)
            tool_name = llm_response.get("tool_name")
            parameters = llm_response.get("parameters")
        except json.JSONDecodeError:
            return "I'm sorry, my internal reasoning failed. Please try again."

        if not tool_name:
            return "I'm sorry, I don't have a tool that can help with that request."

        if tool_name in self.tool_map:
            tool_to_use = self.tool_map[tool_name]
            self.logger(f"Executing Tool: '{tool_name}' with parameters: {parameters}")
            try:
                result = tool_to_use.use(**parameters) if parameters else tool_to_use.use()
                self.last_tool_result = result # Save result for potential follow-up commands
                self.logger(f"[Vedic 5.0] Response: {result}")
                return str(result)
            except Exception as e:
                error_msg = f"An error occurred while executing the '{tool_name}' tool. Details: {e}"
                self.logger(error_msg)
                return error_msg
        else:
            error_msg = f"I tried to use a tool named '{tool_name}', but it's not in my toolbox."
            self.logger(error_msg)
            return f"I'm sorry, an internal error occurred: {error_msg}"
