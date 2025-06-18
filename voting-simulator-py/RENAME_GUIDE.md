# GitHub Repository Rename Guide

To rename your GitHub repository from "Andalusia Lore" to "Weighted Voting System", follow these steps:

1. Go to your repository on GitHub: https://github.com/YOUR-USERNAME/Andalusia-Lore

2. Click on the "Settings" tab (usually on the right side of the repository navigation menu)

3. Under the "General" section, you'll find the Repository name field

4. Change the name from "Andalusia Lore" to "Weighted-Voting-System"

5. Scroll down and click the "Rename" button

6. After renaming on GitHub, update your local repository with these commands:
   ```
   git remote set-url origin https://github.com/YOUR-USERNAME/Weighted-Voting-System.git
   ```

7. Verify the change with:
   ```
   git remote -v
   ```

8. You may need to update any hardcoded references to the old repository name in your code or documentation.

Note: Links to the old repository name will automatically redirect to the new name, so existing links should continue to work.
