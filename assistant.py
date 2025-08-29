import json
import database
from tools.tool_registry import get_all_tools, get_formatted_tool_descriptions

# --- Tool Definitions (Dummies for standalone execution) ---
def _dummy_google_search(query: str): return f"Dummy search result for '{query}' with URL: https://example.com"
def _dummy_view_website(url: str): return f"Dummy content for website: {url}"
def _dummy_grep(pattern: str): return f"Dummy grep result for pattern '{pattern}'"

def _dummy_run_bash(command: str): return f"Dummy execution of command: '{command}'"

class Assistant:
    """
    The core of the Vedic 4.0 architecture: a tool-using agent.

    This class orchestrates the entire process of turning a user's natural language
    command into an action. It doesn't contain much logic itself; its main job
    is to consult a Large Language Model (LLM) to reason about which tool to use.
    """
    def __init__(self, logger=print, google_search_tool=None, view_text_website_tool=None, grep_tool=None, run_in_bash_session_tool=None):
        self.logger = logger

        # Initialize the database
        database.init_db(logger=self.logger)

        # Initialize all available tools, injecting dependencies.
        self.tools = get_all_tools(
            logger=self.logger,
            google_search_tool=google_search_tool or _dummy_google_search,
            view_text_website_tool=view_text_website_tool or _dummy_view_website,
            grep_tool=grep_tool or _dummy_grep,
            run_in_bash_session_tool=run_in_bash_session_tool or _dummy_run_bash
        )
        self.tool_map = {tool.name: tool for tool in self.tools}

    def _llm_choose_tool(self, command: str, tools_description: str) -> str:
        """
        **This is a simulation of a Large Language Model (LLM) call.**
        It uses regex and keyword matching to simulate an LLM's ability
        to parse a command and choose the correct tool and parameters.
        """
        import re
        self.logger("--- [LLM Simulation] ---")
        self.logger(f"Prompt > User Command: '{command}'")

        lower_command = command.lower()
        response_json = {"tool_name": None, "parameters": None}

        # Rule for creating rectangles
        if "rectangle" in lower_command:
            numbers = [int(s) for s in re.findall(r'\b\d+\b', lower_command)]
            response_json = {
                "tool_name": "create_autocad_rectangle",
                "parameters": {"width": numbers[0], "height": numbers[1]} if len(numbers) >= 2 else {"width": 100, "height": 100}
            }
        # Rule for complex reminders
        elif "remind me to" in lower_command:
            match = re.search(r'remind me to (.*) (tomorrow at.*|at.*|in.*)', lower_command)
            if match:
                response_json = {
                    "tool_name": "log_event_to_memory",
                    "parameters": {
                        "event_type": "reminder",
                        "details": {"task": match.group(1), "time_string": match.group(2)}
                    }
                }
        # Rule for recalling events
        elif "recall" in lower_command or "what did i" in lower_command:
            event_type = "user_preference" # default
            if "last reminder" in lower_command:
                event_type = "reminder"
            response_json = {
                "tool_name": "recall_last_event_from_memory",
                "parameters": {"event_type": event_type}
            }
        # Rule for troubleshooting
        elif "fix" in lower_command or "install" in lower_command or "is broken" in lower_command:
            response_json = {
                "tool_name": "troubleshoot_dev_issue",
                "parameters": {"issue_description": command}
            }
        # Rule for web questions
        elif any(q in lower_command for q in ["what is", "who is", "explain"]):
             response_json = {
                "tool_name": "answer_question_from_web",
                "parameters": {"query": command}
            }

        self.logger(f"LLM Response (JSON): {json.dumps(response_json)}")
        self.logger("--- [End LLM Simulation] ---")
        return json.dumps(response_json)

    def execute_command(self, command_text: str) -> str:
        """
        This is the main entry point for the assistant.
        It takes a raw command string, uses an LLM to choose a tool, and executes it.
        """
        self.logger(f"\n[Vedic 4.0] Received command: \"{command_text}\"")

        # Step 1: Get the list of available tools and format their descriptions.
        # This is the "API documentation" that the LLM will use to make its decision.
        tools_description = get_formatted_tool_descriptions(self.tools)

        # Step 2: Call the (simulated) LLM to get its decision.
        # The LLM's response is expected to be a JSON string containing the
        # name of the tool to use and the parameters for it.
        llm_response_str = self._llm_choose_tool(command_text, tools_description)

        # Step 3: Parse the LLM's response.
        try:
            llm_response = json.loads(llm_response_str)
            tool_name = llm_response.get("tool_name")
            parameters = llm_response.get("parameters")
        except json.JSONDecodeError:
            self.logger(f"Error: LLM returned invalid JSON: {llm_response_str}")
            return "I'm sorry, I seem to be having a problem with my internal reasoning. Please try again."

        # Step 4: Execute the chosen tool.
        if not tool_name:
            self.logger("LLM decided no tool was appropriate for the command.")
            return "I'm sorry, I don't think I have a tool that can help with your request."

        if tool_name in self.tool_map:
            tool_to_use = self.tool_map[tool_name]
            self.logger(f"LLM chose to use tool: '{tool_name}' with parameters: {parameters}")
            try:
                # Use the tool with the parameters provided by the LLM
                result = tool_to_use.use(**parameters) if parameters else tool_to_use.use()
                self.logger(f"[Vedic 4.0] Response: \"{result}\"")
                return str(result)
            except Exception as e:
                error_msg = f"An error occurred while executing the '{tool_name}' tool. Details: {e}"
                self.logger(f"[Vedic 4.0] {error_msg}")
                return error_msg
        else:
            error_msg = f"I tried to use a tool named '{tool_name}', but I couldn't find it in my toolbox."
            self.logger(f"[Vedic 4.0] Error: {error_msg}")
            return f"I'm sorry, an internal error occurred. {error_msg}"
