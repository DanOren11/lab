Hands-On - Exercise 01 - my first Pod
Create namespace with name ns-my-first-pod based on exist cluster​
Create yaml file my-first-pod.yaml based on image latest of nginx​
Apply the pod​ to the namespace ns-my-first-pod
Check that the pod is running correctly under test ns
Bonus​
How can we get the IP and Node that the pod running ?​
How can we get the log of pod ?
Solution - Exercise 01
Cleanup if needed
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)

kubectl get pod
kubectl delete all --all
kubectl delete pod <pod-name> --grace-period=0 --force
kubectl get ns
kubectl delete namespace ns-my-first-pod
Create ns and Pod
Go to Practice-01, in case you should create cluster
kubectl get pod
kubectl get ns
kubectl create ns ns-my-first-pod

  # other option is via yaml file
cat << EOF > ~/ns-my-first-pod.yaml 
apiVersion: v1
kind: Namespace
metadata:
  name: test
EOF

kubectl apply -f ns-my-first-pod.yaml

kubectl get ns
kubectl config set-context --current --namespace=ns-my-first-pod
kind get clusters
kubectl config get-contexts
kubectl config get-contexts | awk '{print $1,$5}'

cat << EOF > ~/my-first-pod.yaml​
  Insert the contant of my-first-pod.yaml​ copy to nodepad and run it via cli of gitbash
EOF


kubectl apply -f my-first-pod.yaml​
kubectl get pod
kubectl get svc
kubectl get rs
kubectl describe pod example-pod​
kubectl logs example-pod​
