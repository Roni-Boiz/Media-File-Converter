# Microservice Project: Video-Audio Converter
Converting mp4 videos to mp3 in a microservices architecture.

image

## Deploying a Python-based Microservice Application on Local Minikube Kubernetes Cluster

### Introduction

This document provides a step-by-step guide for deploying a Python-based microservice application on Kubernetes (minikube). The application comprises five major microservices: `gateway`, `auth`, `converter`, `rabbitmq`, and `notification`.

### Prerequisites

Before you begin, ensure that the following prerequisites are met:

1. **Python:** Ensure that Python is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Install kubectl:** Install the latest stable version of `kubectl` on your system. You can find installation instructions [here](https://kubernetes.io/docs/tasks/tools/).

3. **Databases:** Install MySQL and MongoDB for your application.

4. **k9s:** Install k9s to graphically view and manage running services (optional)

### High Level Flow of Application Deployment

Follow these steps to deploy your microservice application:

1. **MongoDB and MySQL Setup:** Create databases requried users and tables.

   navigae to auth (python/src/auth) directory execute,

   ```bash
   $ sudo mysql -u root -p < init.sql
   ```

> [!NOTE]
> Before that command make sure you have update the email with an actual email rather than dummy or fake email because you will receive an email with the *file_id* to download the converted mp3 file. 

3. **RabbitMQ Deployment:** Deploy RabbitMQ for message queuing, which is required for the `converter`.

    ```
    $ cd python/src/rabbit/manifests
    $ kubectl apply -f .
    ```

4. **Create Queues in RabbitMQ:** Before deploying the `converter`, create two queues in RabbitMQ: `mp3` and `video`. (will create them automatically, manually create them if you have delete them by change)

> [!TIP]
> Rabbitmq dashboard can be access through `kubernetes-rabbitmq-manager.com` and default username and password is `guest`

5. **Deploy Microservices:**
    - **converter:** Deploy the `converter`.
    - **notification:** Configure email for notifications. Make sure to provide your email and app-password in `notification/manifests/notification-secret.yaml` then deploy the `notification`
    - **auth:** Deploy the `auth`.
    - **gateway:** Deploy the `gateway`.

    ```
    $ cd python/src/<folder>/manifests
    $ kubectl apply -f .
    ```
  
> [!NOTE]
> Please start service in order `rabbit --> converter --> notification --> auth --> gateway` and wait till previous service in ready to start the next service.

6. **Application Validation:** Verify the status of all components by running:
    ```bash
    $ kubectl get all
    ```

7. **Destroying the Infrastructure** 
    ```bash
    $ cd python/src/<folder>/manifests
    $ kubectl delete -f .
    ```


### Low Level Steps

#### DNS Name Resolution

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

#### MySQL HOST Resolution

- **Set MySQL Hosts:**

  Allow remote access from all host to MySQL

  ```
  $ sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf

  Update following two lines in mysqld.cnf file
  bind-address		= 0.0.0.0
  mysqlx-bind-address	= 0.0.0.0
  ```

#### Cluster Creation

Apply the manifest files for each microservice:

- **rabbitmq Service:**
  ```
  $ cd rabbit/manifests
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

#### Application Validation

After deploying the microservices, verify the status of all components by running:

```
$ kubectl get all
```

### Notification Configuration

In order to get app password for configured email for notifications you need to enable two-factor authentication (2FA), and to create a app password follow these steps:

1. Go to your Gmail account and click on your profile.

2. Click on "Manage Your Google Account."

3. Navigate to the "Security" tab on the left side panel.

4. Enable "2-Step Verification."

5. Search for the application-specific passwords / `app password`. You will find it in the settings.

6. Click on "Other" and provide your name.

7. Click on "Generate" and copy the generated password.

8. Paste this generated password in `notification/manifests/notification-secret.yaml` along with your email.

    ```jsx
    stringData:
      GMAIL_ADDRESS: <your-gmail-address>
      GMAIL_PASSWORD: <your-app-password>
    ```

### Local Environment Configuration

In order for you to do local development you need to enable conda or python environment for each microservice.

**create envirnment**
```
$ conda create --name venv python=3.8
- or -
$ conda create -p ./venv python=3.8
- or -
$ python -m venv venv
```

**activate environment**
```
$ source ./venv/bin/activate
- or -
$ conda activate ./venv
```

**export environment varaibles**

```
$ export MYSQL_HOST=localhost
$ printenv
```

**update requirements.txt**

```
$ pip freeze > requirements.txt
```

When testing scale services to 1

```
$ kubectl scale deployment --replicas=1 auth gateway converter notification
```

## API Definition

Run the application through the following API calls:

- **Login Endpoint**
  ```http request
  POST http://kubernetes-mp3converter.com/login
  ```
  image

  ```console
  $ curl -X POST http://kubernetes-mp3converter.com/login -u <mysql_user_email>:<mysql_user_password>
  ``` 

  image

  Expected output: JWT Token!

- **Upload Endpoint**

  ```http request
  POST http://kubernetes-mp3converter.com/upload
  ```

  image

  ```bash
  $ curl -X POST -F 'file=@./video.mp4' -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/upload"
  ```

  image
  
  Expected output: An email with `file_id` to download the coverted file.

- **Download Endpoint**

  ```http request
  GET http://kubernetes-mp3converter.com/download?fid=<Generated file identifier>
  ```

  image

  ```bash
  $ curl --output convert.mp3 -X GET -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/download?fid=<Generated fid>"
  ``` 

### Test Cases

1. Test Case 1

    - Input: Video (src="./TEDx1.mp4")

    - Output: Audio (mp3)

      <audio controls>
        <source src="./convert1.mp3" type="audio/mp3">
        Your browser does not support the audio tag.
      </audio>

2. Test Case 2

    - Input: Video (src="./TEDx2.mp4")

    - Output: Audio (mp3)

      <audio controls>
        <source src="./convert2.mp3" type="audio/mp3">
        Your browser does not support the audio tag.
      </audio>

3. Test Case 3

    - Input: Video (src="./TEDx3.mp4")

    - Output: Audio (mp3)

      <audio controls>
        <source src="./convert3.mp3" type="audio/mp3">
        Your browser does not support the audio tag.
      </audio>

## Destroying the Infrastructure

- **Gateway Service:**
  ```
  $ cd gateway/manifests
  $ kubectl delete -f .
  ```

- **Auth Service:**
  ```
  $ cd auth/manifests
  $ kubectl delete -f .
  ```

- **Notification Service:**
  ```
  $ cd notification/manifests
  $ kubectl delete -f .
  ```

- **Converter Service:**
  ```
  $ cd converter/manifests
  $ kubectl delete -f .
  ```

- **rabbitmq Service:**
  ```
  $ cd rabbit/manifests
  $ kubectl delete -f .
  ```

- **minikube:**
  ```
  minikube delete --all
  ```


## Deploying a Python-based Microservice Application on EC2 Instance Kubernetes Cluster

**Launch an EC2 Instance**

image

Enable folowing inbound ports

image

**Setup Self-Hosted Runner**

```bash
# Create a folder
$ mkdir actions-runner && cd actions-runner

# Download the latest runner package
$ curl -o actions-runner-linux-x64-2.319.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz

# Optional: Validate the hash
$ echo "3f6efb7488a183e291fc2c62876e14c9ee732864173734facc85a1bfb1744464  actions-runner-linux-x64-2.319.1.tar.gz" | shasum -a 256 -c

# Extract the installer
$ tar xzf ./actions-runner-linux-x64-2.319.1.tar.gz
  ```

```bash
# Create the runner and start the configuration experience
$ ./config.sh --url https://github.com/Roni-Boiz/Media-File-Converter --token <your-token>

# Last step, run it!
$ ./run.sh
```

**Run Script Workflow**

image

**Setup SonarQube Scanner**

```bash
$ docker run -d --name sonar -p 9000:9000 sonarqube:lts-community
```

image

**Run CICD Wordflow**

image

> [!NOTE]
> Please update the image names with the onces created during the workflow.

FIles need to be updated:
- auth-deploy.yaml --> (image: don361/kubernetes-media-auth:1.0)
- converter-deploy.yaml --> (image: don361/kubernetes-media-converter:1.0)
- gateway-deploy.yaml --> (image: don361/kubernetes-media-gateway:1.0)
- notification-deploy.yaml --> (image: don361/kubernetes-media-notification:1.0)

**Test Application**

Run the application through the following API calls:

- **Login Endpoint**

  ```console
  $ curl -X POST http://kubernetes-mp3converter.com/login -u <mysql_user_email>:<mysql_user_password>
  ``` 

  image

  Expected output: JWT Token!

- **Upload Endpoint**

  ```bash
  $ curl -X POST -F 'file=@./video.mp4' -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/upload"
  ```

  image
  
  Expected output: An email with `file_id` to download the coverted file.

- **Download Endpoint**

  ```bash
  $ curl --output convert.mp3 -X GET -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/download?fid=<Generated fid>"
  ``` 

  image

**Run Destroy Workflow**

image

**Remove Self-Hosted Runner**

```
// Remove the runner
$ ./config.sh remove --token <your-token>
```

**Terminate the Instance**

image