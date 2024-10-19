import asyncio
import inspect
import logging
import os
import re
import traceback
from typing import Any, Callable

import rich_click as click
from mbpy import commands
from mbpy.mpip import find_and_sort
from minspect.inspecting import inspect_library
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme

from msearch.browse import browse
from msearch.parse import mparse
from msearch.search import search_github, search_huggingface, search_web

custom_theme = Theme({"default": "on white"})
console = Console(theme=custom_theme)
logger = logging.getLogger(__name__)

def parse_and_run(query: str, func: Callable) -> Any:
    args, kwargs = mparse(query)
    for key, value in kwargs.items():
        value: str = str(value)
        if value.isnumeric():
            kwargs[key] = float(value)
        elif value.lower() in ['true', 'false']:
            kwargs[key] = value.lower() == 'true'
    try:
        return func(*args, **kwargs)
    except Exception as e:
        console.print(Panel(f"Error: {e}", title="Error", style="bold red"))
        console.print(f"Received args: {args} and kwargs: {kwargs}")
        console.print(Panel(f"Correct usage: {inspect.signature(func)}", title="Usage"))
        exit(1)



def handle_inspect_query(query):
    if "depth" not in query:
        query += " depth=0"
    if "signatures" not in query:
        query += " signatures=True"
    if "docs" not in query:
        query += " docs=False"
    result = parse_and_run(query, inspect_library)
    console.print(Panel(f"Inspecting module: {query}", title="Module Inspection"))
    console.print(Panel(result.get('functions', 'No functions found'), title="Functions"))
    console.print(Panel(result.get('classes', 'No classes found'), title="Classes"))
    console.print(Panel(result.get('variables', 'No variables found'), title="Variables"))
    return result

def handle_pypi_query(query):
    result = parse_and_run(query, find_and_sort)
    display_pypi_results(result)

def handle_huggingface_query(query):
    result = parse_and_run(query, search_huggingface)
    if not result:
        console.print(Panel("No results found.", title="HuggingFace Search"))
    else:
        display_huggingface_results(result)


search_functions = {
        'web': search_web,
        'github': search_github,
        'inspect': handle_inspect_query,
        'pypi': handle_pypi_query,
        'hf': handle_huggingface_query
    }
    

def run_search(query: str, engine: str, interactive: bool):

    results = search_functions[engine](query)
    
    if not results:
        console.print(Panel(f"No results found.", title=f"{engine.capitalize()} Search Results"))
    else:
        display = display_results(results, engine)
        interact_display = handle_interactive_mode(results, engine, interactive=interactive)
        if not interactive:
            return interact_display
    return 0

@click.command()
@click.argument('query', nargs=-1)
@click.option('--engine', '-e', default='web', help='Search engine to use: web, github, inspect, pypi, hf')
@click.option('--interactive', '-i', is_flag=True, default=False, help='Enable interactive mode')
def cli(query, engine: str, interactive: bool):
    """Search for info on the web, github, pypi, or inspect a library."""
    query = ' '.join(query)
 
    if engine not in search_functions:
        console.print(f"Invalid search engine: {engine}")
        return 1
    
    return run_search(query, engine, interactive)
    

def display_results(results, engine):
    if engine == 'web':
        display_web_results(results)
    elif engine == 'github':
        display_github_results(results)
    elif engine == 'pypi':
        display_pypi_results(results)
    elif engine == 'hf':
        display_huggingface_results(results)
    else:
        console.print(f"Display not implemented for {engine} results.")

def display_web_results(results):
    table = Table(title="Web Search Results", show_header=True, header_style="bold magenta")
    table.add_column("Index", style="cyan", width=10)
    table.add_column("Title", style="cyan", width=40, overflow="fold")
    table.add_column("URL", style="blue", width=40, overflow="fold")
    table.add_column("Snippet", style="green", width=40, overflow="fold")
    for i, result in enumerate(results, 1):
        table.add_row(
            str(i),
            result.get('title', 'No title'),
            result.get('url', 'No URL'),
            result.get('snippet', 'No snippet')
        )
    console.print(Panel(table, expand=True))
    browse([result['url'] for result in results])

