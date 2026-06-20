# Local Setup Guide - MacBook Docker & Minikube

**Status**: Ready to start

## Step 1: Start Docker Desktop (Prerequisite)

### Option A: Using Docker Desktop GUI
```bash
# Open Applications folder
open /Applications/Docker.app

# Wait for Docker icon to appear in menu bar (top-right)
# It will show "Docker is running" after 1-2 minutes
```

### Option B: Start Docker Daemon from Terminal
```bash
# This command starts Docker in the background
open -a Docker

# Wait for it to fully start (2-3 minutes)
# You'll see the Docker icon in the menu bar when ready
```

### Verify Docker is Running
```bash
docker ps
# Should show: "CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES"
# If it works, Docker is ready!
```

---

## Step 2: Start Minikube (After Docker is Ready)

### Start Minikube Cluster
```bash
# Start with Docker driver (requires Docker to be running)
minikube start --driver=docker

# This will:
# - Create a virtual cluster
# - Pull necessary images
# - Configure kubectl
# - Takes 2-5 minutes on first run
```

### Verify Minikube Status
```bash
minikube status

# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
```

### Get Minikube Info
```bash
# Get cluster IP
minikube ip

# Check dashboard (optional GUI)
minikube dashboard

# View all addons
minikube addons list
```

---

## Step 3: Build Flask Application Docker Image

### Build the Image Locally
```bash
cd /Users/mac/projects/flask-devops-demo

# Build Docker image
docker build -t flask-devops-demo:latest .

# Verify image was created
docker images | grep flask-devops-demo
```

### Test the Image Locally (Optional)
```bash
# Run container locally
docker run -d -p 5000:5000 --name flask-app flask-devops-demo:latest

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/metrics

# View logs
docker logs -f flask-app

# Stop container
docker stop flask-app
docker rm flask-app
```

---

## Step 4: Load Image into Minikube

### Option A: Build Directly in Minikube (Recommended)
```bash
# Point Docker to Minikube's Docker daemon
eval $(minikube docker-env)

# Now build - image goes directly to Minikube
docker build -t flask-devops-demo:latest .

# Verify image is in Minikube
docker images | grep flask-devops-demo

# Return to local Docker (if needed)
eval $(docker-machine env --unset)
```

### Option B: Load Pre-built Image
```bash
# Build locally first
docker build -t flask-devops-demo:latest .

# Save image
docker save flask-devops-demo:latest | gzip > flask-devops-demo.tar.gz

# Load into Minikube
minikube image load flask-devops-demo.tar.gz
```

---

## Step 5: Deploy to Minikube Kubernetes

### Apply Kubernetes Manifests
```bash
cd /Users/mac/projects/flask-devops-demo

# Deploy to Minikube
kubectl apply -f k8s/

# Verify deployment
kubectl get pods
kubectl get svc
```

### Check Deployment Status
```bash
# Watch pods starting
kubectl get pods --watch

# Describe deployment
kubectl describe deployment flask-devops-demo

# View logs
kubectl logs -f deployment/flask-devops-demo
```

### Access the Application
```bash
# Method 1: Port Forward (Easy)
kubectl port-forward svc/flask-devops-demo 5000:80

# In another terminal:
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/metrics

# Method 2: Get Service URL
minikube service flask-devops-demo --url

# Method 3: Service IP
kubectl get svc flask-devops-demo
# Use the CLUSTER-IP or EXTERNAL-IP
```

---

## Step 6: Setup Monitoring Stack (Optional)

### Deploy Prometheus
```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Create Prometheus config
kubectl apply -f prometheus-config.yaml -n monitoring

# Access Prometheus
kubectl port-forward -n monitoring svc/prometheus-server 9090:80

# URL: http://localhost:9090
```

### Deploy Grafana
```bash
# Create Grafana config
kubectl apply -f grafana-dashboard.yaml -n monitoring

# Access Grafana
kubectl port-forward -n monitoring svc/grafana 3000:80

# URL: http://localhost:3000
# Credentials: admin/admin
```

---

## Complete Startup Sequence

### **First Time Setup** (~10-15 minutes)
```bash
# 1. Start Docker Desktop
open -a Docker
# Wait 2-3 minutes...

# 2. Start Minikube
minikube start --driver=docker
# Wait 3-5 minutes...

# 3. Verify everything
docker ps
minikube status
kubectl cluster-info

# 4. Build image in Minikube
eval $(minikube docker-env)
cd /Users/mac/projects/flask-devops-demo
docker build -t flask-devops-demo:latest .

# 5. Deploy to Kubernetes
kubectl apply -f k8s/

# 6. Access application
kubectl port-forward svc/flask-devops-demo 5000:80
# URL: http://localhost:5000
```

