docker stop wisdom
docker rm wisdom
docker rmi wisdom-layer-app

docker build -t wisdom-layer-app .
