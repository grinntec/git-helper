# create_project.py
import os
from datetime import datetime
from config import (
    QUESTION_TEXT,
    ANSWER_TEXT,
    ERROR_TEXT,
    OUTPUT_TEXT,
    RESET_TEXT,
    print_section_header,
)

GITIGNORE_CONTENT = """# Python
__pycache__/
*.py[cod]
*$py.class

# Jupyter Notebook
.ipynb_checkpoints

# Terraform
*.tfstate
*.tfstate.backup
*.tfstate.lock.info
.terraform/

# Markdown/MkDocs
/site

# Distribution / packaging
build/
dist/
.eggs/
*.egg-info/
.Python
"""

MIT_LICENSE_TEMPLATE = """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

BASE_FOLDERS = [
    "src",
    "docs",
]
BASE_FILES = [
    "README.md",
    "LICENSE",
    ".gitignore",
    "CHANGELOG.md",
]

def simple_project_init():
    print_section_header("New Project Initializer")
    project_name = input(f"{QUESTION_TEXT}Enter project name: {RESET_TEXT}").strip()
    if not project_name:
        print(f"{ERROR_TEXT}Project name cannot be empty.{RESET_TEXT}")
        return

    description = input(f"{QUESTION_TEXT}Short description: {RESET_TEXT}").strip()
    author = input(f"{QUESTION_TEXT}Author name: {RESET_TEXT}").strip()
    target_path = input(f"{QUESTION_TEXT}Path to create project in: {RESET_TEXT}").strip()
    if not target_path:
        print(f"{ERROR_TEXT}Path cannot be empty.{RESET_TEXT}")
        return

    full_path = os.path.join(target_path, project_name)
    if os.path.exists(full_path):
        print(f"{ERROR_TEXT}Directory '{full_path}' already exists.{RESET_TEXT}")
        return

    # Create folders
    os.makedirs(full_path)
    for folder in BASE_FOLDERS:
        os.makedirs(os.path.join(full_path, folder))

    # Create README.md with detailed explanations and best practices
    readme_path = os.path.join(full_path, "README.md")
    structure_tree = "\n".join([f"  {folder}/" for folder in BASE_FOLDERS] + [f"  {file}" for file in BASE_FILES])
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {project_name}\n\n{description}\n\n")
        f.write("## Author\n" + author + "\n\n")
        f.write("## Project Structure\n\n")
        f.write("```\n")
        f.write(f"{project_name}/\n{structure_tree}\n```\n\n")
        f.write("### Folder Explanations\n")
        f.write("- **src/**: Main source code for this project. Place Python, Terraform, or other primary code files here.\n")
        f.write("- **docs/**: Documentation, guides, architecture notes, or Markdown files.\n")
        f.write("\n### File Explanations\n")
        f.write("- **README.md**: Overview, structure, and usage instructions.\n")
        f.write("- **LICENSE**: The project license (MIT by default).\n")
        f.write("- **.gitignore**: Patterns for files and folders to be ignored by git (Python, Terraform, Markdown, etc).\n")
        f.write("- **CHANGELOG.md**: Record of major changes, updates, and releases.\n")
        f.write("\n## Best Practices\n")
        f.write("- **Use git for version control**: Commit early, commit often. Use branches for features or fixes.\n")
        f.write("- **Document your code**: Add Markdown files in `docs/` for architecture, usage, or API reference. Add comments in code files in `src/`.\n")
        f.write("- **Update CHANGELOG.md for each major change**: Note new features, fixes, and releases.\n")
        f.write("- **Respect .gitignore**: Don’t commit IDE files, build artifacts, credentials, or `.tfstate` files (if using Terraform).\n")
        f.write("- **Add a requirements.txt or equivalents in `src/` if applicable**: For Python, list dependencies; for Terraform, use module versions in code.\n")
        f.write("- **Keep LICENSE current**: Use MIT or another OSI-approved license for open collaboration.\n")
        f.write("\n## Getting Started\n")
        f.write("1. Clone the repository or create it with this initializer.\n")
        f.write("2. Place your main code in `src/`, docs in `docs/`.\n")
        f.write("3. Initialize git and make your first commit.\n")
        f.write("4. Update `README.md` and `CHANGELOG.md` as you develop.\n")
        f.write("5. Share and collaborate!\n")

    # Create LICENSE
    license_path = os.path.join(full_path, "LICENSE")
    year = datetime.now().year
    with open(license_path, "w", encoding="utf-8") as f:
        f.write(MIT_LICENSE_TEMPLATE.format(year=year, author=author))

    # Create .gitignore
    gitignore_path = os.path.join(full_path, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(GITIGNORE_CONTENT)

    # Create empty CHANGELOG.md
    changelog_path = os.path.join(full_path, "CHANGELOG.md")
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(f"\n## 0.0.1 - {year}-{datetime.now().month:02d}-{datetime.now().day:02d}\n- Project initialized\n")

    print(f"{ANSWER_TEXT}Project initialized at {full_path}{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}Structure:{RESET_TEXT}")
    for folder in BASE_FOLDERS:
        print(f"{ANSWER_TEXT}  {folder}/ {RESET_TEXT}")
    for file in BASE_FILES:
        print(f"{ANSWER_TEXT}  {file}{RESET_TEXT}")
    return full_path