import pexpect
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def handle_interactive_mode(results, engine, interactive=False):
    while True:
        # Show options to the user
        options = [f"{i}. {result.get('name', result.get('title', 'No title'))}" for i, result in enumerate(results, 1)]
        options.append("q. Quit")

        for option in options:
            console.print(option)

        # Handle interaction
        if interactive:
            child = pexpect.spawn(os.environ.get("SHELL", "bash"))
            child.interact()  # This gives control back to the REPL to choose a number
            child.sendline("exit")  # Exit from pexpect after interaction

        # Prompt for user input
        choice = Prompt.ask("Choose an option", choices=[str(i) for i in range(1, len(results) + 1)] + ["q"])

        if choice.lower() == "q":
            break  # Exit the loop if user chooses 'q'

        index = int(choice) - 1
        result = results[index]

        if engine == "web":
            console.print(display_web_content(result))
        elif engine == "github":
            console.print(display_github_content(result))
        elif engine == "pypi":
            console.print(display_pypi_content(result))
        elif engine == "hf":
            console.print(display_huggingface_content(result))
        else:
            console.print(f"Content display not implemented for {engine} results.")

        # If not interactive, return after the first result
        if not interactive:
            return result

    return None


def clean(content):
    # Step 1: Remove content between "!sc" markers (including the markers themselves)
    code_block_pattern = re.compile(r'!sc.*?!sc', re.DOTALL)
    cleaned_content = re.sub(code_block_pattern, '', content)
    cleaned_content = re.sub(r'!sc.*?!sc/', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'!sc.*?!sc/', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'{[^}]*}', '', cleaned_content)
    # Step 2: Adjust headers by ensuring proper Markdown formatting
    cleaned_content = re.sub(r'\n{2,}', '\n', cleaned_content)   # Reducing excessive newlines
    cleaned_content = re.sub(r'\s{2,}', ' ', cleaned_content)    # Reducing excessive spaces
     # Step 2: Remove any JSON-like objects, key-value pairs


    # Step 3: Remove CSS-like class definitions and content inside curly braces
    cleaned_content = re.sub(r'\.[\w\-]+[{][^}]*[}]', '', cleaned_content)
    # Step 1: Remove everything between "!sc" and its closing "sc/" while preserving the rest
    cleaned_content = re.sub(r'!sc.*?sc/', '', cleaned_content, flags=re.DOTALL)

    # Step 2: Clean up excessive newlines or extra spaces, ensuring headers remain formatted
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)  # Reduce excessive newlines
    cleaned_content = re.sub(r'\s{2,}', ' ', cleaned_content)     # Reduce excessive spaces

    # Step 3: Ensure no extra characters around headers and formatting elements are removed
    cleaned_content = re.sub(r'(?<!\n)\n\s*\n', '\n', cleaned_content)  # Clean stray newlines
    cleaned_content = cleaned_content.strip()  # Final cleanup of leading/trailing spaces

    # Display the cleaned content
    # Step 1: Remove any HTML tags
    cleaned_content = re.sub(r'<[^>]+>', '', cleaned_content)

    # Step 2: Remove CSS class definitions and styles (everything between { })
    cleaned_content = re.sub(r'\.[\w\-]+\s*{[^}]*}', '', cleaned_content)

    # Step 3: Remove unnecessary JSON-like objects or key-value pairs
    cleaned_content = re.sub(r'{[^}]*}', '', cleaned_content)

    # Step 4: Remove all occurrences of null, true, false, and excessive punctuation
    cleaned_content = re.sub(r'\b(null|false|true)\b', '', cleaned_content)
    cleaned_content = re.sub(r'[{}:;"]+', '', cleaned_content)

    # Step 7: Reformat Markdown headers, lists, and fix any spacing issues
    # Ensure Markdown headers and lists are properly formatted (handles things like ## , ### and bullet points)
    cleaned_content = re.sub(r'\s*#+\s*', lambda match: '\n' + match.group().strip() + ' ', cleaned_content)
    cleaned_content = re.sub(r'\s*[-*]\s*', lambda match: '\n' + match.group().strip() + ' ', cleaned_content)

    # Step 8: Remove any excessive new lines but preserve Markdown formatting
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

    return cleaned_content



# def clean(content):
#     # Step 1: Remove unwanted content between "!sc" markers
#     content = re.sub(r'!sc.*?sc/', '', content, flags=re.DOTALL)

#     # Step 2: Remove any unnecessary HTML-like tags or attributes
#     content = re.sub(r'<[^>]+>', '', content)

#     # Step 3: Remove unnecessary CSS-like class definitions and styles
#     content = re.sub(r'\.[\w\-]+\s*{[^}]*}', '', content)

#     # Step 4: Remove all occurrences of null, true, false, and other stray content
#     content = re.sub(r'\b(null|false|true)\b', '', content)
#     content = re.sub(r'[{}:;"]+', '', content)

#     # Step 5: Reformat Markdown headers, lists, and code blocks
#     content = re.sub(r'(?m)^\s*#+\s*(.*)', r'# \1', content)  # Adjust headers
#     content = re.sub(r'\s*[-*]\s+', r'\n- ', content)  # Adjust bullet points
    
