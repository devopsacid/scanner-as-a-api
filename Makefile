# Purpose: Makefile for scanner-api
# Author: Michal Maxian

# build docker image
build:
	docker build -t scanner-api .

# push to dockerhub
push:
	docker tag scanner-api mmaxian/scanner-api:latest
	docker push mmaxian/scanner-api:latest

# deploy to microk8s
deploy:
	microk8s.kubectl apply -f ./k8s

# delete from microk8s
test:
	docker run -it --rm --name scanner-api scanner-api

# run locally
server:
	python3 scanner-api.py

# delete from microk8s
clean: 
	microk8s.kubectl delete -f ./k8s
	docker rmi scanner-api

# build, test and clean
redeploy: clean build push deploy
