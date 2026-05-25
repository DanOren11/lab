Kubernetes StatefulSet
Cleanup
List existing resources
kubectl get all
Delete the PVC's
kubectl delete pvc --all
Delete another resources
kubectl delete all --all
List existing resources
kubectl get all
Manages stateful applications
Used for apps needing:

Stable pod names
Persistent storage
Ordered startup/shutdown
Stable network identity
For Examples:

MySQL
PostgreSQL
MongoDB
Kafka
Elasticsearch
ETC...
Summary step 01 - 09
Stable pod names web-0 always stays web-0
Persistent storage Each Pod keeps data
Ordered deployment Pods start sequentially
Ordered scaling Controlled startup/shutdown
Rolling updates Safe sequential updates
StatefulSets provide stable identity and persistent storage for stateful Kubernetes applications.
Step 01
Create the a headless service for the StatefulSet
kubectl create -f service.yaml
kubectl get svc

Step 02
Create StatefulSet
kubectl create -f statefulset.yaml
kubectl get statefulsets
Step 03
Inspect the StatefulSet pods
kubectl get pods -l="app=nginx"
kubectl get statefulsets
	# Output
web-0
web-1
web-2
Step 04
Inspect the StatefulSet's PV, PVCs and storageclass
kubectl get pv
kubectl get pv | awk '{print $1,"        "$5 }'

	# Output
NAME         RECLAIM
pvc-59780f77-fa3d-45a6-95db-1ae91f20d0a1         Bound
pvc-66aeb99e-087a-4249-a3ec-39e36404a074         Bound
pvc-86759a88-c071-4b21-a97b-3240e410e95b         Bound
pvc-b413fbb7-e1ff-48df-828a-b9e159a5d4b0         Bound
pvc-fe070e7b-b5ee-4c43-813a-4dad34b4261b         Bound

kubectl get storageclass
kubectl get pvc | awk '{print $1,"        "$3 }'
	#output
NAME         VOLUME
www-web-0         pvc-86759a88-c071-4b21-a97b-3240e410e95b
www-web-1         pvc-fe070e7b-b5ee-4c43-813a-4dad34b4261b
www-web-2         pvc-66aeb99e-087a-4249-a3ec-39e36404a074
www-web-3         pvc-59780f77-fa3d-45a6-95db-1ae91f20d0a1
www-web-4         pvc-b413fbb7-e1ff-48df-828a-b9e159a5d4b0

Step 05
Scale Up StatefulSet, Edit StatefulSet
Change from replicas 3 to replicas: 5
kubectl edit statefulset web
kubectl get pods -l="app=nginx" --watch

 # Output
NAME    READY   STATUS    RESTARTS   AGE
web-0   1/1     Running   0          5h44m
web-1   1/1     Running   0          5h44m
web-2   1/1     Running   0          9s
web-3   1/1     Running   0          8s
web-4   1/1     Running   0          7s

 # Verify Pods
kubectl get pods -l="app=nginx"
 # Verify StatefulSet
kubectl get statefulset web
Step 06
Scale down StatefulSet, Edit StatefulSet
Change from replicas 5 to replicas: 2
kubectl edit statefulset web
kubectl get pods -l="app=nginx" --watch

	# Output
NAME    READY   STATUS    RESTARTS   AGE
web-0   1/1     Running   0          5h51m
web-1   1/1     Running   0          5h51m

# Pods terminate in reverse order:
	# web-4 deleted first
	# web-3 deleted next
Step 07
Update StatefulSet, Edit StatefulSet image
Replace from gcrcontainer/nginx-slim:0.20 to gcrcontainer/nginx-slim:0.26
kubectl edit statefulset web

Step 08
Watch rollout
kubectl rollout status statefulset web

Updates occur one Pod at a time:
Ordered rolling update
web-0
web-1
web-2

 # Verify images
kubectl describe pod web-0 | grep Image:
kubectl describe pod web-1 | grep Image:

Expected:

gcrcontainer/nginx-slim:0.26

Step 09
Rollback StatefulSet
kubectl rollout undo statefulset web

	# Restores previous version.
kubectl rollout status statefulset web
	# Verify rollback image
kubectl describe pod web-0 | grep Image:
kubectl describe pod web-1 | grep Image:

	# Output
    gcrcontainer/nginx-slim:0.20
