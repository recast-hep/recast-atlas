
#!/bin/bash
echo "login to Docker Hub"
docker login -u "$DOCKERLOGIN" -p "$DOCKERPW"
echo "show images"
docker images
echo "push to Docker Hub"
docker push recast/recastatlas:$TRAVIS_BRANCH

