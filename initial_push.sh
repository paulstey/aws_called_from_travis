#!/bin/sh

# This script is called by the .yml file in this repo. It is meant to
# run on Travis-CI and push the updates (performed on Travis) back
# to the original Github repo. In particular, it pushes them back to
# the `gh-pages` branch of the repo.

setup_git() {
  git config --global user.email ${GH_EMAIL}
  git config --global user.name ${GH_USERNAME}
}

clean_up() {
    rm *.fna
    rm *.faa
    rm *_mismatch_ids.txt
}

commit_files() {
  git checkout -b gh-pages
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER [ci skip]"
}


upload_files() {
  git remote add origin-pages https://${GH_TOKEN}@github.com/${GH_USERNAME}/${GH_REPONAME}.git
  git push --quiet --set-upstream --force origin-pages gh-pages                                       
}

setup_git
clean_up
commit_files
upload_files
