# This file serves as a central registry for all available tools.
# It imports all tool classes and provides a function to initialize
# and return a list of all tool instances that the assistant can use.

from .autocad_tools import CreateRectangleTool, AddCircleTool
from .browser_tools import OpenWebsiteTool
from .notes_tools import SearchNotesTool
from .qgis_tools import CreateShapefileTool
from .research_tools import AnswerQuestionFromWebTool
from .revit_tools import CreateWallTool
from .system_tools import RunDiagnosticsTool, CheckForUpdatesTool, OptimizePerformanceTool
from .shell_tools import RunBashCommandTool, TroubleshootDevIssueTool
from .memory_tools import LogEventTool, RecallEventTool

def get_all_tools(
    logger,
    google_search_tool,
    view_text_website_tool,
    grep_tool,
    run_in_bash_session_tool
):
    """
    Initializes and returns a list of all available tool instances.
    Dependencies like loggers and external tools are injected here.
    """
    # Low-level tools
    bash_tool = RunBashCommandTool(logger=logger, run_in_bash_session_tool=run_in_bash_session_tool)

    # High-level tools that might use other tools
    fix_it_tool = TroubleshootDevIssueTool(logger=logger, bash_tool=bash_tool)

    return [
        CreateRectangleTool(logger=logger),
        AddCircleTool(logger=logger),
        OpenWebsiteTool(logger=logger),
        SearchNotesTool(logger=logger, grep_tool=grep_tool),
        CreateShapefileTool(logger=logger),
        AnswerQuestionFromWebTool(
            logger=logger,
            google_search_tool=google_search_tool,
            view_text_website_tool=view_text_website_tool
        ),
        CreateWallTool(logger=logger),
        RunDiagnosticsTool(logger=logger),
        CheckForUpdatesTool(logger=logger),
        OptimizePerformanceTool(logger=logger),
        bash_tool,
        fix_it_tool,
        LogEventTool(logger=logger),
        RecallEventTool(logger=logger),
    ]

def get_formatted_tool_descriptions(tool_list):
    """
    Formats the list of tools into a string for the LLM prompt.
    """
    description_string = ""
    for tool in tool_list:
        description_string += f"- Tool Name: {tool.name}\n"
        description_string += f"  Description: {tool.description}\n\n"
    return description_string.strip()
