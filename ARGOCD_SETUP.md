# ArgoCD Setup & Integration Guide

Complete guide to deploy ArgoCD, get secrets, and integrate with your CI/CD pipeline.

---

## 🎯 What is ArgoCD?

ArgoCD is a **GitOps deployment tool** that:
- Automatically deploys applications from Git repositories
- Keeps your Kubernetes cluster in sync with Git
- Makes deployments reproducible and auditable
- Integrates with Jenkins for automated GitOps workflows

**In your pipeline:**
```
Jenkins Pipeline
    ↓
Build Docker image
    ↓
Push to Docker Hub
    ↓
ArgoCD (GitOps)
    ↓
Deploy to Kubernetes
    ↓
Application Running ✅
```

---

## 📋 ArgoCD Prerequisites

Before installing ArgoCD, ensure you have:

✅ Kubernetes cluster running (Minikube)
```bash
minikube status
```

✅ kubectl configured
```bash
kubectl cluster-info
```

✅ Helm installed (we installed it earlier)
```bash
helm version
```

✅ At least 2GB free memory in cluster
```bash
kubectl top nodes
```

---

## 🚀 Step 1: Deploy ArgoCD to Kubernetes

### Option A: Using Helm (Recommended)

```bash
# Add ArgoCD Helm repository
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Create namespace
kubectl create namespace argocd

# Install ArgoCD
helm install argocd argo/argo-cd \
  --namespace argocd \
  --values - << EOF
  server:
    service:
      type: LoadBalancer
    extraArgs:
      - --insecure
  configs:
    secret:
      argocdServerAdminPassword: ""
EOF

# Wait for pods to be ready (2-3 minutes)
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=argocd-server \
  -n argocd --timeout=300s

# Verify installation
kubectl get all -n argocd
```

### Option B: Using kubectl (Direct YAML)

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=argocd-server \
  -n argocd --timeout=300s

# Verify
kubectl get pods -n argocd
```

---

## 🔌 Step 2: Access ArgoCD Web UI

### Port Forward to Local Machine

```bash
# Terminal 1: Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Access: https://localhost:8080
# (Ignore SSL warning - self-signed cert)
```

### Get Initial Admin Password

```bash
# Get password from secret
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo

# Output: (random password string)
```

### Login to ArgoCD UI

1. **Open**: https://localhost:8080
2. **Username**: `admin`
3. **Password**: (from command above)
4. Click **Sign In**

---

## 🔑 Step 3: Create ArgoCD API Token (for Jenkins)

### In ArgoCD Web UI

1. **Log in** (step above)
2. **Navigate to**: User Settings (gear icon top right)
3. **Click**: Account → Tokens
4. **Click**: Generate New
5. **Configure**:
   - Token name: `jenkins-token`
   - Token expiration: `720h` (30 days)
6. **Click**: Generate
7. **COPY**: Token (won't be shown again!)

### Or Via Command Line

```bash
# Generate token via argocd CLI
argocd account generate-token \
  --account jenkins-token \
  --namespace argocd

# Output: (long JWT token)

# Save this token - you'll need it for Jenkins!
```

---

## 🔐 Step 4: Add Credentials to Jenkins

### Add ArgoCD Server URL

**In Jenkins UI:**
1. **Manage Jenkins** → **Manage Credentials**
2. **Global** → **Add Credentials**
3. **Configure**:
   - Kind: `Secret text`
   - Secret: `https://localhost:8080` (or your ArgoCD URL)
   - ID: `argocd-server`
   - Description: `ArgoCD Server URL`
4. Click **Create**

### Add ArgoCD Token

**In Jenkins UI:**
1. **Manage Jenkins** → **Manage Credentials**
2. **Global** → **Add Credentials**
3. **Configure**:
   - Kind: `Secret text`
   - Secret: (paste token from Step 3)
   - ID: `argocd-token`
   - Description: `ArgoCD Authentication Token`
4. Click **Create**

---

## 📝 Step 5: Create Git Repository for ArgoCD

ArgoCD watches a Git repository for deployment manifests.

### Create Repository Structure

