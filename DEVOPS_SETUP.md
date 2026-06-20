# Flask DevOps Demo - Complete Setup Guide

This document outlines the DevOps pipeline components and setup instructions for the Flask DevOps Demo application.

## Pipeline Components

### 1. **SonarQube Code Analysis**
   - **Purpose**: Automated code quality scanning and security analysis
   - **Configuration**: `sonar-project.properties`
   - **Metrics Tracked**:
     - Code coverage
     - Code smells
     - Security hotspots
     - Bugs and vulnerabilities
   - **Setup**:
     ```bash
     # SonarQube Server (Docker)
     docker run -d --name sonarqube -p 9000:9000 sonarqube:lts
     
     # Access at http://localhost:9000
     # Default credentials: admin/admin
     ```
   - **Jenkins Credentials Required**:
     - `sonarqube-host-url`: URL of SonarQube server
     - `sonarqube-token`: SonarQube authentication token

### 2. **Trivy Image Scanning**
   - **Purpose**: Container image vulnerability scanning
   - **Configuration**: Integrated in Jenkinsfile
   - **Scans For**:
     - HIGH and CRITICAL severity vulnerabilities
     - OS and application dependencies
   - **Output**: `trivy-report.json`
   - **Setup**:
     ```bash
     # Install Trivy
     wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add -
     echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list
     apt-get install -y trivy
     ```

### 3. **Helm Charts**
   - **Purpose**: Kubernetes deployment templating and versioning
   - **Structure**:
     ```
     helm/flask-devops-demo/
     ├── Chart.yaml
     ├── values.yaml
     └── templates/
         ├── deployment.yaml
         ├── service.yaml
         ├── _helpers.tpl
     ```
   - **Features**:
     - Scalable replication
     - Automatic service discovery
     - Health checks (liveness & readiness probes)
     - Resource limits and requests
     - HPA (Horizontal Pod Autoscaler)
   - **Usage**:
     ```bash
     # Install
     helm install flask-devops-demo helm/flask-devops-demo \
       --namespace default --create-namespace
     
     # Upgrade
     helm upgrade flask-devops-demo helm/flask-devops-demo \
       --values helm/flask-devops-demo/values.yaml
     
     # Validate
     helm lint helm/flask-devops-demo
     ```

### 4. **ArgoCD GitOps Deployment**
   - **Purpose**: Declarative GitOps-based deployment
   - **Configuration**: `argocd-apps/flask-demo-app.yaml`
   - **Features**:
     - Automatic sync from Git repository
     - Self-healing deployments
     - Automated pruning of orphaned resources
   - **Setup**:
     ```bash
     # Install ArgoCD
     kubectl create namespace argocd
     kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
     
     # Access ArgoCD
     kubectl port-forward svc/argocd-server -n argocd 8080:443
     # URL: http://localhost:8080
     # Default: admin/password
     
     # Get password
     kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
     ```
   - **Jenkins Credentials Required**:
     - `argocd-server`: ArgoCD server URL
     - `argocd-token`: ArgoCD API token

### 5. **Prometheus Monitoring**
   - **Purpose**: Metrics collection and monitoring
   - **Metrics Exposed**:
     - `flask_http_requests_total`: Total HTTP requests by method, endpoint, status
     - `flask_http_request_duration_seconds`: Request latency histogram
     - `flask_active_requests`: Current active request count
   - **Configuration**: Created automatically by pipeline in `prometheus-config.yaml`
   - **Setup**:
     ```bash
     # Install Prometheus Operator (recommended)
     helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
     helm install prometheus prometheus-community/kube-prometheus-stack \
       --namespace monitoring --create-namespace
     
     # Or install manually
     kubectl create namespace monitoring
     kubectl apply -f prometheus-config.yaml -n monitoring
     ```
   - **Access**:
     ```bash
     kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
     # URL: http://localhost:9090
     ```

### 6. **Grafana Dashboards**
   - **Purpose**: Data visualization and alerting
   - **Pre-configured Panels**:
     - HTTP Requests (5m rate)
     - Response Time (p95 latency)
     - Error Rate (5xx responses)
     - Memory Usage
     - CPU Usage
   - **Setup**:
     ```bash
     # Install Grafana via Helm
     helm repo add grafana https://grafana.github.io/helm-charts
     helm install grafana grafana/grafana \
       --namespace monitoring \
       --values grafana-values.yaml
     
     # Access Grafana
     kubectl port-forward svc/grafana 3000:80 -n monitoring
     # URL: http://localhost:3000
     # Default: admin/admin (change on first login)
     ```
   - **Dashboards**: Automatically imported from `grafana-dashboard.yaml`

## Jenkins Pipeline Stages

