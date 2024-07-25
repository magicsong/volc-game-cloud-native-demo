#!/bin/bash

# Set the image name and tag
IMAGE_NAME=$1
TAG=$2

# Build the Docker image
docker build -t $IMAGE_NAME:$TAG . -f veloren_wrapper.Dockerfile

# Push the Docker image to a registry
docker push $IMAGE_NAME:$TAG