# Purpose: Makefile for scanner-batch
# Author: Michal Maxian

# build docker image
build:
	docker build -t scanner-batch-image .

# push to dockerhub
push:
	docker tag scanner-batch-image mmaxian/scanner-batch-image:latest
	docker push mmaxian/scanner-batch-image:latest

# deploy to microk8s
deploy:
	microk8s kubectl apply -f scanner-batch-deployment.yml

# delete from microk8s
clean:
	microk8s kubectl delete -f scanner-batch-deployment.yml
	docker rmi scanner-batch-image

# clean, build, push and deploy
redeploy: clean build push deploy
