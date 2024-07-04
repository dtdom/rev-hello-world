# rev-hello-world

This repository contains a Flask application designed to be deployed both locally and in a Kubernetes cluster. The infrastructure components such as Kubernetes clusters, VPC, networking, and security groups are assumed to be managed separately, potentially using Terraform or other IaC tools, and are not included in this repository. The Flux and Helm files are just a starting point and should be customized to fit the specific requirements of the target environment.

## Index
1. [Local setup](#local-setup)
    1. [Raw setup](#raw-setup)
    2. [Docker setup](#docker-setup)
2. [Cloud setup](#cloud-setup)
    1. [Behaviour](#behaviour)
    2. [Cloud architecture diagram](#cloud-architecture-diagram)
3. [Next steps](#next-steps)

## Local setup

### Raw setup

Clone repo:
```
git clone https://github.com/dtdom/rev-hello-world.git
cd rev-hello-world

```

Create a virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```
Install the dependencies:
```
pip install -r requirements.txt
```

Run the app:
```
flask run
```

### Docker setup

Build the image:
```
docker build -t rev-hello-world .
``` 

Run the image:
```
docker run -p 5000:5000 rev-hello-world
``` 

## Cloud setup

This solution has been designed to be deployed in a K8s cluster hosted in AWS. 
This cluster should have at least the following components:

- Load balancer controller
- Helm controller
- Prometheus operator
- A collector like Alloy already in place

For the remote deployment, it also expects a database to be available.

### Behaviour
1. When you push code to the main branch of the Git repository, the following automated process begins:
2. The GitHub Actions Pipeline get executed:
    1. Checkout and python setup
    2. Lint Code
    3. Run Tests: The code is tested using unittest.
    4. Build the imnage with buildx or kaniko, etc
    5. Push image to ECR.
3. FluxCD:
    1. When a change is detected (e.g., a new Docker image), FluxCD updates the Kubernetes cluster with the new manifests.
    2. The updated Docker image is deployed to the Kubernetes cluster.


### Cloud arch diagram

![Diagram](diagram.png)

We are not including in the Diagram the following information:

- Security groups and some other network configurations.
- DNS/route53 configurations.
- WAF, Firewall, etc.
- K8s controllers, operator, etc.

## Next steps

1. Install Vault operator to manage the secrets in the cluster.
2. We may discuss if one environment is enough or if we need to have a staging environment, etc.
3. The pipeline should be improved to include more tests and checks. Using SCA and SAST tools would be a good idea.