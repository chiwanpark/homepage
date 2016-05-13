#!/usr/bin/env bash

if [ "$TRAVIS" == "true" ]; then
    git config --global user.email "chiwanpark@icloud.com"
    git config --global user.name "Chiwan Park"
fi

git clone --quiet --branch=master https://${GH_TOKEN}@github.com/chiwanpark/chiwanpark.github.io master > /dev/null
cd master
rsync -rv --delete --exclude=.git ../_build/ .
git add -f --all .
git commit -m "Travis build $TRAVIS_BUILD_NUMBER"
git push -fq origin master > /dev/null
echo -e "Deploy completed."
