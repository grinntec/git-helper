
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
