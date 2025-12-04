import requests

from models import URLList

class URLProcessor:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.headers = {
            "Accept": "text/css",
            "User-Agent": "Mozilla/5.0" 
        }

    def check_url(self, url: str):
        """Check a single URL and return (url, response_text) if 200."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)

            return {
                "url": url,
                "status": response.status_code,
                "content": response.text
            }
            
        except requests.exceptions.RequestException:
            return None

    def check_urls(self, url_list: list[URLList]):
        """Check multiple URLs and return only successful responses."""
        results = []

        for url in url_list:
            result = self.check_url(url.url)
            if result:
                results.append(result)

        return results
