# Kubernetes HPA Autoscaling Demo

## Cleanup Existing Resources

```bash
kubectl delete all --all
```

## Verify Cluster State

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl get nodes
```

## Deploy Application

```bash
kubectl apply -f autoscaling-hpa.yaml
```

## Verify Deployment

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
```

# Create Horizontal Pod Autoscaler (HPA)

```bash
kubectl autoscale deployment php-apache --cpu-percent=10 --min=1 --max=2
```

## Check HPA

```bash
kubectl get hpa
```

## Watch HPA Changes

```bash
kubectl get hpa --watch
```

# Generate Load to Trigger Scaling

## Open a New Terminal

### Start BusyBox Shell

```bash
kubectl run -i --tty load-generator --image=busybox /bin/sh
```

### Run Continuous Load

```sh
while sleep 0.01; do wget -q -O- http://php-apache; done
```

---

## Alternative One-Liner Load Generator

```bash
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while true; do wget -q -O - http://php-apache; done"
```

# Back to Previous Terminal

## Watch HPA Scaling

```bash
kubectl get hpa --watch
```

## Check Running Pods

```bash
kubectl get pods
```

# Edit HPA Configuration

```bash
kubectl edit hpa php-apache
```

Update:

- `maxReplicas: 50`
- `minReplicas: 3`

## Watch HPA Again

```bash
kubectl get hpa --watch
```

## Check Pods

```bash
kubectl get pods
```

## Check Cluster Nodes

```bash
kubectl get nodes
```

# Recreate HPA with Different Limits

## Delete Existing HPA

```bash
kubectl delete hpa php-apache
```

## Verify HPA Deletion

```bash
kubectl get hpa
```

## Create New HPA

```bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=5
```

## Verify New HPA

```bash
kubectl get hpa
```

# Reapply HPA Manifest

```bash
kubectl apply -f autoscaling-hpa.yaml
```

# Monitor Resources

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl get nodes
```

# Additional Monitoring Commands

## Watch Pods Scaling

```bash
kubectl get pods -w
```

## Watch Deployments

```bash
kubectl get deployments -w
```

## Watch Nodes

```bash
kubectl get nodes -w
```

# Troubleshooting Commands

## Describe HPA

```bash
kubectl describe hpa php-apache
```

## Describe Deployment

```bash
kubectl describe deployment php-apache
```

## Describe Pods

```bash
kubectl describe pods
```

## View Logs

```bash
kubectl logs deployment/php-apache
```

## Check Metrics Server

```bash
kubectl get apiservices | grep metrics
```

## Verify Metrics API

```bash
kubectl top pods
kubectl top nodes
```

## Restart Deployment

```bash
kubectl rollout restart deployment php-apache
```

## Check Rollout Status

```bash
kubectl rollout status deployment/php-apache
```

# Cleanup

## Delete Load Generator

```bash
kubectl delete pod load-generator
```

## Delete All Resources

```bash
kubectl delete all --all
```

## Verify Cleanup

```bash
kubectl get all
```
