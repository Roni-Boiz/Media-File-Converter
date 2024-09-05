# DevOps Project: video-converter
Converting mp4 videos to mp3 in a microservices architecture.

<!-- ## Architecture

<p align="center">
  <img src="./Project documentation/ProjectArchitecture.png" width="600" title="Architecture" alt="Architecture">
  </p> -->

## Deploying a Python-based Microservice Application on Minikube Kuerentes Cluster

### Introduction

This document provides a step-by-step guide for deploying a Python-based microservice application on Kubernetes (minikube). The application comprises four major microservices: `auth`, `converter`, `database` (MySQL and MongoDB), and `notification`.

### Prerequisites

Before you begin, ensure that the following prerequisites are met:

1. **Python:** Ensure that Python is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Install kubectl:** Install the latest stable version of `kubectl` on your system. You can find installation instructions [here](https://kubernetes.io/docs/tasks/tools/).

3. **Databases:** Set up MySQL and MongoDB for your application.

4. **k9s:** Install k9s to graphically view and manage running services (optional)

### High Level Flow of Application Deployment

Follow these steps to deploy your microservice application:

1. **MongoDB and MySQL Setup:** Create databases and enable automatic connections to them.

2. **RabbitMQ Deployment:** Deploy RabbitMQ for message queuing, which is required for the `converter`.

3. **Create Queues in RabbitMQ:** Before deploying the `converter`, create two queues in RabbitMQ: `mp3` and `video`.

4. **Deploy Microservices:**
   - **auth:** Navigate to the `auth` manifest folder and apply the configuration.
   - **gateway:** Deploy the `gateway`.
   - **converter:** Deploy the `converter`.
   - **notification:** Configure email for notifications and two-factor authentication (2FA). Make sure to provide your email and app-password in `notification/manifests/notification-secret.yaml`.

5. **Application Validation:** Verify the status of all components by running:
   ```bash
   $ kubectl get all
   ```

6. **Destroying the Infrastructure** 


### Low Level Steps

#### DNS Name resolution

- **Set DNS Names:**
    ```
    $ minikube start

    $ minikube ip

    $ minikube addons list

    $ minikube addons enable ingress
    ```

    ```
    $ sudo vim /etc/hosts

    Add following two lines to /etc/hosts file
    <minikube_ip>	kubernetes-mp3converter.com
    <minikube_ip>	kubernetes-rabbitmq-manager.com
    ```


#### Cluster Creation

### Apply the manifest files for each microservice:

- **Auth Service:**
  ```
  $ cd auth/manifests
  $ kubectl apply -f .
  ```

- **Gateway Service:**
  ```
  $ cd gateway/manifests
  $ kubectl apply -f .
  ```

- **Converter Service:**
  ```
  $ cd converter/manifests
  $ kubectl apply -f .
  ```

- **Notification Service:**
  ```
  $ cd notification/manifests
  $ kubectl apply -f .
  ```

- **rabbitmq Service:**
  ```
  $ cd rabbit/manifests
  $ kubectl apply -f .
  ```

### Application Validation

After deploying the microservices, verify the status of all components by running:

```
$ kubectl get all
```

### Notification Configuration


For configuring email notifications and two-factor authentication (2FA), follow these steps:

1. Go to your Gmail account and click on your profile.

2. Click on "Manage Your Google Account."

3. Navigate to the "Security" tab on the left side panel.

4. Enable "2-Step Verification."

5. Search for the application-specific passwords/app password. You will find it in the settings.

6. Click on "Other" and provide your name.

7. Click on "Generate" and copy the generated password.

8. Paste this generated password in `notification/manifests/notification-secret.yaml` along with your email.

Run the application through the following API calls:

# API Definition

- **Login Endpoint**
  ```http request
  POST http://kubernetes-mp3converter.com/login
  ```

  ```console
  curl -X POST http://kubernetes-mp3converter.com/login -u <mysql_user_email>:<mysql_user_password>
  ``` 
  Expected output: success!

- **Upload Endpoint**
  ```http request
  POST http://kubernetes-mp3converter.com/upload
  ```

  ```console
   curl -X POST -F 'file=@./video.mp4' -H 'Authorization: Bearer <JWT Token>' http://kubernetes-mp3converter.com/upload
  ``` 
  
  Check if you received the ID on your email.

- **Download Endpoint**
  ```http request
  GET http://kubernetes-mp3converter.com/download?fid=<Generated file identifier>
  ```
  ```console
   curl --output video.mp3 -X GET -H 'Authorization: Bearer <JWT Token>' "http://kubernetes-mp3converter.com/download?fid=<Generated fid>"
  ``` 

## Destroying the Infrastructure

- **Auth Service:**
  ```
  $ cd auth/manifests
  $ kubectl delete -f .
  ```

- **Gateway Service:**
  ```
  $ cd gateway/manifests
  $ kubectl delete -f .
  ```

- **Converter Service:**
  ```
  $ cd converter/manifests
  $ kubectl delete -f .
  ```

- **Notification Service:**
  ```
  $ cd notification/manifests
  $ kubectl delete -f .
  ```

- **rabbitmq Service:**
  ```
  $ cd rabbit/manifests
  $ kubectl delete -f .
  ```

- **minikube:**
  ```
  $ minikube delete --all
  ```
