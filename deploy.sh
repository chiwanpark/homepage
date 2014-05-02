#!/usr/bin/env bash

git clone --quite --branch=master https://${GH_TOKEN}@github.com/chiwanpark.github.io github
cd github
rsync -rv --exclude=.git ../_build/* .
git add -f .
git commit -m "Travis build $TRAVIS_BUILD_NUMBER"
git push -fq origin master
echo -e "Deploy completed."
