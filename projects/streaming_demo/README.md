# To start the demo:
sed -i 's/replicas: 0/replicas: 1/' ~/repos/k8s-data-platform/projects/streaming_demo/k8s/producer-deployment.yaml
sed -i 's/replicas: 0/replicas: 1/' ~/repos/k8s-data-platform/projects/streaming_demo/k8s/consumer-deployment.yaml

git add .
git commit -m "Start streaming demo"
git push

# To stop the demo
sed -i 's/replicas: 1/replicas: 0/' ~/repos/k8s-data-platform/projects/streaming_demo/k8s/producer-deployment.yaml
sed -i 's/replicas: 1/replicas: 0/' ~/repos/k8s-data-platform/projects/streaming_demo/k8s/consumer-deployment.yaml

git add .
git commit -m "Stop streaming demo"
git push

# Check status
kubectl get deployments -n streaming-demo
kubectl get pods -n streaming-demo