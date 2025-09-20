import os
from utils import (
    setup_logging,
    prompt_user,
    create_file_with_content,
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
    DEFAULT_LICENSE,
    DEFAULT_GITIGNORE,
    PROJECT_STRUCTURE,
)

logger = setup_logging()

def create_project_structure(project_name, structure):
    os.makedirs(project_name, exist_ok=True)
    for path in structure:
        abs_path = os.path.join(project_name, path)
        if path.endswith('/'):
            os.makedirs(abs_path, exist_ok=True)
        else:
            open(abs_path, 'a').close()

def main():
    print_section_header(PROGRAM_TITLE)
    logger.info(f"{OUTPUT_TEXT}Welcome to the Python Project Initializer!{RESET_TEXT}")

    project_name = prompt_user("Enter the project name:")
    description = prompt_user("Short project description:")
    author = prompt_user("Author name:")
    license_type = prompt_user("License (default: MIT):", default="MIT")

    # Create the folder structure
    create_project_structure(project_name, PROJECT_STRUCTURE)

    # Write README.md
    readme_content = f"""# {project_name}

{description}

## Project Structure
