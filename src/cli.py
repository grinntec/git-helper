import os
from enum import Enum

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

# Constants
PROGRAM_TITLE = "Git Helper"
PROGRAM_AUTHOR = "Neil Grinnall"
PROGRAM_HELP_TEXT = "A guided method to using Git"
PROGRAM_VERSION = "0.0.2"
PROGRAM_DATE = "2025-09"

#--- Define an enumeration class named UserChoice ---#
class UserChoice(Enum):
    # Each member of this enumeration represents a user choice in the application
    
    # REFRESH checks and displays the current status with no actions taken
    REFRESH = ('0', 'REFRESH and display current status')
    # PULL represents the choice to pull changes from the remote repository
    PULL = ('1', 'PULL changes from remote repository')  
    # PUSH represents the choice to push changes to the remote repository
    PUSH = ('2', 'PUSH changes to remote repository (into MAIN branch)')    
    # COMMIT represents the choice to commit changes to the local repository
    COMMIT = ('3', 'COMMIT changes to local repository')
    # ADD represents the choice to add changes to the staging area
    ADD = ('4', 'ADD changes/files to staging area')    
    # TAG represents the choice to tag a specific commit
    TAG = ('5', 'TAG the repository')    
    # EXIT represents the choice to exit the application
    EXIT = ('6', 'Exit the application')

# --- Display a title card --- #
def display_title(title, author, help_text, version, date):
    """
    Display a professional-looking title in the console.

    Args:
    - title (str): The title of the program.
    - author (str): The author's name.
    - help_text (str): A brief description of what the program does.
    - version (str): The version of the program.
    - date (str): The release or update date.
    """    
    # Determine the maximum length for proper formatting
    max_length = max(len(title), len(author), len(help_text), len(version) + len("Version: "), len(date) + len("Date: "))
    
    # Print the top border
    print("+" + "-" * (max_length + 2) + "+")
    
    # Print the title, centered
    print("| " + title.center(max_length) + " |")
    print("| " + ("Version: " + version).center(max_length) + " |")
    print("| " + ("Date: " + date).center(max_length) + " |")
    print("| " + ("Author: " + author).center(max_length) + " |")
    print("| " + "-" * max_length + " |")
    
    # Print the help text, centered
    print("| " + help_text.center(max_length) + " |")
    
    # Print the bottom border
    print("+" + "-" * (max_length + 2) + "+")

# --- Clear the console screen --- #
def clear_screen():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Ensures the last message is read before continuing --- #
def prompt_to_continue():
    input("Press enter to continue...")

# --- Act based on what the user inputs --- #
def get_user_choice():
    choice = input("\nEnter the number of your choice: ")
    return choice    