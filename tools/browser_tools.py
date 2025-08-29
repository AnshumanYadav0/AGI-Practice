import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class OpenWebsiteTool:
    """A tool to open a website in a web browser using Selenium."""
    name = "open_website"
    description = "Navigates to a specific URL in a web browser. The `url` parameter must be a full, valid URL (e.g., 'https://www.google.com')."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self, url: str):
        self.logger(f"--- Browser Tool: Attempting to open URL: {url} ---")

        if not url.startswith("http"):
            url = "https://" + url

        driver = None
        try:
            service = ChromeService(ChromeDriverManager().install())

            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome(service=service, options=options)

            self.logger(f"WebDriver initialized. Navigating to {url}...")
            driver.get(url)

            time.sleep(3)

            title = driver.title
            self.logger(f"Successfully opened '{title}'")
            return f"Successfully opened website: {title}"

        except Exception as e:
            self.logger(f"WARNING: Selenium WebDriver failed. Running in dummy mode. Error: {e}")
            dummy_message = f"DUMMY MODE: Would have opened {url}"
            self.logger(dummy_message)
            return dummy_message
        finally:
            if driver:
                driver.quit()
                self.logger("Browser closed.")
