This is a demo repo showing how one can use containerized models with W&B Launch on Kubernetes.

# Overview
This repo contains code to create 2 images:
1. A containerized model using tenforflow model server to host a containerized model.
2. An image that will send requests to the containerized model.

The queue config provided will allow the 2 images to communicate in a kubernetes cluster.


# To get started:
1. Create a queue with the queue config provided in `queue_config.yaml`.
2. Create kubernetes cluster and start an agent running in it watching the queue from step 1.
3. Run model.py to create an instance of the model to be containerized.
4. Run `docker buildx build --platform linux/amd64 -t <model-image-name> . --push` to create an image of the containerized model. Ensure the repo containing this image
   is accessible by the kubernetes cluster.
5. Run `docker buildx build --platform linux/amd64 -f ./Dockerfile.inf . -t <inference-job-image-name> --push` to create an image for the inference job. Ensure the repo 
   containing this image is accesible by the kubernetes cluster.
6. Run `wandb job create image <inference-job-image-name>  -p <project> -e <entity> --name inference-sender`
7. Go to the UI and submit the created job to the queue.




