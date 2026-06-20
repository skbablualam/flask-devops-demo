# Quick Start Guide - Flask DevOps Demo Pipeline

## Prerequisites

- ✅ Jenkins server running
- ✅ Docker installed
- ✅ Kubernetes cluster (minikube/EKS/GKE)
- ✅ Git repository access

## Step 1: Setup Jenkins Credentials

```bash
# In Jenkins UI: Manage Jenkins → Manage Credentials → Global → Add Credentials

1. Docker Hub Credentials
   - Kind: Username with password
   - Username: <your-dockerhub-username>
   - Password: <your-dockerhub-token>
   - ID: dockerhub-creds

2. Kubernetes Config
   - Kind: Secret file
   - File: ~/.kube/config (or your kubeconfig)
   - ID: MINIKUBE_KUBECONFIG

3. SonarQube Host URL
   - Kind: Secret text
   - Secret: http://sonarqube-server:9000
   - ID: sonarqube-host-url

4. SonarQube Token
   - Kind: Secret text
   - Secret: <generate from SonarQube admin>
   - ID: sonarqube-token

5. ArgoCD Server
   - Kind: Secret text
   - Secret: https://argocd-server.example.com
   - ID: argocd-server

6. ArgoCD Token
   - Kind: Secret text
   - Secret: <generate from ArgoCD>
   - ID: argocd-token
```

## Step 2: Setup SonarQube

```bash
# Option A: Docker
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:h2:tcp://localhost:9092/sonarqube \
  -e SONAR_JDBC_LOGIN=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:lts

# Access: http://localhost:9000
# Default: admin/admin

# Generate token:
# 1. Click admin profile (top right)
# 2. Security → Tokens
# 3. Generate new token
# 4. Copy to Jenkins credential 'sonarqube-token'

# Option B: Kubernetes
kubectl create namespace sonarqube
helm repo add sonarqube https://SonarSource.github.io/helm-chart-sonarqube
helm install sonarqube sonarqube/sonarqube -n sonarqube
```

## Step 3: Setup Monitoring Stack

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Install Prometheus Operator (recommended)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring

# Install Grafana
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana \
  --namespace monitoring

# Port forward to access
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
kubectl port-forward svc/grafana 3000:80 -n monitoring

# Grafana login: admin/prom-operator (or get password: kubectl get secret grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 -d)
```

## Step 4: Setup ArgoCD (Optional but Recommended)

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get initial password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Login to ArgoCD and generate API token
# Access: https://localhost:8080
# Username: admin
# Password: <from above>

# Create API token:
# Settings → Account → Tokens → Generate new

# Copy token to Jenkins credential 'argocd-token'
```

## Step 5: Create Jenkins Pipeline

### Using Jenkinsfile from Git

1. In Jenkins: New Item → Pipeline
2. Name: `flask-devops-demo`
3. In Pipeline section:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: https://github.com/skbablualam/flask-devops-demo.git
   - Branch: */main
   - Script Path: Jenkinsfile

4. Save and Build

### Or: Copy-Paste Jenkinsfile

1. In Jenkins: New Item → Pipeline
2. Name: `flask-devops-demo`
3. In Pipeline section:
   - Definition: Pipeline script
   - Copy entire Jenkinsfile content
4. Save and Build

## Step 6: Build Environment Variables Update

Edit the Jenkinsfile to match your environment:

```groovy
environment {
    IMAGE = "YOUR_DOCKER_REGISTRY/flask-devops-demo:${BUILD_NUMBER}"
    IMAGE_LATEST = "YOUR_DOCKER_REGISTRY/flask-devops-demo:latest"
    SONAR_HOST_URL = credentials('sonarqube-host-url')
    SONAR_LOGIN = credentials('sonarqube-token')
    DOCKER_REGISTRY = "docker.io"  # Change if using different registry
    HELM_RELEASE_NAME = "flask-devops-demo"
    HELM_NAMESPACE = "default"
    ARGOCD_SERVER = credentials('argocd-server')
    ARGOCD_TOKEN = credentials('argocd-token')
    PROMETHEUS_NAMESPACE = "monitoring"
    GRAFANA_NAMESPACE = "monitoring"
}
```

