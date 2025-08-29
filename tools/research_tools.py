from typing import Callable
import re

class AnswerQuestionFromWebTool:
    """A tool to answer questions by searching the web."""
    name = "answer_question_from_web"
    description = "Searches the public internet to find an answer to a specific question. Use this for general knowledge, facts, or current events. The entire question should be passed as the `query`."

    def __init__(self, logger: Callable = print, google_search_tool: Callable = None, view_text_website_tool: Callable = None):
        self.logger = logger
        self.google_search_tool = google_search_tool
        self.view_text_website_tool = view_text_website_tool

    def use(self, query: str):
        self.logger(f"--- Research Tool: Answering question '{query}' ---")

        if not self.google_search_tool or not self.view_text_website_tool:
            self.logger("ERROR: Web search tools were not provided to the research tool.")
            return "Sorry, the web search tools are not available at the moment."

        try:
            self.logger(f"Searching Google for: '{query}'")
            search_results_text = self.google_search_tool(query=query)

            urls = re.findall(r'https?://[^\s\)\"]+', search_results_text)
            if not urls:
                return "Sorry, I couldn't find any relevant websites for that question."

            top_url = urls[0]
            self.logger(f"Found top URL: {top_url}")

            self.logger(f"Reading content from {top_url}...")
            website_content = self.view_text_website_tool(url=top_url)
            if not website_content:
                return f"Sorry, I was unable to read the content from {top_url}."

            summary = website_content.strip()[:1000]
            final_answer = f"According to {top_url}, here is a summary:\n\n{summary}..."
            self.logger("Successfully generated answer from web content.")
            return final_answer

        except Exception as e:
            self.logger(f"An error occurred during web research: {e}")
            return "I'm sorry, an unexpected error occurred while I was searching the web."
