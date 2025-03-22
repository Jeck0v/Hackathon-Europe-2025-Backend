#!/bin/bash

set -e

if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Please install it."
    exit 1
fi

echo "Starting Minikube..."
minikube start --nodes=3 --driver=docker

echo " Activating Ingress..."
minikube addons enable ingress

echo "Cluster Minikube operational, infos:"
minikube status
kubectl get nodes
