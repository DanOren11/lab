Hands-On – Exercise 01: My First Pod
Create namespace with name ns-my-first-pod based on existing cluster
Create YAML file my-first-pod.yaml based on image nginx:latest
Apply the pod to the namespace ns-my-first-pod
Check that the pod is running correctly under the namespace
Bonus
How can we get the IP and Node where the pod is running?
How can we get the logs of the pod?
Solution – Exercise 01
Cleanup (if needed)
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)

kubectl get pod
kubectl delete all --all
kubectl delete pod <pod-name> --grace-period=0 --force
kubectl get ns
kubectl delete namespace ns-my-first-pod
Create Namespace
kubectl create ns ns-my-first-pod
kubectl get ns
OR via YAML
cat << EOF > ns-my-first-pod.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ns-my-first-pod
EOF

kubectl apply -f ns-my-first-pod.yaml
Set namespace context (optional but useful)
kubectl config set-context --current --namespace=ns-my-first-pod
kubectl config get-contexts
Create Pod YAML
cat << EOF > my-first-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
EOF
Apply Pod
kubectl apply -f my-first-pod.yaml
Check Resources
kubectl get pod
kubectl get ns
kubectl get svc
kubectl get rs
Inspect Pod
kubectl describe pod my-first-pod
Get Logs
kubectl logs my-first-pod
Bonus Answers
Get Pod IP and Node
kubectl get pod -o wide

or more detailed:

kubectl describe pod my-first-pod

Look for:

IP
Node
Get Pod Logs
kubectl logs my-first-pod
