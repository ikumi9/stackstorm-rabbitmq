#!/bin/bash
# echo "$1, StackStorm!"

cd

git clone $1

repo_name=$(echo $1 | awk -F / '{print $NF}' | sed 's/.git//')

cd $repo_name

ls 