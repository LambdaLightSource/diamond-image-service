# Diamond Image Service

## Introduction

The Diamond Image Service processes and manage images dynamically within a Kubernetes environment. This service uses Thumbor, an open-source photo processing and thumbnail tool, to provide features for image visualization, resizing, reformatting, and storage management via a NAS-S3 bucket.  
  
For instructions on how to use the service please refer to the [User Guide](/docs/user_guide.md).  
For deployment setup please refer to the [Deployment Guide](/docs/deployment_guide.md).  
For getting setup for local testing, refer to the [Developer Guide](/docs/developer_setup.md).  

# Technical Architecture

![Thumbor Architecture](thumbor/assets/ThumborArchitecture.png)

## Clients
Clients can be any device or system that makes HTTP requests to the service. They interact with the Thumbor instance through web requests to process and retrieve images as specified by the URL parameters they include.

## Ingress  
The Ingress acts as the entry point for all requests from clients to the services running within the Kubernetes cluster. It manages external access to the services, routing traffic to the appropriate internal components.

## Thumbor Instance 
This is the core component where the image processing tasks are executed. It runs as a containerized application within Kubernetes and is scaleable.

## Persistent Volume 
The Persistent Volume (PV) is used for managing storage resources that need to persist beyond the lifecycle of individual pods. It is used for caching images and persists through restarts and deployments. No matter how many instances of Thumbor are running they will all share the same volume. The cache purger deletes from the same volume.

## Cache Purger
This component is responsible for clearing the cache in the Persistent Volume. It ensures that cached images modified more than 7 days ago and accessed more than 1 day ago are removed from the cache. This is run on a schedule that is executed on the hour, every hour.

## Expired Image Deleter
The Expired Image Deleter removes images from the NAS-S3 bucket that have reached their expiration date, as defined by the lifespan parameter during upload. 

## NAS-S3 Bucket
This component is the external storage system where images are ultimately stored and retrieved from.
