import os
from enum import Enum
import re

from utils import ( 
    get_org_and_repo_name,
    get_uncommitted_changes,
    compare_with_origin
)

from config import (
    BOLD_TEXT,
    UNDERLINE_TEXT,
    QUESTION_TEXT,
    ANSWER_TEXT,
    ERROR_TEXT,
    OUTPUT_TEXT,
    HELP_TEXT,
    WARNING_TEXT,
    RESET_TEXT,
    print_section_header,
    PROGRAM_TITLE,
    PROGRAM_AUTHOR,
    PROGRAM_HELP_TEXT,
    PROGRAM_VERSION,
    PROGRAM_DATE,
)

class UserChoice(Enum):
    REFRESH = ('0', 'REFRESH and display current status')
    PULL = ('1', 'PULL changes from remote repository')  
    PUSH = ('2', 'PUSH changes to remote repository (into MAIN branch)')    
    ADD = ('3', 'ADD changes/files to staging area')    
    COMMIT = ('4', 'COMMIT changes to local repository')
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
    print_section_header("Options", color=WARNING_TEXT)
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

def print_repository_info(repo, branch_name, latest_tag):
    remote_url = repo.remotes.origin.url
    org_name, repo_name = get_org_and_repo_name(remote_url)
    
    print_section_header("Repository Information", color=WARNING_TEXT)
    print(f"{OUTPUT_TEXT}Origin:            {ANSWER_TEXT}{remote_url}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Organization/User: {ANSWER_TEXT}{org_name}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Repository Name:   {ANSWER_TEXT}{repo_name}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Working Directory: {ANSWER_TEXT}{repo.working_tree_dir}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Active Branch:     {ANSWER_TEXT}{branch_name}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Latest Tag:        {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")


def print_status(comparison_result):
    print_section_header("Differences between local and origin", color=WARNING_TEXT)
    print(comparison_result)