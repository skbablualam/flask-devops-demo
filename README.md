# Flask DevOps Demo 🚀

**A complete end-to-end DevOps project** with full CI/CD automation using Jenkins, Docker, Kubernetes (Minikube), SonarQube, ArgoCD, and Monitoring Stack.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]() 
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()
[![Kubernetes](https://img.shields.io/badge/kubernetes-deployed-green)]()
[![Python](https://img.shields.io/badge/python-3.11-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

## 📊 Current Status ✅

```
✅ Running Locally on MacBook
   - Docker Desktop: Running
   - Minikube Cluster: Running (Kubernetes v1.35.1)
   - Flask App: 3/3 pods ready
   - All Endpoints: Working
   
✅ Endpoints Available:
   - http://localhost:5000/              → Home page
   - http://localhost:5000/health        → Health check
   - http://localhost:5000/metrics       → Prometheus metrics
```

---

## 🎯 Project Overview

This project demonstrates a **complete DevOps workflow** with:

```
GitHub Repository
    ↓
Jenkins CI/CD Pipeline (11 stages)
    ↓
├─ Code Quality (SonarQube + Static Analysis)
├─ Security Scanning (Trivy, Bandit, Pylint)
├─ Docker Build & Push
├─ Helm Chart Validation
├─ ArgoCD GitOps Deployment
├─ Kubernetes Deployment
├─ Prometheus Monitoring Setup
└─ Grafana Dashboard Creation
    ↓
Minikube Kubernetes Cluster
    ↓
├─ 3 Pod Replicas (Flask App)
├─ Horizontal Pod Autoscaler (HPA)
├─ Network Policies
├─ Health Checks & Probes
└─ Prometheus Metrics Exposure
    ↓
Monitoring Stack
    ├─ Prometheus → Metrics Collection
    └─ Grafana → Visualization & Alerts
```

---

## 🚀 11-Stage CI/CD Pipeline

| Stage | Purpose | Tools | Status |
|-------|---------|-------|--------|
| **1. Checkout** | Clone repository from GitHub | Git | ✅ Ready |
| **2. Unit Tests** | Run pytest with coverage | pytest, coverage | ✅ Ready |
| **3. SonarQube** | Code quality & security analysis | SonarQube, flake8, pylint, bandit | ✅ Ready |
| **4. Build Docker** | Create container image | Docker | ✅ Ready |
| **5. Trivy Scan** | Container vulnerability scanning | Trivy | ✅ Ready |
| **6. Push Docker** | Push to Docker Hub | Docker Registry | ✅ Ready |
| **7. Helm Charts** | Kubernetes templating & validation | Helm | ✅ Ready |
| **8. ArgoCD** | GitOps deployment automation | ArgoCD | ✅ Ready |
| **9. K8s Deploy** | Deploy to Kubernetes cluster | kubectl | ✅ Ready |
| **10. Prometheus** | Setup metrics collection | Prometheus | ✅ Ready |
| **11. Grafana** | Create visualization dashboards | Grafana | ✅ Ready |

---

## 🌐 Available Endpoints

| Endpoint | Method | Response | Purpose |
|----------|--------|----------|---------|
| `/` | GET | `DevOps Demo App Running Successfully!` | Home page |
| `/health` | GET | `{"status":"UP"}` | Health check (for K8s probes) |
| `/metrics` | GET | Prometheus format | Metrics for Prometheus scraping |

### Example Requests

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/metrics
```

---

## 🚀 Quick Start (3 minutes)

```bash
# 1. Start Docker Desktop
open -a Docker && sleep 120

# 2. Start Minikube
minikube start --driver=docker
eval $(minikube docker-env)

# 3. Deploy Flask app
kubectl apply -f k8s/

# 4. Port forward
kubectl port-forward svc/flask-devops-demo 5000:5000

# 5. Test (in another terminal)
curl http://localhost:5000/health
```

---

## 📁 Project Structure

```
flask-devops-demo/
├── Jenkinsfile                      # 11-stage CI/CD pipeline
├── sonar-project.properties         # SonarQube configuration
├── Dockerfile                       # Production container
├── app.py                           # Flask app with metrics
├── test_app.py                      # Test suite
├── requirements.txt                 # Dependencies
├── README.md                        # This file
│
├── k8s/                             # Kubernetes manifests
│   ├── deployment.yaml
│   └── service.yaml
│
└── helm/                            # Helm chart
    └── flask-devops-demo/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
```

---
![alt text](<Screenshot 1948-03-31 at 1.14.04 PM.png>)
## 📊 Kubernetes Management

```bash
# View resources
kubectl get pods
kubectl get svc
kubectl get deployment

# Debug
kubectl describe pod <pod-name>
kubectl logs -f <pod-name>

# Scale
kubectl scale deployment flask-devops-demo --replicas=5

# Port forward
kubectl port-forward svc/flask-devops-demo 5000:5000
```

---

## 🔄 Helm Charts

```bash
# Validate chart
helm lint helm/flask-devops-demo

# Install
helm install flask-devops-demo helm/flask-devops-demo

# Upgrade
helm upgrade flask-devops-demo helm/flask-devops-demo

# Uninstall
helm uninstall flask-devops-demo
```

---

## 🔧 Local Development

### Build & Deploy

```bash
# Build Docker image
docker build -t flask-devops-demo:latest .

# Restart deployment
kubectl rollout restart deployment/flask-devops-demo
```

### Run Tests

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest --cov=. --junitxml=test-results.xml

# Coverage report
open htmlcov/index.html
```

---

## 🔄 CI/CD Pipeline Setup

### Install Jenkins (Docker)

```bash
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /Users/mac/jenkins:/var/jenkins_home \
  jenkins/jenkins:lts-alpine

# Get password
docker logs jenkins | grep -i "initial admin password"
```

### Configure Credentials

Jenkins UI → Manage Jenkins → Manage Credentials → Add:

| Credential | Type | Details |
|-----------|------|---------|
| dockerhub-creds | Username/Password | Docker Hub credentials |
| MINIKUBE_KUBECONFIG | Secret file | ~/.kube/config |
| sonarqube-token | Secret text | SonarQube API token |
| argocd-token | Secret text | ArgoCD API token |

### Create Pipeline Job

1. **New Item** → `flask-devops-demo` → **Pipeline** → OK
2. **Pipeline** section:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository: `https://github.com/skbablualam/flask-devops-demo.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
3. **Save** → **Build Now**

---

## 📊 Monitoring Stack

### Deploy Prometheus

```bash
kubectl create namespace monitoring
kubectl apply -f prometheus-config.yaml -n monitoring
kubectl port-forward -n monitoring svc/prometheus-server 9090:80
```

### Deploy Grafana

```bash
kubectl apply -f grafana-dashboard.yaml -n monitoring
kubectl port-forward -n monitoring svc/grafana 3000:80

# Access: http://localhost:3000 (admin/admin)
```

---

## ✨ Key Features

### 🐳 Docker
- ✅ Multi-stage optimized build
- ✅ Non-root user (appuser)
- ✅ Health checks enabled
- ✅ Gunicorn with 4 workers
- ✅ Minimal base image (python:3.11-slim)

### ☸️ Kubernetes
- ✅ 3 pod replicas
- ✅ HPA (2-5 replicas)
- ✅ Liveness & Readiness probes
- ✅ Resource limits & requests
- ✅ NetworkPolicy for security
- ✅ LoadBalancer service

### 📊 Monitoring
- ✅ Prometheus metrics (/metrics)
- ✅ 40+ metrics collected
- ✅ 3 custom Flask metrics

### 🔐 Security
- ✅ SonarQube code analysis
- ✅ Trivy container scanning
- ✅ Bandit security scanning
- ✅ Pylint & flake8 linting
- ✅ Network policies
- ✅ Non-root user

---

## 🛠️ Troubleshooting

### Docker Issues
```bash
pkill -f Docker && open -a Docker
docker ps
```

### Minikube Issues
```bash
minikube status
minikube logs | tail -50
minikube delete && minikube start --driver=docker
```

### Pod Issues
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl delete pod <pod-name>
```

### Jenkins Issues
```bash
docker logs jenkins
# Jenkins UI → Pipeline name → Console Output
```

---

## 📚 Documentation Files

- `QUICK_REFERENCE.md` - Daily commands (print it!)
- `MACBOOK_SETUP.md` - MacBook operations guide
- `LOCAL_SETUP.md` - Local development setup
- `QUICKSTART.md` - Jenkins pipeline guide
- `DEVOPS_SETUP.md` - Full DevOps architecture
- `CONFIG_SUMMARY.md` - Technical reference
- `CURRENT_STATUS.txt` - Current system status

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 👥 Support

- 📖 Check documentation files
- 🔍 Review troubleshooting sections
- 💬 Open GitHub issues
- 📧 Contact DevOps team

---

**Last Updated**: 2025-06-20  
**Status**: ✅ Production Ready  
**Tested On**: macOS, Docker Desktop, Minikube v1.38+
