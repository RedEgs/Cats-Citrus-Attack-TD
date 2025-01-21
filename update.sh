git add *

read -p "Commit Description: " description
n=${#description}
l=1

if [ "$n" -lt "$l" ]; then
    git commit -m "$(date +%F) (Arch Laptop)"
else
    git commit -m "${description} (Arch Laptop)"
fi
git push -u origin master
