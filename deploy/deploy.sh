#!/bin/bash
docker login -u "$DOCKERLOGIN" -p "$DOCKERPW"
docker push recast/recastatlas:$TRAVIS_BRANCH $PWD

