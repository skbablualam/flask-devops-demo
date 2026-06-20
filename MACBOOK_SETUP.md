# MacBook Local Setup - Step-by-Step Guide

**Date**: 2026-06-20  
**Status**: ✅ Complete and Working

## ✅ What's Running Right Now

```
🐳 Docker Desktop: Running
☸️  Minikube Cluster: Running (Kubernetes v1.35.1)
📦 Flask Application: 3 replicas running
🔧 Gunicorn: 4 workers handling requests
```

## 📊 Working Endpoints

| Endpoint | URL | Purpose | Status |
|----------|-----|---------|--------|
| Home | `http://localhost:5000/` | Application home page | ✅ Working |
| Health | `http://localhost:5000/health` | Health check (for probes) | ✅ Working |
| Metrics | `http://localhost:5000/metrics` | Prometheus metrics | ✅ Working |

---

## 🚀 Step-by-Step: How We Got Here

### Step 1: Started Docker Desktop
```bash
open -a Docker
# Waited 2-3 minutes for daemon to initialize
# Verified: docker ps
```

### Step 2: Started Minikube Cluster
```bash
minikube start --driver=docker --cpus=4 --memory=4096
# Result: Kubernetes v1.35.1 cluster created
```

### Step 3: Built Flask Application Image
```bash
# Pointed to Minikube's Docker environment
eval $(minikube docker-env)

# Built image with all dependencies (Prometheus, testing tools, etc.)
docker build -t flask-devops-demo:latest .
```

### Step 4: Deployed to Kubernetes
```bash
# Applied deployment and service manifests
kubectl apply -f k8s/

# Deployment created 3 replicas
# Service exposed as NodePort
```

### Step 5: Verified All Endpoints
```bash
# Port-forwarded service
kubectl port-forward svc/flask-devops-demo 5000:5000

# Tested all endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/metrics
```

---

## 💻 Daily Startup Commands

### Quick Start (Your Go-To Commands)

**Terminal 1: Start Docker & Minikube**
```bash
# 1. Start Docker
open -a Docker
# Wait 2 minutes...

# 2. Start Minikube
minikube start

# 3. Point to Minikube Docker
eval $(minikube docker-env)

# 4. Verify everything
docker ps
minikube status
kubectl cluster-info
```

**Terminal 2: Access the App**
```bash
# Port forward the service
kubectl port-forward svc/flask-devops-demo 5000:5000

# App is now accessible at:
# http://localhost:5000
```

**Terminal 3 (Optional): View Logs**
```bash
# Watch app logs in real-time
kubectl logs -f deployment/flask-devops-demo
```

---

## 🔄 Common Tasks

### View All Pods
```bash
kubectl get pods
```

### Rebuild and Redeploy (After Code Changes)
```bash
# 1. Make sure you're using Minikube's Docker
eval $(minikube docker-env)

# 2. Rebuild image
cd /Users/mac/projects/flask-devops-demo
docker build -t flask-devops-demo:latest .

# 3. Restart deployment
kubectl rollout restart deployment/flask-devops-demo

# 4. Wait for pods to be ready
kubectl get pods --watch
```

### Scale Application
```bash
# Scale to 5 replicas
kubectl scale deployment flask-devops-demo --replicas=5

# Check status
kubectl get deployment flask-devops-demo
```

### View Application Logs
```bash
# Latest pod logs
kubectl logs deployment/flask-devops-demo --tail=50

# Watch logs in real-time
kubectl logs -f deployment/flask-devops-demo

# Specific pod logs
kubectl logs pod-name
```

### Access Pod Shell
```bash
# Get shell access to a pod
LATEST_POD=$(kubectl get pods -o name | head -1)
kubectl exec -it $LATEST_POD -- /bin/bash

# Test from inside pod
curl http://localhost:5000/metrics
```

### Delete and Redeploy Everything
```bash
# Delete deployment
kubectl delete deployment flask-devops-demo

# Redeploy
kubectl apply -f k8s/
```

---

## 🛑 Stopping Everything

### Stop (Keep Data)
```bash
# Stop Minikube cluster
minikube stop

# Stop Docker
pkill -f "docker"
# Or: Quit Docker Desktop from menu
```

### Clean Up (Start Fresh)
```bash
# Delete Minikube cluster
minikube delete

# Remove image
docker rmi flask-devops-demo:latest

# Restart fresh
minikube start --driver=docker
```

---

## 📋 Troubleshooting

### Docker Not Responding
```bash
# Kill stuck Docker processes
killall Docker

# Start fresh
open -a Docker
sleep 120  # Wait 2 minutes
docker ps
```

### Minikube Issues
```bash
# Check status in detail
minikube status

# View logs
minikube logs | tail -50

# SSH into cluster
minikube ssh

# Restart
minikube delete
minikube start --driver=docker
```