```bash
# Create repo (or use existing)
mkdir -p ~/argocd-deployment-repo
cd ~/argocd-deployment-repo

# Create directory structure
mkdir -p apps/flask-devops-demo

# Create deployment manifest
cat > apps/flask-devops-demo/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-devops-demo
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-devops-demo
  template:
    metadata:
      labels:
        app: flask-devops-demo
    spec:
      containers:
      - name: flask
        image: skbablualam03031997/flask-devops-demo:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: flask-devops-demo
  namespace: default
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
  selector:
    app: flask-devops-demo
EOF

# Create Kustomization file (optional but recommended)
cat > apps/flask-devops-demo/kustomization.yaml << 'EOF'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

commonLabels:
  app: flask-devops-demo
  managed-by: argocd
EOF

# Initialize Git repo
git init
git add .
git commit -m "Initial deployment configuration"

# Push to GitHub (if using remote repo)
# git remote add origin https://github.com/YOUR_USERNAME/argocd-deployment-repo.git
# git push -u origin main
```

---

## 🔄 Step 6: Create ArgoCD Application

### Via Web UI

1. **Log in** to ArgoCD: https://localhost:8080
2. **Click**: New App
3. **Configure**:

**General:**
- Application Name: `flask-devops-demo`
- Project: `default`

**Source:**
- Repository URL: `https://github.com/YOUR_USERNAME/argocd-deployment-repo.git` (or local path)
- Revision: `HEAD`
- Path: `apps/flask-devops-demo`

**Destination:**
- Cluster URL: `https://kubernetes.default.svc`
- Namespace: `default`

4. **Click**: Create

### Via CLI

```bash
argocd app create flask-devops-demo \
  --repo https://github.com/YOUR_USERNAME/argocd-deployment-repo.git \
  --path apps/flask-devops-demo \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default

# Sync the application
argocd app sync flask-devops-demo
```

---

## 🔗 Step 7: Configure Jenkinsfile for ArgoCD

Your Jenkinsfile already has ArgoCD integration! (Stage 8)

### Relevant Stage in Jenkinsfile

```groovy
stage('ArgoCD GitOps Deployment') {
    when {
        branch 'main'
    }
    steps {
        script {
            withCredentials([
                string(credentialsId: 'argocd-server', variable: 'ARGOCD_SERVER'),
                string(credentialsId: 'argocd-token', variable: 'ARGOCD_TOKEN')
            ]) {
                sh '''
                    # Login to ArgoCD
                    argocd login $ARGOCD_SERVER \
                        --username admin \
                        --password $ARGOCD_TOKEN \
                        --insecure
                    
                    # Update application
                    argocd app set flask-devops-demo \
                        -p image=skbablualam03031997/flask-devops-demo:${BUILD_NUMBER}
                    
                    # Sync to latest
                    argocd app sync flask-devops-demo
                    
                    # Wait for sync
                    argocd app wait flask-devops-demo
                '''
            }
        }
    }
}
```

---

## 🎯 How It Works in Your Pipeline

### Complete Flow

```
1. Developer Pushes Code to GitHub
           ↓
2. Jenkins Webhook Triggered
           ↓
3. Stage 1-2: Checkout & Test Code
           ↓
4. Stage 3-6: SonarQube, Build Docker, Trivy, Push
           ↓
5. Stage 7: Helm Chart Validation
           ↓
6. Stage 8: ArgoCD Updates
   - Logs into ArgoCD
   - Updates image version
   - Triggers sync
           ↓
7. Stage 9: Deploy to Kubernetes
           ↓
8. Stage 10-11: Prometheus & Grafana Setup
           ↓
9. Application Deployed ✅
```

---

## 📊 ArgoCD Credentials for Jenkins

| Credential ID | Type | Value | Purpose |
|---|---|---|---|
| `argocd-server` | Secret text | `https://localhost:8080` | ArgoCD server URL |
| `argocd-token` | Secret text | JWT token from Step 3 | Authentication token |

---

## 🔍 Monitor ArgoCD Deployments

### Via Web UI

```
https://localhost:8080
→ Applications
→ flask-devops-demo
→ View sync status, health, history
```

### Via CLI

```bash
# List applications
argocd app list

# Get app status
argocd app get flask-devops-demo

# View app logs
argocd app logs flask-devops-demo

# Sync app
argocd app sync flask-devops-demo

# Watch sync progress
argocd app wait flask-devops-demo
```

### Via kubectl