#     # Step 6: Clean up newlines and stray spaces
#     content = re.sub(r'\n{3,}', '\n\n', content)  # Reduce excessive newlines
#     content = re.sub(r'\s{2,}', ' ', content)     # Reduce excessive spaces
#     # Ensure headers are on new lines and preserve the newline after them
#     cleaned_content = re.sub(r'(?<!\n)(#+\s.*?)(?!\n)', r'\n\1\n', content)
#     # Remove inline styles and script tags
#     cleaned_content = re.sub(r'<style[^>]*>.*?</style>', '', cleaned_content, flags=re.DOTALL)
#     cleaned_content = re.sub(r'<script[^>]*>.*?</script>', '', cleaned_content, flags=re.DOTALL)


#     # Preserve comments by ensuring they are not treated as headers
#     cleaned_content = re.sub(r'(?<!\n)(#(?!#).*)', r'\n\1', cleaned_content)

#     # Handle code blocks by ensuring they are preserved with surrounding newlines
#     code_block_pattern = re.compile(r'```.*?```', re.DOTALL)
#     cleaned_content = re.sub(code_block_pattern, lambda match: f"\n{match.group(0)}\n", cleaned_content)

#     # Ensure final cleanup
#     content = cleaned_content.strip()

#     return content

# Example usage


def display_web_content(result, interactive=False):
    console.print(f"Title: {result['title']}", style="cyan")
    console.print(f"URL: {result['url']}", style="blue")
    result = browse([result['url']], interactive=interactive)[0]
    content = result.get('content')
    if not content:
        console.print("No content found.", style="bold red")
        return
    console.print(f"Title: {result['title']}", style="cyan")
    console.print("Content:", style="yellow")
    console.print(Markdown(clean(content)))

    words = content.split()
    total_words = len(words)
    current_position = 0
    return content

    # while current_position < total_words:
    #     chunk = ' '.join(words[current_position:current_position + 2000])
    #     console.print(Markdown(chunk))
    #     current_position += 2000
        
    #     if current_position < total_words:  # noqa: SIM102
    #         if not interactive or  Prompt.ask("Continue reading?", choices=["y", "n"], default="y") != "y":
    #             break

# def display_web_content(result):
#     url = result['url']
#     browse_result = browse([url], interactive=True)[0]
    
#     if 'error' in browse_result:
#         console.print(f"Error for {url}: {browse_result['error']}", style="bold red")
#     else:
#         console.print(f"Title: {browse_result['title']}", style="cyan")
#         console.print("Content:", style="yellow")
#         console.print(Markdown(browse_result['content']))

def display_github_content(result):
    console.print(f"Repository: {result['name']}", style="cyan")
    console.print(f"URL: {result['url']}", style="blue")
    console.print(f"Description: {result['description']}", style="green")
    console.print(f"Stars: {result['stars']}", style="yellow")
    console.print(f"Forks: {result['forks']}", style="yellow")

def display_pypi_content(result):
    console.print(f"Package: {result['name']}", style="cyan")
    console.print(f"Version: {result['version']}", style="magenta")
    console.print(f"Description: {result['summary']}", style="green")

def display_huggingface_content(result):
    console.print(f"Name: {result['name']}", style="cyan")
    console.print(f"Type: {result['type'].capitalize()}", style="magenta")
    console.print(f"URL: {result['url']}", style="blue")
    console.print(f"Downloads: {result['downloads']}", style="green")
    console.print(f"Likes: {result['likes']}", style="yellow")

def display_github_results(results):
    table = Table(title="GitHub Search Results")
    table.add_column("Repository", style="cyan", no_wrap=True)
    table.add_column("URL", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Stars", justify="right", style="yellow")
    table.add_column("Forks", justify="right", style="yellow")
    for repo in results:
        table.add_row(repo['name'], repo['url'], repo['description'], str(repo['stars']), str(repo['forks']))
    console.print(Panel(table))

def display_pypi_results(results):
    table = Table(title="PyPI Search Results")
    table.add_column("Package", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Description", style="green")
    for package in results:
        table.add_row(package['name'], package['version'], package['summary'])
    console.print(Panel(table))

def display_huggingface_results(results):
    table = Table(title="HuggingFace Search Results", show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("URL", style="blue")
    table.add_column("Downloads", justify="right", style="green")
    table.add_column("Likes", justify="right", style="yellow")
    for item in results:
        table.add_row(item['type'].capitalize(), item['name'], item['url'], str(item['downloads']), str(item['likes']))
    console.print(Panel(table, expand=False))
    console.print(Panel(f"Total results: {len(results)}", title="Summary", style="bold green"))

if __name__ == "__main__":
    exit(cli())