1. **Checkout**: Clone repository from GitHub
2. **Unit Tests**: Run pytest with coverage reporting
3. **SonarQube Code Analysis**: Quality gates and security scanning
4. **Build Docker Image**: Build and tag container image
5. **Trivy Image Scanning**: Vulnerability scanning of container image
6. **Push Docker Image**: Push to Docker Hub registry
7. **Helm Chart Deployment**: Validate and prepare Helm deployment
8. **ArgoCD GitOps Deployment**: Create ArgoCD Application manifest
9. **Deploy to Kubernetes**: Apply manifests to cluster
10. **Prometheus Monitoring Setup**: Configure metrics collection
11. **Grafana Dashboards Setup**: Create visualization dashboards

## Jenkins Credentials Setup

Add the following credentials to Jenkins:

| Credential ID | Type | Description |
|---|---|---|
| `dockerhub-creds` | Username/Password | Docker Hub registry credentials |
| `MINIKUBE_KUBECONFIG` | File | Kubernetes config file |
| `sonarqube-host-url` | Secret text | SonarQube server URL |
| `sonarqube-token` | Secret text | SonarQube authentication token |
| `argocd-server` | Secret text | ArgoCD server URL |
| `argocd-token` | Secret text | ArgoCD API token |

## Application Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Home page |
| `/health` | GET | Health check (JSON) |
| `/metrics` | GET | Prometheus metrics |

## Health Check

```bash
curl http://localhost:5000/health
# Returns: {"status": "UP"}
```

## Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest --cov=. --cov-report=html

# Run application
python app.py

# Access application
curl http://localhost:5000/
```

## Docker Build & Run

```bash
# Build image
docker build -t flask-devops-demo:1.0.0 .

# Run container
docker run -d -p 5000:5000 \
  --name flask-demo \
  flask-devops-demo:1.0.0

# View logs
docker logs -f flask-demo
```

## Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace default

# Apply manifests
kubectl apply -f k8s/ -n default

# Check deployment status
kubectl rollout status deployment/flask-devops-demo -n default

# Port forward
kubectl port-forward svc/flask-devops-demo 8080:80 -n default
```

## Monitoring Stack Deployment

```bash
# Deploy monitoring stack
kubectl apply -f prometheus-config.yaml -n monitoring
kubectl apply -f grafana-dashboard.yaml -n monitoring

# Access Prometheus
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring

# Access Grafana
kubectl port-forward svc/grafana 3000:80 -n monitoring
```

## Troubleshooting

### SonarQube Analysis Fails
- Verify SonarQube server is running: `curl http://sonarqube-host:9000/api/system/health`
- Check token is valid: `curl -u admin:token http://sonarqube-host:9000/api/user_tokens/search`

### Trivy Scan Issues
- Update Trivy database: `trivy image --download-db-only`
- Check network access to vulnerability database

### ArgoCD Deployment Fails
- Verify ArgoCD server is accessible
- Check Git repository permissions
- Validate Application manifest: `kubectl describe app flask-devops-demo -n argocd`

### Prometheus Metrics Not Appearing
- Verify Flask pod is accessible: `kubectl port-forward svc/flask-devops-demo 5000:5000`
- Check metrics endpoint: `curl http://localhost:5000/metrics`
- Verify ServiceMonitor is created

### Grafana Dashboards Empty
- Ensure Prometheus is properly connected as data source
- Check Prometheus scrape configuration: `http://prometheus:9090/targets`

## Security Best Practices

1. **Container Security**
   - Run as non-root user (implemented in Dockerfile)
   - Use read-only root filesystem where possible
   - Regularly scan images with Trivy
   - Use minimal base images (python:3.11-slim)

2. **Code Security**
   - Regular SonarQube scans
   - Dependency vulnerability scanning (bandit, safety)
   - Static code analysis with flake8, pylint

3. **Kubernetes Security**
   - Network policies implemented
   - Resource limits and requests
   - Health checks (liveness & readiness probes)
   - Security context for containers

4. **Access Control**
   - Use Jenkins credentials for sensitive data
   - Implement RBAC in Kubernetes
   - Secure ArgoCD authentication

## Performance Optimization

- **Horizontal Pod Autoscaling (HPA)**: Scales based on CPU/Memory usage
- **Resource Limits**: Prevents resource exhaustion
- **Caching**: Prometheus metric caching
- **Multi-worker Gunicorn**: 4 workers for concurrent request handling

## CI/CD Best Practices

- Automated testing on every commit
- Code quality gates before merge
- Container image vulnerability scanning
- Automated Kubernetes deployment
- GitOps-based infrastructure management
- Continuous monitoring and alerting

---

For more information, visit the [GitHub Repository](https://github.com/skbablualam/flask-devops-demo)
