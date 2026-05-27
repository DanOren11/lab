
K8s ConfigMap
Configmap It’s just a way to manage configuration independent of the container image using a ConfigMap any cluster environment (dev, staging, prod)

ConfigMaps are environment-agnostic.

You can create different ConfigMaps for different environments:

app-config-dev
app-config-prod
Then use the appropriate one in each Pod depending on the environment

You can inject different versions of a file (like index.html) using a single ConfigMap but not dynamically at runtime per environment Instead, you update the existing ConfigMap with the new content and re-apply the Pod or Deployment

The kube-root-ca.crt in ConfigMap is Allow Pods to securely communicate with the Kubernetes API server using TLS its automatically created in each namespace by the Kubernetes control plane It contains the cluster's root Certificate Authority (CA) certificate and it's used by workloads (Pods) inside the cluster to securely communicate with the Kubernetes API server over HTTPS

the Purpose is TLS validation: Applications inside Pods can verify the identity of the API server. Secure service account token usage: Used in conjunction with the
Mount the CA cert at /var/run/secrets/kubernetes.io/serviceaccount/ca.crt inside Pods.
Configmap Lab-01 - step by step index.html
Inject different versions of a index.html file using a single ConfigMap but not dynamically at runtime per environment

Instead, you update the existing ConfigMap with the new content and re-apply the Pod

Create index.html file

<!DOCTYPE html>
<html>
<head><title>Env</title></head>
<body><h1>Hello from ConfigMap Dev!</h1></body>
</html>
Create the ConfigMap
kubectl get configmap
kubectl describe configmap
kubectl create configmap html-config --from-file=index.html
kubectl get configmap
kubectl describe configmap
kubectl get configmap -o yaml
  # See the data diif with and without index.html data
kubectl describe configmap kube-root-ca.crt
kubectl describe configmap kube-root-ca.crt

Mount the ConfigMap in a Pod, see the example pod-with-configmap.yaml
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
Aplly the pod
kubectl apply -f pod-with-configmap.yaml
Port forward to the Browser
kubectl port-forward pod/html-pod 8080:80
Go to the Browser

http://localhost:8080/
Update the ConfigMap with a new version (Prod)

<!DOCTYPE html>
<html>
<head><title>Env</title></head>
<body><h1>Hello from ConfigMap Prod!</h1></body>
</html>
Update the ConfigMap
kubectl create configmap html-config --from-file=index.html --dry-run=client -o yaml | kubectl apply -f -
Delete and recreate the Pod
kubectl delete pod html-pod
kubectl apply -f pod-with-configmap.yaml
Port forward to the Browser
kubectl port-forward pod/html-pod 8080:80
Go to the Browser
http://localhost:8080/
ConfigMap Lab-02 with app.properties
Create the /config/app.properties file ( see the file in config folder )
# app.properties
app.name=MyKubeApp
app.environment=development
Create a ConfigMap from the file
kubectl create configmap app-config --from-file=config/app.properties
kubectl describe configmap app-config
Use the ConfigMap in a config-pod-properties.yaml (mount as file)
apiVersion: v1
kind: Pod
metadata:
  name: app-with-config
spec:
  containers:
  - name: myapp
    image: busybox
    command: [ "sh", "-c", "cat /config/app.properties && sleep 3600" ]
    volumeMounts:
    - name: config-volume
      mountPath: /config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
Deploy the Pod
kubectl apply -f configmap-pod-properties.yaml
Check if the file is mounted
kubectl exec app-with-config -- cat config/app.properties
Usage commands
kubectl get configmap
kubectl create configmap app-config --from-file=app.properties
kubectl describe configmap app-config
kubectl apply -f configmap-pod-properties.yaml
kubectl exec app-with-config -- cat config/app.properties
kubectl delete configmap --all
ConfigMap Lab-03 all together app.properties, index.html and switch between env
Node - do it twise to makesure is edited
kubectl edit configmap app-config
