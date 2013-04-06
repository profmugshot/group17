
#!/bin/bash

echo "- git:"
git reset --hard
git pull
echo "Pulling git..."
echo
echo "- chmod:"
chmod 755 www -R
echo "done."
