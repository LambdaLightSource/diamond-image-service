# Diamond Image Service

Processes images enabling the retrieval and storing of images in a NAS S3 Bucket and enables various manipulations to the images. 

# Getting Started

## Cloning the Repository

To begin, please clone the repository to your local machine. This will provide you with all the necessary files to run and deploy the server:

```bash
git clone https://github.com/LambdaLightSource/diamond-image-service
```

## Running Locally

Navigate to the thumbor_ directory and execute server.py to start the server locally:

```bash
python server.py
```
You can access the local server at: http://localhost:8888/unsafe/<image_name>

This will allow you to test image processing directly in your browser.

# Kubernetes Deployment

## Setting Up the Namespace

Our service is hosted within the image-service namespace on Kubernetes. Typically, you’ll be in your personal test namespace identified by your fedid. Switch to the image-service namespace using:

```bash
kubectl config set-context --current --namespace=image-service
```

# Deployment Process

Ensure that all necessary YAML files are correctly applied. Start by deploying the sealed secret containing the NAS S3 credentials:

```bash
kubectl apply -f k8s/sealedthumbor-secret.yaml
```

If issues arise with the sealed secret, create and seal a new one by following the guidelines available in the [Secrets Guide](https://dev-portal.diamond.ac.uk/guide/kubernetes/tutorials/secrets/)

Next, set up the persistent volume to store the image cache:

```bash
kubectl apply -f k8s/pv-pvc.yaml
```

Then, deploy the service and deployment configurations:

```bash
kubectl apply -f k8s/service.yaml

kubectl apply -f k8s/deployment.yaml
```

This deployment uses images from the Google Cloud Registry. Ensure you have the necessary permissions and settings configured as specified in the [Container Registry guide](https://confluence.diamond.ac.uk/display/CLOUD/Container+Registry).

Finally, apply the ingress to make the service accessible externally:

```bash
kubectl apply -f k8s/ingress.yaml
```

# Managing Cache and Storage

To use the cache, first find your pod:

```bash
kubectl get pods
```

Then, access the pod's shell:

```bash
kubectl exec -it <pod_name> -- /bin/bash
```

Find the cache directory:

```bash
find /data/thumbor/storage
```

To manage cache purging, clone the CronCachePurger repository and apply the relevant YAML:

```bash
git clone https://github.com/LambdaLightSource/CronCachePurger

kubectl apply -f cronjob.yaml
```

There are two cron jobs: one purges the cache and the other manages storage deletion from the NAS S3 Bucket. These can be triggered through the Kubernetes dashboard, and the schedule configured through the YAML.

# Testing Locally with Dev Containers.

Please ensure the latest version of the dev containers app is installed. Click the blue icon in the bottom left corner of your editor to open the menu and select "Rebuild in Container" to set up your development environment.

# Technical Architecture

![Thumbor Architecture](https://github.com/LambdaLightSource/diamond-image-service/blob/thumbor/assets/ThumborArchitecture.png)