```bash
# Check ArgoCD resources
kubectl get all -n argocd

# Check deployed application
kubectl get deployment,svc flask-devops-demo -n default

# View app pod logs
kubectl logs -f deployment/flask-devops-demo
```

---

## 🛠️ Troubleshooting ArgoCD

### ArgoCD Pod Not Starting

```bash
# Check pod status
kubectl describe pod -n argocd -l app.kubernetes.io/name=argocd-server

# Check logs
kubectl logs -f -n argocd deployment/argocd-server

# Common issue: Memory
kubectl top pods -n argocd
# If high, increase Minikube memory: minikube config set memory 8192
```

### Can't Login to ArgoCD Web UI

```bash
# Reset admin password
kubectl patch secret argocd-secret \
  -n argocd \
  -p '{"data": {"admin.password": null}}'

# Get new password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### Token Expired

```bash
# Generate new token
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# Create new app-specific token
argocd account generate-token \
  --account jenkins-token \
  --namespace argocd

# Update in Jenkins credentials
```

### Application Sync Fails

**Check:**
```bash
# View app details
argocd app get flask-devops-demo

# Check Git connectivity
argocd repo list

# Check cluster connectivity
argocd cluster list

# Manual sync
argocd app sync flask-devops-demo --force
```

---

## 📈 ArgoCD + Jenkins Integration Benefits

✅ **Automated GitOps**
- Changes in Git → Automatic K8s deployment
- All changes tracked in Git
- Easy rollback to any commit

✅ **Audit Trail**
- Every deployment logged
- Who changed what and when
- Complete version history

✅ **Continuous Deployment**
- Push Docker image → Jenkins builds
- Jenkins triggers ArgoCD → Auto deployment
- No manual kubectl commands needed

✅ **Multi-Environment**
- Deploy to dev, staging, prod
- Each environment in different Git branch
- Consistent deployments

---

## 🚀 Complete Setup Checklist

```
[ ] Step 1: Deploy ArgoCD to Kubernetes
    [ ] Create namespace
    [ ] Install ArgoCD (Helm or kubectl)
    [ ] Wait for pods to be ready

[ ] Step 2: Access ArgoCD UI
    [ ] Port forward: kubectl port-forward
    [ ] Get admin password
    [ ] Login to https://localhost:8080

[ ] Step 3: Create API Token
    [ ] In ArgoCD UI: Settings → Tokens
    [ ] Generate new token
    [ ] Copy token (save somewhere safe)

[ ] Step 4: Add to Jenkins
    [ ] Add argocd-server credential
    [ ] Add argocd-token credential
    [ ] Verify in Manage Credentials

[ ] Step 5: Create Deployment Repo
    [ ] Create Git repository
    [ ] Add deployment manifests
    [ ] Push to GitHub

[ ] Step 6: Create ArgoCD Application
    [ ] In ArgoCD UI: New App
    [ ] Configure source (Git repo)
    [ ] Configure destination (K8s cluster)
    [ ] Sync the application

[ ] Step 7: Configure Jenkins
    [ ] Jenkinsfile stage 8 enabled
    [ ] Credentials configured
    [ ] Test pipeline execution

[ ] Step 8: Verify Integration
    [ ] Push code to Git
    [ ] Jenkins pipeline runs
    [ ] ArgoCD deploys automatically
    [ ] Application running in K8s
```

---

## 📚 Quick Reference Commands

### Deploy ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Access ArgoCD
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# URL: https://localhost:8080
```

### Get Admin Password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo
```

### Create Token
```bash
argocd account generate-token --account jenkins-token --namespace argocd
```

### Check Status
```bash
# ArgoCD pods
kubectl get pods -n argocd

# Deployed app
kubectl get all -n default

# ArgoCD app status
argocd app list
argocd app get flask-devops-demo
```

---

## 🎯 Next Steps

1. **Deploy ArgoCD** (Step 1-2 above)
2. **Get token** (Step 3)
3. **Add to Jenkins** (Step 4)
4. **Create deployment repo** (Step 5)
5. **Create ArgoCD app** (Step 6)
6. **Test with pipeline** (Run `Build Now`)

---

**Status**: Ready to deploy ArgoCD  
**Time**: 15-20 minutes for complete setup  
**Benefits**: Full GitOps automation, audit trail, easy rollbacks

