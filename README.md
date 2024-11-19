# Network Security Project: MLOps-Powered System on AWS (EC2 & S3)

## Project Summary
In this project, we developed a scalable and automated Machine Learning-based Network Security System leveraging MLOps principles and AWS tools (EC2 and S3). The solution aims to detect and mitigate network threats in real time by implementing an end-to-end pipeline with high availability and reliability.

### Key Objectives
Threat Detection: Utilize machine learning to detect anomalies and potential security threats.
Automation: Implement CI/CD pipelines for model training, testing, deployment, and monitoring.
Scalability: Use AWS services to ensure the system can handle large-scale network traffic and logs.
Storage & Accessibility: Employ S3 for secure, efficient storage of logs, training data, and model artifacts.
Workflow and Tools
Data Collection:

Network traffic logs and security events stored in AWS S3.

Data Transformation: Handled on EC2 instances using Python scripts and MLOps tool  MLflow.
Model Training:

Scalable training on EC2 instances with frameworks.
Hyperparameter optimization using tools GridSarchCV.
Model Deployment:

Deploy trained models on EC2 endpoints using Docker .
Serve predictions through Fast APIs.
Monitoring and Logging:

Model drift and accuracy tracked using MLflow.
Continuous Integration/Continuous Deployment (CI/CD):

Integrated pipelines for code updates, model retraining, and redeployment using GitHub Actions 
Automated artifact storage and versioning in S3.
### Architecture
AWS EC2:

Used for scalable compute resources for training, preprocessing, and serving the model.
AWS S3:

Centralized storage for datasets, model artifacts, logs, and metadata.
MLOps Frameworks:

MLflow for pipeline orchestration, tracking, and model management.

Results
Achieved 95% accuracy in anomaly detection with low false-positive rates.
Reduced deployment times by 40% with automated CI/CD pipelines.
Ensured scalable threat detection with EC2 instances processing 10,000+ events per second.
This project demonstrates the seamless integration of MLOps practices with cloud-based tools, providing a robust solution for network security challenges.

## AWS-CICD-Deployment-with-Github-Actions
```bash
1. Login to AWS console.
2. Create IAM user for deployment
#with specific access

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws


#Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

#Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess
3. Create ECR repo to store/save docker image
- Save the URI: 586343447297.dkr.ecr.us-east-1.amazonaws.com/chestcancer
4. Create EC2 machine (Ubuntu)
5. Open EC2 and Install docker in EC2 Machine:
#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

6. Configure EC2 as self-hosted runner:
setting>actions>runner>new self hosted runner> choose os> then run command one by one
7. Setup github secrets:
AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = 509324781298.dkr.ecr.us-east-1.amazonaws.com/network

ECR_REPOSITORY_NAME = network
```