### App Not Responding
```bash
# Check pod status
kubectl get pods

# Describe pod for errors
kubectl describe pod pod-name

# View logs
kubectl logs pod-name

# Check events
kubectl get events
```

### Metrics Endpoint Returns 404
```bash
# This usually means old pods are still running
# Restart deployment:
kubectl rollout restart deployment/flask-devops-demo

# Verify new pods have metrics:
LATEST_POD=$(kubectl get pods -o name | head -1)
kubectl exec $LATEST_POD -- curl localhost:5000/metrics
```

---

## 🔌 Integration Points

### Port Forwarding
```bash
# Flask app port
kubectl port-forward svc/flask-devops-demo 5000:5000

# Prometheus (when deployed)
kubectl port-forward -n monitoring svc/prometheus-server 9090:80

# Grafana (when deployed)
kubectl port-forward -n monitoring svc/grafana 3000:80
```

### Monitoring Stack (Future)
```bash
# When you deploy Prometheus/Grafana:
# Prometheus will scrape: http://flask-app:5000/metrics
# Grafana will visualize the metrics
# Dashboard panels pre-configured in DEVOPS_SETUP.md
```

---

## 📈 Performance Tips

### Resource Allocation
```bash
# Check Docker resources
# Docker menu → Preferences → Resources

# Recommended for MacBook:
# - CPUs: 4-6
# - Memory: 4-6 GB
# - Swap: 1 GB
```

### Monitor Resources
```bash
# Monitor in real-time
top

# Check disk usage
df -h

# Check memory
vm_stat

# Kubernetes resource usage
kubectl top nodes
kubectl top pods
```

### Clean Up Space
```bash
# Remove unused Docker images
docker system prune -a

# Remove unused volumes
docker volume prune

# Remove Minikube cache
rm -rf ~/.minikube
```

---

## 🎯 Quick Reference Card

```bash
# ===== STARTUP =====
open -a Docker && sleep 120 && minikube start && eval $(minikube docker-env)

# ===== BUILD & DEPLOY =====
docker build -t flask-devops-demo:latest . && \
kubectl apply -f k8s/ && \
kubectl rollout restart deployment/flask-devops-demo

# ===== TEST & VERIFY =====
kubectl port-forward svc/flask-devops-demo 5000:5000 &
sleep 2
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/metrics

# ===== VIEW STATUS =====
kubectl get pods
kubectl get svc
kubectl get deployment

# ===== WATCH LOGS =====
kubectl logs -f deployment/flask-devops-demo

# ===== CLEANUP =====
kubectl delete deployment flask-devops-demo
minikube delete
```

---

## 🔐 Security Notes (Local Development)

✅ Running locally - no internet exposure  
✅ Using Minikube - isolated cluster  
✅ Network policies configured in deployment  
⚠️  Health checks enabled (liveness & readiness)  
⚠️  Non-root user (appuser) in container  

---

## 📚 Additional Resources

- [LOCAL_SETUP.md](LOCAL_SETUP.md) - Detailed local setup guide
- [QUICKSTART.md](QUICKSTART.md) - Jenkins pipeline setup
- [DEVOPS_SETUP.md](DEVOPS_SETUP.md) - Full DevOps architecture
- [CONFIG_SUMMARY.md](CONFIG_SUMMARY.md) - Complete reference

---

## ✅ Checklist: First Time Setup

- [x] Docker Desktop installed
- [x] Minikube installed
- [x] Docker started (`docker ps` working)
- [x] Minikube started (`minikube status` showing Running)
- [x] Flask image built (`docker images | grep flask`)
- [x] Deployment created (`kubectl get deployment`)
- [x] Pods running (`kubectl get pods` showing 3/3 Ready)
- [x] Service accessible (`curl http://localhost:5000`)
- [x] All endpoints working (/, /health, /metrics)
- [x] Metrics being exported (Prometheus format visible)

---

## 🎯 Next Steps

1. **Local Testing**
   - Run Flask tests: `pytest --cov=.`
   - Build Docker locally: `docker build -t test:latest .`
   - Test container: `docker run -p 5000:5000 test:latest`

2. **Jenkins Integration**
   - See: [QUICKSTART.md](QUICKSTART.md)
   - Setup Jenkins credentials
   - Create pipeline job
   - Run first build

3. **Monitoring Setup**
   - Deploy Prometheus
   - Deploy Grafana
   - Configure dashboards

4. **Production Ready**
   - Push to Docker Hub
   - Setup ArgoCD
   - Configure Ingress
   - Setup monitoring stack

---

**Last Updated**: 2026-06-20  
**Environment**: macOS, Docker Desktop, Minikube  
**Status**: ✅ All Systems Operational
