# To start the demo:
kubectl scale deployment -n streaming-demo kafka-producer --replicas=1
kubectl scale deployment -n streaming-demo kafka-consumer --replicas=1

# To stop the demo
kubectl scale deployment -n streaming-demo kafka-producer --replicas=0
kubectl scale deployment -n streaming-demo kafka-consumer --replicas=0

# Check status
kubectl get deployments -n streaming-demo
kubectl get pods -n streaming-demo