#!/bin/sh

setup_git() {
    # cat output.txt
    cd $HOME
    git config --global user.email ${GH_EMAIL}
    git config --global user.name ${GH_USERNAME}
    git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/${GH_USERNAME}/${GH_REPONAME}.git gh-pages
    cd gh-pages
    echo "changed to gh-pages"
    pwd
}

update_input() {
    cat /home/travis/build/${GH_USERNAME}/${GH_REPONAME}/input.txt > input.txt          # get input from `master`
}

setup_git
update_input
