
## 1.1.2 - 2025-09-20
- fix error with order of main

### Diff:
```
diff --git a/main.py b/main.py
index 56ceb3b..82f43fb 100644
--- a/main.py
+++ b/main.py
@@ -64,3 +63,0 @@ def main():
-    error_message = None
-    warning_message = None
-
@@ -67,0 +65,4 @@ def main():
+        # Ensure these are always initialized at the start of each loop
+        error_message = None
+        warning_message = None
+
@@ -71 +71,0 @@ def main():
-        # Try to initialize repo
@@ -98 +98 @@ def main():
-            continue  # Next loop iteration
+            continue
@@ -100 +100 @@ def main():
-        # (continue as before with the full menu if inside a repo)
+        # Repo is valid, show full menu
@@ -108 +107,0 @@ def main():
-
```


## 1.1.1 - 2025-09-20
- fix non repo error

### Diff:
```
diff --git a/main.py b/main.py
index 46d08da..56ceb3b 100644
--- a/main.py
+++ b/main.py
@@ -71,9 +71,28 @@ def main():
-        # Repo info
-        try:
-            repo, branch_name, latest_tag = initialize_repository()
-            print_repository_info(repo, branch_name, latest_tag)
-        except Exception as e:
-            logger.error(f"Error initializing repository: {e}")
-            show_error(f"Error initializing repository: {e}")
-            prompt_to_continue()
-            continue
+        # Try to initialize repo
+        repo, branch_name, latest_tag = initialize_repository()
+        if repo is None:
+            show_warning("You are not in a Git repository. Only project creation and repository initialization are available.")
+            log_separator()
+            print(f"{OUTPUT_TEXT}1. Create a new Git Project{RESET_TEXT}")
+            print(f"{OUTPUT_TEXT}2. Initialize a new Git Repository{RESET_TEXT}")
+            print(f"{OUTPUT_TEXT}x. Exit the application{RESET_TEXT}")
+            choice = input(f"\n{QUESTION_TEXT}Enter your choice: {RESET_TEXT}").strip()
+            if choice == '1':
+                simple_project_init()
+                prompt_to_continue()
+            elif choice == '2':
+                local_path = input(f"{QUESTION_TEXT}Enter the path to your local project directory: {RESET_TEXT}").strip()
+                if not local_path or not os.path.isdir(local_path):
+                    show_error(f"Directory '{local_path}' does not exist.")
+                    prompt_to_continue()
+                    continue
+                origin_url = prompt_for_origin()
+                init_git_repo(local_path, origin_url)
+                prompt_to_continue()
+            elif choice == 'x':
+                logger.info("Exiting the application. Goodbye!")
+                break
+            else:
+                show_error("Invalid choice. Please try again.")
+                prompt_to_continue()
+            continue  # Next loop iteration
@@ -81 +100,2 @@ def main():
-        # Status info
+        # (continue as before with the full menu if inside a repo)
+        print_repository_info(repo, branch_name, latest_tag)
@@ -105 +125 @@ def main():
-        
+
@@ -109 +129 @@ def main():
-        
+
@@ -117 +137 @@ def main():
-        
+
@@ -125 +145 @@ def main():
-        
+
@@ -129 +149 @@ def main():
-        
+
@@ -139 +159 @@ def main():
-        
+
diff --git a/src/utils.py b/src/utils.py
index 89810f8..73f8133 100644
--- a/src/utils.py
+++ b/src/utils.py
@@ -53 +53,2 @@ def initialize_repository():
-        raise Exception(f"Invalid Git repository: {repo_path}")
+        # Instead of raising, return None values
+        return None, None, None
@@ -55 +56,2 @@ def initialize_repository():
-        raise Exception(f"Error initializing repository: {e}")
+        # Also return None values for other errors
+        return None, None, None
```


## 1.1.0 - 2025-09-19
- bump to minor

### Diff:
```
diff --git a/README.md b/README.md
index d9e7d99..cc2a4a0 100644
--- a/README.md
+++ b/README.md
@@ -3,2 +2,0 @@
-

-

```


## 1.0.6 - 2025-09-19
- testing the tag

### Diff:
```
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 72b4321..0afe461 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -1,26 +0,0 @@
-
-## 1.0.5 - 2025-09-19
-- fixed the modules
-
-### Diff:
-```
-diff --git a/src/tag.py b/src/tag.py
-index f37d548..6fc87f6 100644
---- a/src/tag.py
-+++ b/src/tag.py
-@@ -3 +2,0 @@
--from semver import VersionInfo
-@@ -6 +5,9 @@ import os
--
-+import sys
-+import git
-+from git import Repo
-+import logging
-+import semver
-+from semver import VersionInfo
-+import datetime
-+import tempfile
-+import shutil
-```
-
-
```

## 1.0.0 - 2023-10-05
- release to prod

### Diff:
```
diff --git a/CHANGELOG.md b/CHANGELOG.md
new file mode 100644
index 0000000..9298485
--- /dev/null
+++ b/CHANGELOG.md
@@ -0,0 +1,2 @@
+

+## 0.0.1 - 2023-10-05

```


## 0.0.1 - 2023-10-05