### **Subsequent Startups** (~5 minutes)
```bash
# 1. Start Docker Desktop
open -a Docker
# Wait 2 minutes...

# 2. Start Minikube
minikube start

# 3. Point to Minikube Docker
eval $(minikube docker-env)

# 4. Rebuild if code changed
docker build -t flask-devops-demo:latest .

# 5. Redeploy if needed
kubectl apply -f k8s/

# 6. Port forward
kubectl port-forward svc/flask-devops-demo 5000:80
```

---

## Useful Commands Reference

### Docker Commands
```bash
# List running containers
docker ps

# List all images
docker images

# Build image
docker build -t name:tag .

# Run container
docker run -d -p port:port --name name image:tag

# View logs
docker logs container-name

# Stop container
docker stop container-name

# Remove container
docker rm container-name
```

### Minikube Commands
```bash
# Start cluster
minikube start --driver=docker

# Stop cluster
minikube stop

# Delete cluster
minikube delete

# Get cluster IP
minikube ip

# Access dashboard
minikube dashboard

# SSH into cluster
minikube ssh

# View logs
minikube logs
```

### Kubernetes (kubectl) Commands
```bash
# Get pods
kubectl get pods

# Get services
kubectl get svc

# Get deployments
kubectl get deployment

# Describe resource
kubectl describe pod pod-name

# View logs
kubectl logs pod-name

# Port forward
kubectl port-forward svc/service-name local:remote

# Deploy manifests
kubectl apply -f file.yaml

# Delete deployment
kubectl delete deployment name

# Watch resources
kubectl get pods --watch
```

---

## Troubleshooting

### Docker Daemon Not Starting
```bash
# Kill any stuck Docker processes
killall Docker

# Start fresh
open -a Docker

# Wait 2-3 minutes and verify
docker ps
```

### Minikube Issues
```bash
# Check status in detail
minikube status

# View logs
minikube logs | tail -50

# Reset cluster
minikube delete
minikube start --driver=docker

# Check disk space
minikube ssh "df -h"
```

### Pod Not Starting
```bash
# Check pod status
kubectl describe pod flask-devops-demo-XXXX

# View logs
kubectl logs flask-devops-demo-XXXX

# Check events
kubectl get events

# Common fix - restart deployment
kubectl rollout restart deployment/flask-devops-demo
```

### Cannot Connect to Service
```bash
# Verify service exists
kubectl get svc

# Check endpoints
kubectl get endpoints

# Test pod directly
kubectl exec -it pod-name -- curl localhost:5000/health

# Port forward and test
kubectl port-forward svc/flask-devops-demo 5000:80
# New terminal: curl http://localhost:5000/
```

### Image Pull Issues in Minikube
```bash
# Point to Minikube Docker
eval $(minikube docker-env)

# Rebuild image
docker build -t flask-devops-demo:latest .

# Verify image exists in Minikube
docker images

# Update deployment imagePullPolicy
kubectl set image deployment/flask-devops-demo \
  flask-devops-demo=flask-devops-demo:latest \
  --record
```

---

## Resource Monitoring

### Monitor Cluster Resources
```bash
# Show resource usage
kubectl top nodes
kubectl top pods

# Show resource requests/limits
kubectl describe nodes

# Check available resources
kubectl describe node minikube
```

### Scale Application
```bash
# Manually scale
kubectl scale deployment flask-devops-demo --replicas=3

# Check replica status
kubectl get deployment flask-devops-demo
```

### View Application Metrics
```bash
# Get pod metrics
kubectl get pods -o wide

# Watch logs
kubectl logs -f deployment/flask-devops-demo

# Stream metrics
kubectl top pods --watch
```

---

## Cleanup & Shutdown

### Stop Everything (Preserve Data)
```bash
# Stop Minikube (keeps images/data)
minikube stop

# Stop Docker
pkill -f "docker"
```

### Full Cleanup (Start Fresh)
```bash
# Delete Minikube cluster
minikube delete

# Remove local images (optional)
docker rmi flask-devops-demo:latest

# Restart
minikube start --driver=docker
```

---

## Performance Tips for MacBook

1. **Allocate Resources to Minikube**
   ```bash
   minikube start --driver=docker --cpus=4 --memory=4096
   ```

2. **Check Docker Desktop Resources**
   - Docker → Preferences → Resources
   - CPUs: 4-6
   - Memory: 4-6 GB

3. **Monitor System Resources**
   ```bash
   # Real-time monitoring
   top
   
   # Disk usage
   df -h
   
   # Memory usage
   vm_stat
   ```

4. **Clean Up Space**
   ```bash
   # Remove unused Docker images/volumes
   docker system prune -a
   
   # Remove Minikube cache
   rm -rf ~/.minikube
   ```

---

## Next Steps

Once everything is running:

1. ✅ Access Flask app: `http://localhost:5000`
2. ✅ Check metrics: `http://localhost:5000/metrics`
3. ✅ Run tests: `pytest --cov=.`
4. ✅ Deploy to Jenkins (when ready)
5. ✅ Setup monitoring stack

---

**Last Updated**: 2026-06-20
**Platform**: macOS
**Tools**: Docker Desktop, Minikube, kubectl
