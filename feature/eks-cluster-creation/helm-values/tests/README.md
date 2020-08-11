## Testing the autoscaling feature
Short description how to test autoscaling in AWS


#### Requirements:
- working deployment of EKS cluster
- kubectl command

#### Test:
- Apply deployment with simple php-apache image:  
``` kubectl apply -f https://k8s.io/examples/application/php-apache.yaml```
- Create horizontal pod autoscale based on CPU/Memory or some other from eg. prometheus metrics. Server metrics is installed by default in AKS version higher then 1.10  
```kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=50 ```
- Create deployment with a containers in order to increase load on nodes using infinite loop of queries to the php-apache service created in previous point.:  
```kubectl apply -f helm-values/tests/load-generator.yaml```
- Increase load as needed   
```kubectl scale deployment load-generator --replicas=5```
- Check the effect using monitoring tools:  
```kubectl get hpa```