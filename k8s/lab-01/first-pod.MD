That happens because Markdown renders everything as a single paragraph when there are **missing blank lines or improper code block formatting**.

Here is a **GitHub-safe README version** that will NOT collapse into one line when pasted:

---

````md
# Hands-On Exercise 01 – My First Pod

## Objective

- Create a namespace `ns-my-first-pod`
- Deploy an NGINX Pod using `nginx:latest`
- Run the Pod inside the created namespace
- Verify the Pod is running correctly

---

## Bonus

- How to get the Pod IP and Node?
- How to view Pod logs?

---

# Solution

## 1. Cleanup (Optional)

Use only if you need a clean environment:

```bash
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)

kubectl get pod
kubectl delete all --all
kubectl delete pod <pod-name> --grace-period=0 --force

kubectl get ns
kubectl delete namespace ns-my-first-pod
````

---

## 2. Create Namespace

### Option A – Command

```bash
kubectl create ns ns-my-first-pod
kubectl get ns
```

### Option B – YAML

```bash
cat << EOF > ns-my-first-pod.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ns-my-first-pod
EOF

kubectl apply -f ns-my-first-pod.yaml
kubectl get ns
```

---

## 3. Set Namespace Context (Optional)

```bash
kubectl config set-context --current --namespace=ns-my-first-pod
kubectl config get-contexts
```

---

## 4. Create Pod YAML

```bash
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
```

---

## 5. Deploy Pod

```bash
kubectl apply -f my-first-pod.yaml
```

---

## 6. Verify Resources

```bash
kubectl get pod
kubectl get ns
kubectl get svc
kubectl get rs
```

---

## 7. Describe Pod

```bash
kubectl describe pod my-first-pod
```

---

## 8. View Logs

```bash
kubectl logs my-first-pod
```

---

# Bonus

## Get Pod IP and Node

```bash
kubectl get pod -o wide
```

or

```bash
kubectl describe pod my-first-pod
```

---

## Useful Commands

```bash
kubectl get pods
kubectl get ns
kubectl logs <pod-name>
kubectl get pod -o wide
```

