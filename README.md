# Microservice Project: Video-Audio Converter
Converting mp4 videos to mp3 in a microservice architecture.

![micro-service-media-converter](https://github.com/user-attachments/assets/0bb4e83f-1d2e-4acb-b55b-bacf21fe1e9b)

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
> Before that command make sure you have update the email with an actual email rather than dummy or fake email because later you will receive an email with the *file_id* to download the converted mp3 file. 

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
> Please start service in order `rabbit --> converter --> notification --> auth --> gateway` and wait till previous service in ready to start the next one.

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
    
    ![minikube-1](https://github.com/user-attachments/assets/dcb534e8-369f-4cac-b024-dc1ce9469c3f)

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

  $ sudo systemctl restart mysql
  ```

  **Set MongoDB Hosts:**

  Allow remote access form all host to MySQL

  ```bash
  $ sudo vim /etc/mongod.conf

  Update following line in mongod.conf file
  bindIp: 0.0.0.0

  sudo systemctl restart mongod
  ```

#### Cluster Creation

Apply the manifest files for each microservice:

- **rabbitmq Service:**
  ```
  $ cd rabbit/manifests
  $ kubectl apply -f .
  ```
  
  ![rabbitmq-1](https://github.com/user-attachments/assets/b16c5bf5-8690-4497-b021-ff4217cacb4d)

  - **Converter Service:**
  ```
  $ cd converter/manifests
  $ kubectl apply -f .
  ```
  
  ![converter-1](https://github.com/user-attachments/assets/1e4928d1-51a3-4d16-93d7-31f9ad25bfc3)

- **Notification Service:**
  ```
  $ cd notification/manifests
  $ kubectl apply -f .
  ```
  
  ![notification-1](https://github.com/user-attachments/assets/359c7533-e034-452d-a3bf-e813a9ae359a)


- **Auth Service:**
  ```
  $ cd auth/manifests
  $ kubectl apply -f .
  ```
  
  ![auth-1](https://github.com/user-attachments/assets/59ca2163-c50a-429d-90ce-1a7f504b6baf)

- **Gateway Service:**
  ```
  $ cd gateway/manifests
  $ kubectl apply -f .
  ```
  
  ![gateway-1](https://github.com/user-attachments/assets/792a30c6-2a52-498d-9a87-bf2cc9c98f9d)

#### Application Validation

After deploying the microservices, verify the status of all components by running:

```
$ kubectl get all
```

![k9s](https://github.com/user-attachments/assets/2fdec9a6-3bf6-4508-8f71-43f209fc178e)

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

![curl-login-upload-download](https://github.com/user-attachments/assets/06dd5afe-4620-45c2-bcd5-5d12d37d2026)

- **Login Endpoint**

  ```console
  $ curl -X POST http://kubernetes-mp3converter.com/login -u <mysql_user_email>:<mysql_user_password>
  ```
  
  ```http request
  POST http://kubernetes-mp3converter.com/login
  ```
  
  ![postman-login](https://github.com/user-attachments/assets/2f859722-aca9-456a-b540-0898919334be)

  Expected output: JWT Token!

- **Upload Endpoint**

  ```bash
  $ curl -X POST -F 'file=@./video.mp4' -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/upload"
  ```

  ```http request
  POST http://kubernetes-mp3converter.com/upload
  ```

  ![postman-upload-1](https://github.com/user-attachments/assets/c9ff35f5-e6c8-4028-af67-74087ea3bb24)

  ![postman-upload-2](https://github.com/user-attachments/assets/495d2b4b-e952-45d7-ba93-9e147d75f05d)

  ![rabbitmq-queue](https://github.com/user-attachments/assets/f04306c0-ca7c-48af-8ae2-e6b2497b235b)

  ![email-notification](https://github.com/user-attachments/assets/d759a59c-c139-4e76-a713-b7f16067c548)
  
  Expected output: Success. An email with `file_id` to download the coverted file.

  ![mongo-1](https://github.com/user-attachments/assets/443d54cf-24fe-4eb2-9edd-41c177766ae9)

  ![mongo-2](https://github.com/user-attachments/assets/bf719c8a-8142-4584-95bf-617b35501d34)

- **Download Endpoint**

  ```bash
  $ curl --output convert.mp3 -X GET -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/download?fid=<Generated fid>"
  ```
  
  ```http request
  GET http://kubernetes-mp3converter.com/download?fid=<Generated file identifier>
  ```

  ![postman-download-1](https://github.com/user-attachments/assets/7f75016a-589e-475b-838f-65a741b480ba)
  
  ![postman-download-2](https://github.com/user-attachments/assets/a2e71927-3885-41eb-ab64-85fa0b0b5d34)

  Expected output: Mp3 file should be save to current directory.

  ```bash
  mongofiles --db=mp3s get_id --local=convert-mongo.mp3 '{"$oid": "fid"}'
  ```

  ![mongo-3](https://github.com/user-attachments/assets/04d18f0e-b047-427d-8d37-940b0e576611)
  

### Test Cases

1. Test Case 1

    - Input: Video (src="./TEDx1.mp4")

    - Output: Audio (mp3)

      https://github.com/user-attachments/assets/1a73c66a-5ce0-42e3-92ff-8e91e827aa03

      <audio controls>
        <source src="./convert1.mp3" type="audio/mp3">
        Your browser does not support the audio tag.
      </audio>

2. Test Case 2

    - Input: Video (src="./TEDx2.mp4")

    - Output: Audio (mp3)
  
      https://github.com/user-attachments/assets/04cdbcd4-b86a-4f34-be55-bfade6b2a4c0

      <audio controls>
        <source src="./convert2.mp3" type="audio/mp3">
        Your browser does not support the audio tag.
      </audio>

3. Test Case 3

    - Input: Video (src="./TEDx3.mp4")

    - Output: Audio (mp3)
  
      https://github.com/user-attachments/assets/5a0ee3fe-d3e4-4913-9b1a-601246450066

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
  
  ![gateway-2](https://github.com/user-attachments/assets/d84a80de-c86a-478e-aca5-14e75dc8c5dc)

- **Auth Service:**
  ```
  $ cd auth/manifests
  $ kubectl delete -f .
  ```
  
  ![auth-2](https://github.com/user-attachments/assets/910c2e50-f111-4312-9969-91f8cab29a64)

- **Notification Service:**
  ```
  $ cd notification/manifests
  $ kubectl delete -f .
  ```

  ![notification-2](https://github.com/user-attachments/assets/17682d6d-60ed-4cc4-a803-2bcb23160eef)

- **Converter Service:**
  ```
  $ cd converter/manifests
  $ kubectl delete -f .
  ```

  ![converter-2](https://github.com/user-attachments/assets/5cef65ba-d4ad-4b06-b4e6-111e2263a566)

- **rabbitmq Service:**
  ```
  $ cd rabbit/manifests
  $ kubectl delete -f .
  ```

  ![rabbitmq-2](https://github.com/user-attachments/assets/16bb736e-4819-47ee-9c01-45bb7c63ba22)

- **minikube:**
  ```
  minikube delete --all
  ```

  ![minikube-2](https://github.com/user-attachments/assets/dcfd5da8-0ad1-461a-8471-6293477150f1)


## Deploying a Python-based Microservice Application on EC2 Instance Kubernetes Cluster

**Launch an EC2 Instance**

![ec2-instance](https://github.com/user-attachments/assets/4f1912f1-64c5-4d2f-a714-dcd4ccf3eb8e)

Enable folowing inbound ports

![ec2-ports](https://github.com/user-attachments/assets/36f92090-a926-45b7-99a7-103dc9e03595)

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

![runner-1](https://github.com/user-attachments/assets/4648db78-5edb-48f2-a16f-cc4013895ca1)

![runner-2](https://github.com/user-attachments/assets/1f94267a-6223-4d6a-8e03-7948c79eb419)


**Run Script Workflow**

![script-pipeline](https://github.com/user-attachments/assets/8c947298-a16d-4e26-8598-09384aba01fc)

**Setup SonarQube Scanner**

![partial-script](https://github.com/user-attachments/assets/999039df-181c-4090-99f0-9fe5745927ec)

```bash
$ docker run -d --name sonar -p 9000:9000 sonarqube:lts-community
```

![sonar-1](https://github.com/user-attachments/assets/fb02fcae-3ec4-4b33-892f-4892af0d46a8)

![sonar-2](https://github.com/user-attachments/assets/f37270d3-c354-4913-83ce-22f910ca3983)

![sonar-3](https://github.com/user-attachments/assets/c8283da1-5c88-4520-ad61-2e6889a0b686)

![sonar-4](https://github.com/user-attachments/assets/08205114-059b-4006-9a0b-f0fcd2328183)

![sonar-5](https://github.com/user-attachments/assets/d1f2f225-7251-4dfb-a10b-fad377b6a5c2)

![sonar-6](https://github.com/user-attachments/assets/bb558530-ceac-4ed0-bb0c-593736093374)

![sonar-7](https://github.com/user-attachments/assets/73cd2541-f232-4d95-bd85-f32b1e87ed1b)

![sonar-8](https://github.com/user-attachments/assets/c64ec1da-b578-41b4-9a70-dd4fcac7cf4c)

![sonar-9](https://github.com/user-attachments/assets/a551a248-e005-4217-ad88-f65a16bf2cd5)

![sonar-10](https://github.com/user-attachments/assets/ca073e80-099c-444c-9a1e-3917de4c9920)

![sonar-11](https://github.com/user-attachments/assets/3a71eb5c-7012-4292-a8de-931607bb4ca2)

![sonar-output](https://github.com/user-attachments/assets/df881914-bd95-4928-80a4-2d03d76fd06d)

**Setup Docker**

![docker-1](https://github.com/user-attachments/assets/9979bcba-ac43-4d58-8678-9c09a872fca6)

![docker-2](https://github.com/user-attachments/assets/de8a9396-842a-461d-9651-b87f57322e0d)

![docker-3](https://github.com/user-attachments/assets/b9ebc4e7-959a-4ed0-b10d-ea9c9e5d5d8e)

**Run CICD Wordflow**

![cicd-pipeline](https://github.com/user-attachments/assets/36852e57-6a33-4df6-bc28-37b4a489ce62)

> [!NOTE]
> Before run this pipeline please update the image names with the onces created during the pipeline. The pipeline will execute infinitely at strat tunnel step (last step) otherview you need to start the tunnel manually.

FIles need to be updated:
- auth-deploy.yaml --> (image: don361/kubernetes-media-auth:1.0)
- converter-deploy.yaml --> (image: don361/kubernetes-media-converter:1.0)
- gateway-deploy.yaml --> (image: don361/kubernetes-media-gateway:1.0)
- notification-deploy.yaml --> (image: don361/kubernetes-media-notification:1.0)

Also make sure that you have set the `GMAIL_ADDRESS` and `GMAIL_PASSWORD` in `notification/manifests/notification-secret.yaml` as specifine in notification configuration. Moreover, with a working email in `auth/init.sql`

However you can update them run time as well:

![update-user-email](https://github.com/user-attachments/assets/95c908ad-bf0b-48a5-8976-94c4e47817d3)

![update-notification-secret](https://github.com/user-attachments/assets/48506ba1-a878-43b8-9b47-65ab97143377)

![notification-secret](https://github.com/user-attachments/assets/47c3f851-122c-491e-b9a7-d6eb64b7c5d7)

![verify-notification-secret-update](https://github.com/user-attachments/assets/90db480a-119b-45ec-bbbd-fcd307e5a13c)

**Test Application**

Run the application through the following API calls:

![ec2-login-upload-download](https://github.com/user-attachments/assets/02123d8f-f80a-4e61-91d5-ad89c93fdcc4)

- **Login Endpoint**

  ```bash
  $ curl -X POST http://kubernetes-mp3converter.com/login -u <mysql_user_email>:<mysql_user_password>
  ``` 

  Expected output: JWT Token!

- **Upload Endpoint**

  ```bash
  $ curl -X POST -F 'file=@./video.mp4' -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/upload"
  ```
  
  Expected output: An email with `file_id` to download the coverted file.

- **Download Endpoint**

  ```bash
  $ curl --output convert.mp3 -X GET -H 'Authorization: Bearer <token>' "http://kubernetes-mp3converter.com/download?fid=<Generated fid>"
  ``` 

  ```bash
  mongofiles --db=mp3s get_id --local=convert-mongo.mp3 '{"$oid": "fid"}'
  ```

> [!WARNING]
> If you get `internal server error` as an output please restart the gateway service.

**Run Destroy Workflow**

![destroy-pipeline](https://github.com/user-attachments/assets/12c20a5b-9e3d-482d-94bf-23b7a819d55a)

**Remove Self-Hosted Runner**

```
// Remove the runner
$ ./config.sh remove --token <your-token>
```

![runner-remove-1](https://github.com/user-attachments/assets/5fe41d01-c3d8-4c53-9be5-d6d4630f7e5e)

![runner-remove-2](https://github.com/user-attachments/assets/2ce0507a-f4c1-4e62-a940-8d3663d7a5ea)

**Terminate the Instance**

![terminate-instance](https://github.com/user-attachments/assets/db4c4438-b200-46a7-a1b6-b801c1e3ba41)
