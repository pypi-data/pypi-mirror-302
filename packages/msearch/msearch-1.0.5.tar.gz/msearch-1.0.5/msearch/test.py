from prompt_toolkit import prompt
from msearch.main import display_web_content, display_github_content, display_pypi_content, display_huggingface_content
def handle_interactive_mode(results, engine, interactive=False):
    choice = None
    
    while choice != 'q':
        # Display the options (1-indexed)
        options = [f"{i}. {result.get('name', result.get('title', 'No title'))}" for i, result in enumerate(results, 1)]
        options.append("q. Quit")

        # Print the options
        for option in options:
            print(option)

        # Get the user's choice via prompt_toolkit's prompt method
        choice = prompt("Choose an option (number or 'q' to quit): ")

        # Handle quitting
        if choice.lower() == 'q':
            break

        try:
            # Validate input and fetch the selected result
            index = int(choice) - 1
            result = results[index]

            # Display the selected content based on the engine
            if engine == 'web':
                results = display_web_content(result, interactive=interactive)
            elif engine == 'github':
                results = display_github_content(result)
            elif engine == 'pypi':
                results = display_pypi_content(result)
            elif engine == 'hf':
                results = display_huggingface_content(result)
            else:
                print(f"Content display not implemented for {engine} results.")
        
        except (ValueError, IndexError):
            print("Invalid option. Please choose a valid number.")

        # Optionally return results for non-interactive mode
        if not interactive:
            return results

    return None
  
  
if __name__ == "__main__":
    results = [
        {"name": "Python", "description": "Python programming language", "title": "Python Programming", "url": "https://example.com"},
        {"name": "Java", "description": "Java programming language", "title": "Java Programming", "url": "https://example.com/java"},
        {"name": "C++", "description": "C++ programming language", "title": "C++ Programming", "url": "https://example.com/cpp"},
    ]
    engine = "web"
    handle_interactive_mode(results, engine, interactive=True)