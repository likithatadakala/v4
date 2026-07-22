---
date: '2'
title: 'YOLO Inference Docker'
cover: './yolo-inference-docker/yolo-inference-docker.png'
github: 'https://github.com/likithatadakala/yolo-inference-docker'
external: 'https://hub.docker.com/r/tadakalalikitha/yolo-inference'
cta: ''
tech:
  - Python
  - FastAPI
  - Docker
  - Kubernetes
  - GitHub Actions
  - YOLOv8
  - pytest
---

Production shaped ML inference service that serves a YOLOv8 object detection model behind a FastAPI endpoint, packaged in a multi stage Docker container with a non root user and baked in model weights. Deployed to a local Kubernetes cluster with liveness and readiness probes plus a Horizontal Pod Autoscaler that scaled the service from 2 to 5 pods under load.

A GitHub Actions CI/CD pipeline runs pytest smoke tests on every pull request and automatically builds and publishes the Docker image on every merge to main, tagging each build with both :latest and :commit-sha for full traceability. Closes a real production engineering gap, moving from a model that works in a notebook to a model that is deployed, tested, and reproducibly built on every commit.
