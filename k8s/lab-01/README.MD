Installation of K8S cluster via kind
PreRequisite: install Docker Desktop following: devops-docker-make-it-happen/lesson-docker/practice-01

Go to the link and install it step by step following the instruction: https://kind.sigs.k8s.io/docs/user/quick-start/ Note: you can install kind via section Installing with go install its including kind as part of Go installtion

Go to the cli of PowerShell and check the version of kind

kind version
kind info
kubectl version
Basic k8s commands:
list of cluster, probably nothing will appear
kind get clusters
kubectl get nodes
kubectl get all --all-namespaces
  # for cleanup
kubectl config delete-context kind-example
Create your first kind cluster
kind create cluster --name kind-01 --config kind-config.yaml
kind get clusters
# probably kind-01 cluster will appear
Shortcut options
echo 'source <(kubectl completion bash)' >>~/.bash_profile
echo 'alias k=kubectl' >>~/.bash_profile
echo 'complete -F __start_kubectl k' >>~/.bash_profile
source ~/.bash_profile
