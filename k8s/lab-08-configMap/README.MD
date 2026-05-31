# Kubernetes ConfigMap

A **ConfigMap** is a Kubernetes object used to manage configuration separately from the container image.

This allows the same container image to run in different environments such as:

* Development (`dev`)
* Staging (`staging`)
* Production (`prod`)

ConfigMaps are **environment-agnostic**.

Example ConfigMaps:

```bash
app-config-dev
app-config-prod
```

You can then attach the appropriate ConfigMap to a Pod or Deployment depending on the environment.

---

# Why Use ConfigMaps?

ConfigMaps help you:

* Separate configuration from application code
* Reuse the same container image across environments
* Store configuration files
* Store environment variables
* Mount configuration into Pods

---

# Important Note About Dynamic Updates

You can inject different versions of a file (for example `index.html`) using a ConfigMap.

However, switching environments is **not dynamic at runtime**.

Instead:

1. Update the existing ConfigMap
2. Re-apply or restart the Pod/Deployment

---

# `kube-root-ca.crt` ConfigMap

Kubernetes automatically creates a ConfigMap named:

```bash
kube-root-ca.crt
```

inside every namespace.

## Purpose

It contains the cluster Root Certificate Authority (CA) certificate.

This allows Pods to securely communicate with the Kubernetes API Server over HTTPS using TLS.

### Used For

* TLS validation
* Verifying the identity of the API server
* Secure service account communication

### Mounted Inside Pods

```bash
/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
```

---

# ConfigMap Lab-01 — `index.html`

## Goal

Inject different versions of an `index.html` file using a ConfigMap.

---

## Step 1 — Create `index.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>Env</title>
</head>
<body>
  <h1>Hello from ConfigMap Dev!</h1>
</body>
</html>
```

---

## Step 2 — Create the ConfigMap

### View existing ConfigMaps

```bash
kubectl get configmap
kubectl describe configmap
```

### Create ConfigMap from file

```bash
kubectl create configmap html-config --from-file=index.html
```

### Verify

```bash
kubectl get configmap
kubectl describe configmap
kubectl get configmap -o yaml
```

> Compare the YAML output before and after adding `index.html`.

---

## Step 3 — Inspect `kube-root-ca.crt`

```bash
kubectl describe configmap kube-root-ca.crt
```

---

## Step 4 — Mount the ConfigMap into a Pod

Create `pod-with-configmap.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: html-pod

spec:
  containers:
    - name: nginx
      image: nginx

      volumeMounts:
        - name: html-volume
          mountPath: /usr/share/nginx/html/index.html
          subPath: index.html

  volumes:
    - name: html-volume
      configMap:
        name: html-config
```

---

## Step 5 — Deploy the Pod

```bash
kubectl apply -f pod-with-configmap.yaml
```

---

## Step 6 — Port Forward

```bash
kubectl port-forward pod/html-pod 8080:80
```

Open in browser:

```text
http://localhost:8080/
```

---

# Update the ConfigMap (Prod Version)

## New `index.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>Env</title>
</head>
<body>
  <h1>Hello from ConfigMap Prod!</h1>
</body>
</html>
```

---

## Update the Existing ConfigMap

```bash
kubectl create configmap html-config \
  --from-file=index.html \
  --dry-run=client -o yaml | kubectl apply -f -
```

---

## Restart the Pod

```bash
kubectl delete pod html-pod
kubectl apply -f pod-with-configmap.yaml
```

---

## Port Forward Again

```bash
kubectl port-forward pod/html-pod 8080:80
```

Open:

```text
http://localhost:8080/
```

You should now see:

```text
Hello from ConfigMap Prod!
```

---

# ConfigMap Lab-02 — `app.properties`

## Step 1 — Create `config/app.properties`

```properties
# app.properties

app.name=MyKubeApp
app.environment=development
```

---

## Step 2 — Create ConfigMap from File

```bash
kubectl create configmap app-config --from-file=config/app.properties
```

Verify:

```bash
kubectl describe configmap app-config
```

---

## Step 3 — Mount ConfigMap into a Pod

Create `configmap-pod-properties.yaml`

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: app-with-config

spec:
  containers:
    - name: myapp
      image: busybox

      command:
        - "sh"
        - "-c"
        - "cat /config/app.properties && sleep 3600"

      volumeMounts:
        - name: config-volume
          mountPath: /config

  volumes:
    - name: config-volume
      configMap:
        name: app-config
```

---

## Step 4 — Deploy the Pod

```bash
kubectl apply -f configmap-pod-properties.yaml
```

---

## Step 5 — Verify Mounted File

```bash
kubectl exec app-with-config -- cat /config/app.properties
```

---

# Useful Commands

## View ConfigMaps

```bash
kubectl get configmap
```

---

## Create ConfigMap

```bash
kubectl create configmap app-config --from-file=config/app.properties
```

---

## Describe ConfigMap

```bash
kubectl describe configmap app-config
```

---

## Apply YAML

```bash
kubectl apply -f configmap-pod-properties.yaml
```

---

## Read Mounted File

```bash
kubectl exec app-with-config -- cat /config/app.properties
```

---

## Delete All ConfigMaps

```bash
kubectl delete configmap --all
```

---

# ConfigMap Lab-03 — Switch Between Environments

This lab combines:

* `app.properties`
* `index.html`
* Environment switching

## Edit the ConfigMap

```bash
kubectl edit configmap app-config
```

> Edit the values multiple times to verify changes are applied correctly.

---

# Summary

ConfigMaps allow Kubernetes applications to:

* Separate configuration from code
* Reuse the same container image in multiple environments
* Inject files and environment variables into Pods
* Update configuration without rebuilding images

They are one of the most important Kubernetes resources for managing application configuration cleanly and securely.
