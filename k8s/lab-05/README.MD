# Kubernetes HPA Autoscaling Demo

## Clean Existing Resources

```bash
kubectl delete all --all
Verify Cluster State
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl get nodes
Deploy Application
kubectl apply -f autoscaling-hpa.yaml

Verify deployment:

kubectl get deployments
kubectl get pods
kubectl get svc
Create Horizontal Pod Autoscaler (HPA)
Initial HPA Configuration
kubectl autoscale deployment php-apache --cpu-percent=10 --min=1 --max=2

Check HPA:

kubectl get hpa

Watch HPA changes live:

kubectl get hpa --watch
Generate Load to Trigger Scaling
Open a New Terminal
Option 1 — Interactive BusyBox Shell
kubectl run -i --tty load-generator --image=busybox /bin/sh

Inside the container run:

while sleep 0.01; do wget -q -O- http://php-apache; done
Option 2 — One-Liner Load Generator
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- \
/bin/sh -c "while true; do wget -q -O - http://php-apache; done"
Monitor Autoscaling

Back in the previous terminal:

kubectl get hpa --watch

Check running pods:

kubectl get pods
Edit HPA Configuration

Edit the HPA resource:

kubectl edit hpa php-apache

Update:

maxReplicas → 50
minReplicas → 3

Watch scaling behavior again:

kubectl get hpa --watch

Check running pods:

kubectl get pods

Check cluster nodes:

kubectl get nodes
Recreate HPA with New Limits

Delete the current HPA:

kubectl delete hpa php-apache

Verify deletion:

kubectl get hpa

Create a new HPA:

kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=5

Verify:

kubectl get hpa
Reapply HPA Manifest
kubectl apply -f autoscaling-hpa.yaml

Verify resources:

kubectl get deployments
kubectl get pods
kubectl get svc
kubectl get nodes
Cleanup

Delete all resources:

kubectl delete all --all

Verify cleanup:

kubectl get pod
kubectl get svc
Useful Commands Reference
Watch HPA
kubectl get hpa --watch
Check Pods
kubectl get pods
Check Nodes
kubectl get nodes
View Deployments
kubectl get deployments
---

# Monitor Cluster Scaling

## Watch HPA Metrics

```bash
kubectl get hpa --watch
```

---

## Watch Pods Scaling

```bash
kubectl get pods -w
```

---

## Watch Deployments

```bash
kubectl get deployments -w
```

---

## Watch Nodes

```bash
kubectl get nodes -w
```

---

# Debugging Commands

## Describe HPA

```bash
kubectl describe hpa php-apache
```

---

## Describe Deployment

```bash
kubectl describe deployment php-apache
```

---

## Describe Pods

```bash
kubectl describe pods
```

---

## View Logs

```bash
kubectl logs deployment/php-apache
```

---

# Cleanup Load Generator

Delete load generator pod:

```bash
kubectl delete pod load-generator
```

---

# Full Cleanup

Delete all resources:

```bash
kubectl delete all --all
```

Verify cleanup:

```bash
kubectl get all
```

---

# Useful Troubleshooting Commands

## Check Metrics Server

```bash
kubectl get apiservices | grep metrics
```

---

## Verify Metrics API

```bash
kubectl top pods
kubectl top nodes
```

---

## Restart Deployment

```bash
kubectl rollout restart deployment php-apache
```

---

## Check Rollout Status

```bash
kubectl rollout status deployment php-apache
```
