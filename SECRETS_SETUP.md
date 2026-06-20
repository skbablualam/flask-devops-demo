# Jenkins Secrets & Credentials Setup Guide

Complete guide to obtaining and configuring all required secrets for the CI/CD pipeline.

---

## 📋 Secrets Needed for Pipeline

Your Jenkinsfile requires these 7 credentials:

| # | Credential ID | Type | Purpose | Status |
|---|---|---|---|---|
| 1 | `dockerhub-creds` | Username/Password | Push images to Docker Hub | ✅ **DONE** |
| 2 | `MINIKUBE_KUBECONFIG` | Secret file | Deploy to Kubernetes | ✅ **DONE** |
| 3 | `sonarqube-host-url` | Secret text | SonarQube server URL | ⏳ **NEEDED** |
| 4 | `sonarqube-token` | Secret text | SonarQube authentication | ⏳ **NEEDED** |
| 5 | `argocd-server` | Secret text | ArgoCD server URL | ⏳ Optional |
| 6 | `argocd-token` | Secret text | ArgoCD authentication | ⏳ Optional |
| 7 | `github-token` | Secret text | GitHub access (webhooks) | ⏳ Optional |

**Note**: Trivy & Prometheus don't need secrets - they're auto-installed during pipeline execution.

---

## 🔑 Where to Get Each Secret

### ✅ 1. Docker Hub Credentials (Already Done!)

**You already have:** `dockerhub-creds` ✅

These come from Docker Hub:
- Username: Your Docker Hub username
- Password/Token: Generate at https://hub.docker.com/settings/security → Access Tokens

---

### ✅ 2. Minikube Kubeconfig (Already Done!)

**You already have:** `MINIKUBE_KUBECONFIG` ✅

This is your local kubectl config:
```bash
# Already configured at:
~/.kube/config
```

---

### ⏳ 3. SonarQube Host URL

**Status**: You need to set this up

**Two Options:**

#### Option A: Use SonarQube Cloud (Recommended - Free)

1. Go to: https://sonarcloud.io/
2. Click **Sign up** (or Sign in if you have account)
3. Choose **GitHub** for login (easiest)
4. Authorize SonarCloud
5. Create organization or use existing
6. Get your **Organization Key**

**Where to find:**
- Dashboard → Administration → Organization Settings
- Copy the **Organization Key**

**In Jenkins, add credential:**
- ID: `sonarqube-host-url`
- Secret: `https://sonarqube.cloud` (or your custom URL)

#### Option B: Deploy SonarQube Server Locally

Run in Docker:
```bash
# Start SonarQube
docker run -d --name sonarqube \
  -p 9000:9000 \
  sonarqube:latest

# Wait for startup (3-5 minutes)
# Access: http://localhost:9000
# Default login: admin/admin

# Get your URL
echo "http://localhost:9000"
```

**In Jenkins, add credential:**
- ID: `sonarqube-host-url`
- Secret: `http://localhost:9000`

---

### ⏳ 4. SonarQube Token

**Status**: You need to generate this

#### If Using SonarQube Cloud:

