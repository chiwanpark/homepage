#!/usr/bin/env bash

git clone --quiet --branch=master https://${GH_TOKEN}@github.com/chiwanpark/chiwanpark.github.io master > /dev/null
cd master
rsync -rv --exclude=.git ../_build/* .
git add -f .
git commit -m "Travis build $TRAVIS_BUILD_NUMBER"
git push -fq origin master > /dev/null
echo -e "Deploy completed."
