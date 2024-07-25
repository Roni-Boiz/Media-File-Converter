```
$ conda create --name venv python=3.8

$ conda create -p ./venv python=3.8

$ python -m venv venv
```
```
$ source ./venv/bin/activate or $ conda activate ./venv

$ env | grep VIRTUAL

$ export MYSQL_HOST=localhost

$ printenv

$ pip freeze > requirements.txt
```

```
minikube start

minikube ip

minikube addons list

minikube addons enable ingress
```

```
$ sudo vim /etc/hosts

Add following two lines
<minikube_ip>	kubernetes-mp3converter.com
<minikube_ip>	kubernetes-rabbitmq-manager.com
```

When testing scale services to 1
```
kubectl scale deployment --replicas=1 gateway-deployment
```