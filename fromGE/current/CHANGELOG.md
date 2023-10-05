
## 4.0.0 - 2023-10-05
- something changed
- it was the code

### Diff:
```
diff --git a/fromGE/current/git-helper-15.py b/fromGE/current/git-helper-15.py
index d419bf4..6e56da9 100644
--- a/fromGE/current/git-helper-15.py
+++ b/fromGE/current/git-helper-15.py
@@ -9,0 +10 @@ import tempfile
+import shutil
@@ -489,5 +489,0 @@ def tag_version(repo, latest_tag):
-import datetime
-import os
-import shutil
-
-
@@ -495 +491,4 @@ def update_changelog(version, diff):
-    temp_file = "CHANGELOG_TEMP.md"
+    cwd = os.getcwd()
+    changelog_path = os.path.join(cwd, 'CHANGELOG.md')
+    temp_file = os.path.join(cwd, "CHANGELOG_TEMP.md")
+    
@@ -498,3 +497,3 @@ def update_changelog(version, diff):
-            # Check if CHANGELOG.md exists
-            if os.path.exists('CHANGELOG.md'):
-                with open('CHANGELOG.md', 'r') as original:
+            # Check if CHANGELOG.md exists in the CWD
+            if os.path.exists(changelog_path):
+                with open(changelog_path, 'r') as original:
@@ -515 +514 @@ def update_changelog(version, diff):
-                print(f"{ANSWER_TEXT}CHANGELOG.md not found. Creating a new one.{RESET_TEXT}")
+                print(f"{ANSWER_TEXT}CHANGELOG.md not found in the current working directory. Creating a new one.{RESET_TEXT}")
@@ -519,2 +518,2 @@ def update_changelog(version, diff):
-        shutil.move(temp_file, 'CHANGELOG.md')
-        print(f"{ANSWER_TEXT}CHANGELOG.md has been updated with version {version} and associated changes.{RESET_TEXT}")
+        shutil.move(temp_file, changelog_path)
+        print(f"{ANSWER_TEXT}CHANGELOG.md in the current working directory has been updated with version {version} and associated changes.{RESET_TEXT}")
@@ -524,0 +524,2 @@ def update_changelog(version, diff):
+
+
```


## 3.0.0 - 2023-10-05
