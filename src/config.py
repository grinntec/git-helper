# ANSI escape codes for text colors and reset
BOLD_TEXT = '\033[1m'
UNDERLINE_TEXT = '\033[4m'
QUESTION_TEXT = '\033[96m\033[1m'  # Bold Cyan
ANSWER_TEXT = '\033[92m'  # Green
ERROR_TEXT = '\033[91m\033[1m'  # Bold Red
OUTPUT_TEXT = '\033[97m'  # White
HELP_TEXT = '\033[90m'  # Grey
WARNING_TEXT = '\033[93m'  # Yellow
RESET_TEXT = '\033[0m'  # Reset

# Section header function
def print_section_header(text, color=BOLD_TEXT):
    """
    Print a visually strong section header with underline and color.
    
    # Example usage in your CLI script:
        print_section_header("Repository Information", color=QUESTION_TEXT)
        print_section_header("Options", color=WARNING_TEXT)
        print_section_header("Differences between local and origin", color=OUTPUT_TEXT)
        print_section_header("Error", color=ERROR_TEXT)
        print_section_header("Guidance", color=HELP_TEXT)

    """
    line_length = max(32, len(text) + 6)
    print(f"{color}{'=' * line_length}{RESET_TEXT}")
    print(f"{color}{text.center(line_length)}{RESET_TEXT}")
    print(f"{color}{'=' * line_length}{RESET_TEXT}")

# Program metadata
PROGRAM_TITLE = "Git Helper"
PROGRAM_AUTHOR = "Neil Grinnall"
PROGRAM_HELP_TEXT = "A guided method to using Git"
PROGRAM_VERSION = "1.1.0"
PROGRAM_DATE = "2025-09"