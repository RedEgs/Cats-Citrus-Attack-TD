#! /bin/bash


cd ~/Documents/Cats-Citrus-Attack-TD/ApplicationEngine/redengine/
# Get the current directory
current_dir=$(pwd)

# Get the parent directory
parent_dir=$(dirname "$current_dir")

# Get the grandparent directory
grandparent_dir=$(dirname "$parent_dir")

source $grandparent_dir/bin/activate
nvim engine_main.py


 


