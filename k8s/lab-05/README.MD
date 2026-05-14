PHP


kubectl delete all --all
kubectl get deployments
kubectl apply -f autoscaling-hpa.yaml
kubectl get deployments
kubectl get pods
kubectl get svc

kubectl autoscale deployment php-apache --cpu-percent=10 --min=1 --max=2
kubectl get hpa
kubectl get hpa --watch
new terminal
#kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never --
while sleep 0.01; do wget -q -O- http://php-apache; done

kubectl run -i --tty load-generator --image=busybox /bin/sh

back to priviouse

kubectl edit hpa php-apache

kubectl get hpa
kubectl get hpa
kubectl apply -f autoscaling-hpa.yaml
kubectl get nodes
kubectl get deployments

Generate load to trigger scaling

In a new terminal run the following command to drop into a shell on a new container

kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=5
  577  kubectl get hpa
  578  kubectl delete hpa php-apache
  579  kubectl get hpa
  580  kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=5
  581  kubectl get hpa
  582  kubectl delete all --all
  583  kubectl get pod
  584  kubectl get svc
  585  history
  
  
  n the previous terminal watch the changes of HPA with the following command

kubectl get hpa --watch

You can check the running pods as well

kubectl get pods
Edit HPA configuration

Edit the HPA resource to increment the maxReplicas up to 50 and the minReplicas to 3

kubectl edit hpa php-apache

Watch the HPA with the following command to see how the application is beeing scaled

kubectl get hpa --watch

You can check the running pods as well

kubectl get pods
Check current cluster nodes

Check the current nodes of your cluster and see that the nodes have been added

kubectl get nodes


kubectl run -i --tty load-generator --image=busybox /bin/sh while true; do wget -q -O - http://php-apache; done

kubectl run -i --tty load-generator --image=busybox /bin/sh | while true; do wget -q -O - http://php-apache; done
