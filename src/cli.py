import os
from enum import Enum
import re

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

# Program metadata
PROGRAM_TITLE = "Git Helper"
PROGRAM_AUTHOR = "Neil Grinnall"
PROGRAM_HELP_TEXT = "A guided method to using Git"
PROGRAM_VERSION = "0.0.2"
PROGRAM_DATE = "2025-09"

class UserChoice(Enum):
    REFRESH = ('0', 'REFRESH and display current status')
    PULL = ('1', 'PULL changes from remote repository')  
    PUSH = ('2', 'PUSH changes to remote repository (into MAIN branch)')    
    COMMIT = ('3', 'COMMIT changes to local repository')
    ADD = ('4', 'ADD changes/files to staging area')    
    TAG = ('5', 'TAG the repository')    
    EXIT = ('x', 'Exit the application')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title(title, author, help_text, version, date):
    max_length = max(
        len(title), len(author), len(help_text),
        len(version) + len("Version: "), len(date) + len("Date: ")
    )
    print("+" + "-" * (max_length + 2) + "+")
    print("| " + title.center(max_length) + " |")
    print("| " + ("Version: " + version).center(max_length) + " |")
    print("| " + ("Date: " + date).center(max_length) + " |")
    print("| " + ("Author: " + author).center(max_length) + " |")
    print("| " + "-" * max_length + " |")
    print("| " + help_text.center(max_length) + " |")
    print("+" + "-" * (max_length + 2) + "+")

def prompt_to_continue():
    input("Press enter to continue...")

def log_options():
    print(f"\n{BOLD_TEXT}Options:{RESET_TEXT}")
    for choice in UserChoice:
        number, description = choice.value
        if ' ' in description:
            command_word, rest = description.split(' ', 1)
        else:
            command_word = description
            rest = ""
        print(f"{OUTPUT_TEXT}{number}. {ANSWER_TEXT}{command_word}{OUTPUT_TEXT} {rest}{RESET_TEXT}")

def log_separator():
    print(f"{BOLD_TEXT}{'-' * 30}{RESET_TEXT}")

def show_error(message):
    print(f"{ERROR_TEXT}Error: {message}{RESET_TEXT}")

def show_warning(message):
    print(f"{WARNING_TEXT}Warning: {message}{RESET_TEXT}")

def get_user_choice():
    while True:
        choice = input(f"\n{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")
        if choice not in [option.value[0] for option in UserChoice]:
            print(f"{ERROR_TEXT}Invalid choice. Please try again.{RESET_TEXT}")
        else:
            return choice

# --- New: Display repository information in the CLI --- #
def print_repository_info(repo, branch_name, latest_tag):
    remote_url = repo.remotes.origin.url
    org_name, repo_name = get_org_and_repo_name(remote_url)
    
    print(f"\n{BOLD_TEXT}--- Repository Information ---{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Organization/User: {ANSWER_TEXT}{org_name}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Repository Name:   {ANSWER_TEXT}{repo_name}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Working Directory: {ANSWER_TEXT}{repo.working_tree_dir}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Active Branch:     {ANSWER_TEXT}{branch_name}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Latest Tag:        {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")

# --- New: Display status information in the CLI --- #
def print_status(comparison_result):
    print(f"{BOLD_TEXT}--- Differences between local and origin ---{RESET_TEXT}")
    print(comparison_result)