1. Go to: https://sonarcloud.io/account/security
2. Click **Generate Token**
3. Name it: `jenkins-token`
4. Click **Generate**
5. **Copy the token immediately** (won't be shown again)

#### If Using Local SonarQube Server:

1. Go to: `http://localhost:9000`
2. Login with `admin/admin`
3. Click user avatar (top right) → **My Account**
4. Go to **Security** tab
5. Under **Tokens**, enter name: `jenkins-token`
6. Click **Generate**
7. **Copy the token immediately**

**In Jenkins, add credential:**
- ID: `sonarqube-token`
- Secret: (paste the token you just copied)

---

### ⏳ 5. ArgoCD Server URL (Optional)

**Status**: Optional - only needed for GitOps deployment

#### Deploy ArgoCD in Kubernetes:

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# Port forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Access: https://localhost:8080
# Default username: admin
# Default password (get it):
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**In Jenkins, add credential:**
- ID: `argocd-server`
- Secret: `https://localhost:8080` (or your ArgoCD server URL)

---

### ⏳ 6. ArgoCD Token (Optional)

**Status**: Optional - only needed for GitOps deployment

1. Access ArgoCD UI: `https://localhost:8080`
2. Login with admin credentials (username: `admin`, password from above)
3. Go to **Settings** → **Accounts** → **Tokens**
4. Click **Generate New**
5. Name: `jenkins-token`
6. Expiration: `720h` (30 days)
7. Click **Generate**
8. **Copy the token immediately**

**In Jenkins, add credential:**
- ID: `argocd-token`
- Secret: (paste the token you just copied)

---

### ⏳ 7. GitHub Token (Optional)

**Status**: Optional - only needed for webhooks

#### Generate GitHub Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Configure:
   - Token name: `Jenkins Pipeline`
   - Expiration: `90 days`
   - Scopes: Select these:
     - ✅ `repo` (full control of private repositories)
     - ✅ `admin:repo_hook` (write access to hooks)
     - ✅ `admin:org_hook` (write access to org hooks)
4. Click **Generate token**
5. **Copy the token immediately** (won't be shown again)

**In Jenkins, add credential:**
- ID: `github-token`
- Secret: (paste the token you just copied)

---

## 🔧 Add Credentials to Jenkins

### Step-by-Step in Jenkins UI

1. **Jenkins Home** → **Manage Jenkins** → **Manage Credentials**
2. Click **global** under "Global credentials (unrestricted)"
3. Click **+ Add Credentials** (top left)

### Add SonarQube Host URL

1. **Kind**: Secret text
2. **Secret**: `https://sonarcloud.io` (or your server URL)
3. **ID**: `sonarqube-host-url`
4. **Description**: `SonarQube Server URL`
5. Click **Create**

### Add SonarQube Token

1. **Kind**: Secret text
2. **Secret**: (paste your SonarQube token)
3. **ID**: `sonarqube-token`
4. **Description**: `SonarQube Authentication Token`
5. Click **Create**

### Add ArgoCD Server (Optional)

1. **Kind**: Secret text
2. **Secret**: `https://localhost:8080`
3. **ID**: `argocd-server`
4. **Description**: `ArgoCD Server URL`
5. Click **Create**

### Add ArgoCD Token (Optional)

1. **Kind**: Secret text
2. **Secret**: (paste your ArgoCD token)
3. **ID**: `argocd-token`
4. **Description**: `ArgoCD Authentication Token`
5. Click **Create**

### Add GitHub Token (Optional)

1. **Kind**: Secret text
2. **Secret**: (paste your GitHub token)
3. **ID**: `github-token`
4. **Description**: `GitHub Personal Access Token`
5. Click **Create**

---

## 📊 Trivy & Prometheus (No Secrets Needed!)

### Trivy Image Scanning

✅ **No credentials needed!**

Trivy:
- Downloads automatically during pipeline
- Scans container image for vulnerabilities
- Generates report: `trivy-report.json`
- No authentication required

**What it does:**
```bash
# Pipeline runs this automatically
trivy image --severity HIGH,CRITICAL $IMAGE --format json --output trivy-report.json
```

---

### Prometheus Monitoring

✅ **No credentials needed!**

Prometheus:
- Deployed automatically by pipeline
- Creates namespace: `monitoring`
- Scrapes metrics from pod: `:5000/metrics`
- No authentication required

**What it does:**
```bash
# Pipeline creates monitoring namespace
kubectl create namespace monitoring

# Pipeline deploys Prometheus config
kubectl apply -f prometheus-config.yaml -n monitoring
```

---

## ✅ Verification Checklist

After adding all credentials, verify in Jenkins:

1. **Go to**: Manage Jenkins → Manage Credentials
2. Check these exist:
   - ✅ `dockerhub-creds` (Username/Password)
   - ✅ `MINIKUBE_KUBECONFIG` (Secret file)
   - ✅ `sonarqube-host-url` (Secret text)
   - ✅ `sonarqube-token` (Secret text)
   - ⏳ `argocd-server` (Optional)
   - ⏳ `argocd-token` (Optional)
   - ⏳ `github-token` (Optional)

---

## 🚀 After Adding Secrets

### Run Pipeline Test

1. **Jenkins Dashboard** → Click on `flask-devops-demo` job
2. Click **Build Now**
3. Monitor the build:
   - Stage 1: Checkout ✅
   - Stage 2: Unit Tests ✅
   - Stage 3: SonarQube Analysis ✅ (will use `sonarqube-host-url` & `sonarqube-token`)
   - Stage 4-11: Other stages...

### Check Pipeline Logs

If stage fails, click **Console Output** to see:
```bash
# Look for these messages:
✅ Using credential: sonarqube-host-url
✅ Using credential: sonarqube-token
✅ SonarQube analysis completed
✅ Trivy scan completed
✅ Prometheus setup completed
```

---

## 🐛 Troubleshooting Secrets

### Credential Not Found Error

**Error**: `Credential 'sonarqube-token' not found`

**Solution**:
1. Verify credential exists: Manage Jenkins → Manage Credentials
2. Check spelling matches exactly
3. Re-create credential if needed

### SonarQube Analysis Fails

**Error**: `401 Unauthorized` or connection failed

**Check**:
1. `sonarqube-host-url` is correct
2. `sonarqube-token` is valid and not expired
3. SonarQube server is running (if local)
4. Firewall allows connection

**Test locally**:
```bash
# Test SonarQube connection
curl -u admin:token_here http://localhost:9000/api/user/current
```

### Token Expired

**Solution**:
1. Generate new token (follow steps above)
2. Update credential in Jenkins
3. Run pipeline again

---

## 📚 Quick Reference

### For Quick Setup (Minimum)

You only NEED these 2:
1. ✅ `dockerhub-creds` (already done)
2. ✅ `MINIKUBE_KUBECONFIG` (already done)
3. ⏳ `sonarqube-host-url` (add this)
4. ⏳ `sonarqube-token` (add this)

### For Full Setup

Add optional ones if you want:
5. ⏳ `argocd-server` (for GitOps)
6. ⏳ `argocd-token` (for GitOps)
7. ⏳ `github-token` (for webhooks)

### Nothing Needed For:
- Trivy (auto-installed)
- Prometheus (auto-deployed)

---

## 🎯 Next Steps

### Immediate (Today)

1. ✅ Already done:
   - `dockerhub-creds` ✅
   - `MINIKUBE_KUBECONFIG` ✅

2. ⏳ Add SonarQube credentials:
   - Go to https://sonarcloud.io (free)
   - Generate token
   - Add to Jenkins:
     - `sonarqube-host-url`: `https://sonarcloud.io`
     - `sonarqube-token`: (your token)

### This Week

3. Test pipeline: **Build Now** in Jenkins
4. Monitor: Console Output to see all stages
5. Verify metrics: Prometheus collecting data

### Optional Later

6. Add ArgoCD for GitOps
7. Add GitHub webhooks
8. Deploy monitoring dashboards

---

## 💡 Pro Tips

✅ **Save tokens securely**
- Use password manager (1Password, LastPass, Bitwarden)
- Never commit tokens to Git
- Never share tokens

✅ **Rotate tokens regularly**
- Regenerate every 30-90 days
- Delete old tokens
- Update Jenkins credentials

✅ **Use SonarQube Cloud for free**
- No server to maintain
- Free tier includes:
  - Unlimited projects
  - Public repos included
  - 200k LOC limit per month

---

**Status**: Ready to add secrets  
**Next**: Add SonarQube credentials  
**Time**: 10 minutes to complete
