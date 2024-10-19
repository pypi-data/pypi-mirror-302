import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
from lager import log
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Span, Text

console = Console(style="bold white on cyan1", soft_wrap=True)
blue_console = Console(style="bold white on blue", soft_wrap=True)
print = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="red", overflow="fold")) for arg in args), **kwargs) # noqa
print_bold = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="bold", overflow="fold")) for arg in args), **kwargs)
input = lambda arg, **kwargs: Confirm.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, default="y", **kwargs) # noqa
ask = lambda arg, **kwargs: Prompt.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, **kwargs) # noqa

def is_valid_url(url) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def html_to_markdown(element, level=0):
    markdown = ""
    if element.name:
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            markdown += f"{'#' * int(element.name[1])} {element.prettify().strip()}\n\n"
        elif element.name == 'p':
            
            markdown += f"{element.prettify().strip()}\n\n"
        # elif element.name == 'a':
        #     href = element.get('href', '')
        #     markdown += f"[{element.prettify().strip()}]({href})"
        # elif element.name in ['ul', 'ol']:
        #     for li in element.find_all('li', recursive=False):
        #         markdown += f"{'  ' * level}- {li.prettify().strip()}\n"
        #     markdown += "\n"
        else:
            for child in element.children:
                if child.name:
                    markdown += html_to_markdown(child, level + 1)
                elif isinstance(child, str) and not "!sc" in child:
                    markdown += child.strip() + " "
    return markdown

def browse(urls, timeout=25, interactive=False):
    log.debug(f"browse function called with urls: {urls}, timeout: {timeout}, interactive: {interactive}")
    results = []
    for i, url in enumerate(urls):
        try:
            log.debug(f"Sending GET request to {url}")
            response = requests.get(url, timeout=timeout)
            log.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html5lib')

            title = soup.title.string if soup.title else "No title found"
            markdown_content = html_to_markdown(soup.body)
            
            result = {
                'url': url,
                'title': title,
                'content': markdown_content,
            }
            results.append(result)
            
            log.info(f"Processed: {url}")
        except requests.exceptions.RequestException as e:
            log.error(f"Error fetching the webpage {url}: {str(e)}")
            error_message = f"Error fetching the webpage: {e.response.status_code if hasattr(e, 'response') else str(e)}"
            results.append({
                'url': url,
                'error': error_message,
            })
        except Exception as e:
            log.error(f"Unexpected error while browsing {url}: {str(e)}")
            log.exception("Exception traceback:")
            results.append({
                'url': url,
                'error': f"Error browsing {url}: {str(e)}",
            })
    
    return results

if __name__ == "__main__":
    browse()