## Step 7: Configure Kubernetes

```bash
# Create namespaces
kubectl create namespace default
kubectl create namespace monitoring
kubectl create namespace argocd

# Create service accounts if needed
kubectl create serviceaccount jenkins -n default
kubectl create clusterrolebinding jenkins-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=default:jenkins
```

## Step 8: Test Local Development

```bash
# Clone repo
git clone https://github.com/skbablualam/flask-devops-demo.git
cd flask-devops-demo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest --cov=. --cov-report=html

# Run app
python app.py

# Test endpoints in another terminal:
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/metrics
```

## Step 9: First Pipeline Run

1. In Jenkins: Select `flask-devops-demo` job
2. Click "Build Now"
3. Monitor Console Output
4. Verify each stage:
   - ✅ Checkout
   - ✅ Unit Tests
   - ✅ SonarQube Analysis
   - ✅ Build Docker
   - ✅ Trivy Scan
   - ✅ Push Docker
   - ✅ Helm Chart
   - ✅ ArgoCD Deployment
   - ✅ Kubernetes Deploy
   - ✅ Prometheus Setup
   - ✅ Grafana Setup

## Step 10: Verify Deployments

```bash
# Check Kubernetes deployment
kubectl get pods -n default
kubectl get svc -n default

# Check logs
kubectl logs -f deployment/flask-devops-demo -n default

# Port forward to app
kubectl port-forward svc/flask-devops-demo 8080:80 -n default

# Test application
curl http://localhost:8080/health
```

## Step 11: View Results

### SonarQube
- URL: http://sonarqube:9000
- Project: flask-devops-demo
- Check code quality, coverage, vulnerabilities

### Prometheus
- URL: http://localhost:9090
- Query: `flask_http_requests_total`
- View metrics collected from Flask app

### Grafana
- URL: http://localhost:3000
- Login: admin/password
- View Flask DevOps Demo dashboard
- Metrics visualized:
  - HTTP Requests (rate)
  - Response Time (latency)
  - Error Rate
  - Memory Usage
  - CPU Usage

### ArgoCD
- URL: https://localhost:8080
- View `flask-devops-demo` application
- Monitor sync status
- See deployment history

## Troubleshooting

### Pipeline Stages Fail

**SonarQube Stage**
```bash
# Verify connection
curl http://sonarqube:9000/api/system/health

# Check token validity
curl -u admin:token http://sonarqube:9000/api/user_tokens/search
```

**Docker Push Stage**
```bash
# Verify credentials
docker login -u username

# Test push manually
docker tag flask-devops-demo:latest username/flask-devops-demo:latest
docker push username/flask-devops-demo:latest
```

**Kubernetes Deploy**
```bash
# Check kubeconfig
kubectl cluster-info

# Verify namespace
kubectl get namespaces

# Check pod status
kubectl describe pod <pod-name> -n default
```

### Monitoring Not Working

```bash
# Verify Flask metrics endpoint
kubectl port-forward svc/flask-devops-demo 5000:5000
curl http://localhost:5000/metrics

# Check Prometheus targets
# URL: http://localhost:9090/targets

# Verify ServiceMonitor (if using Prometheus Operator)
kubectl get servicemonitor -n monitoring
```

## Performance Considerations

- **HPA**: Auto-scales between 2-5 replicas
- **Resource Limits**: 256Mi-512Mi RAM, 250m-500m CPU
- **Health Checks**: 30s liveness, 10s readiness
- **Gunicorn Workers**: 4 workers for concurrency

## Security Notes

1. **Container Security**
   - Non-root user (appuser)
   - Security scanning with Trivy
   - Regular image scans

2. **Code Security**
   - SonarQube analysis
   - Bandit security scanning
   - Pylint/flake8 linting

3. **Access Control**
   - Network policies
   - RBAC in Kubernetes
   - ArgoCD authentication

## Next Steps

1. ✅ Pipeline is running successfully
2. 🔍 Review SonarQube quality gates
3. 📊 Setup Grafana alert rules
4. 🔐 Configure GitOps deployment strategy
5. 📈 Monitor application performance

---

For detailed information, see [DEVOPS_SETUP.md](DEVOPS_SETUP.md)

Contact: DevOps Team
