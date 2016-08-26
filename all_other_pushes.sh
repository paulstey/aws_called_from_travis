#!/bin/sh


setup_git() {
    cat output.txt
    cd $HOME
    git config --global user.email ${GH_EMAIL}
    git config --global user.name ${GH_USERNAME}
    git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/${GH_USERNAME}/${GH_REPONAME}.git gh-pages
    cd gh-pages
}

update_readme() {
    # cat /home/travis/build/${GH_USERNAME}/${GH_REPONAME}/output.txt > README.md
    cat output.txt > README.md

}

commit_files() {
    git add --force .
    git commit --message "Travis build: $TRAVIS_BUILD_NUMBER [ci skip]"
}

upload_files() {
    git push --quiet origin gh-pages
}

setup_git
update_readme
commit_files
upload_files
