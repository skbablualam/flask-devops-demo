# Quick Secrets & Helm Troubleshooting Guide

## 🎯 Your Questions Answered

---

## 1️⃣ Where to Get SonarQube Secret?

### ✅ Quick Setup (5 minutes)

**SonarQube Host URL:**
```
https://sonarcloud.io
```
(Free SonarQube cloud - no installation needed)

**SonarQube Token:**
1. Go to: https://sonarcloud.io/account/security
2. Click **Generate Token**
3. Name: `jenkins-token`
4. Copy the token

**Add to Jenkins:**
- Manage Jenkins → Manage Credentials → Global → Add Credentials
- **Kind**: Secret text
- **Secret**: (your token)
- **ID**: `sonarqube-token`

See detailed guide: `SECRETS_SETUP.md`

---

## 2️⃣ Where to Get Trivy Secret?

### ✅ Good News: Trivy doesn't need a secret! ✅

**Why?**
- Trivy is a vulnerability scanner
- It installs automatically during pipeline execution
- It scans local Docker images (no credentials needed)
- No external authentication required

**What it does:**
```bash
# Pipeline runs this automatically during stage 5
trivy image --severity HIGH,CRITICAL $IMAGE --output trivy-report.json
```

**No action needed!** ✅

---

## 3️⃣ Where to Get Prometheus Secret?

### ✅ Good News: Prometheus doesn't need a secret! ✅

**Why?**
- Prometheus is deployed automatically by pipeline
- It runs inside your Kubernetes cluster
- No external authentication required
- It scrapes metrics from your Flask app's `/metrics` endpoint

**What it does:**
```bash
# Pipeline runs this automatically during stage 10
kubectl create namespace monitoring
kubectl apply -f prometheus-config.yaml -n monitoring
```

**No action needed!** ✅

---

## 4️⃣ Why is Helm File Showing Red?

### ✅ Short Answer: Nothing's wrong! ✅

**Evidence:**
```bash
helm lint helm/flask-devops-demo
# Result: 1 chart(s) linted, 0 chart(s) failed ✅
```

### What might cause red in VS Code:

**Possible Causes:**

1. **VS Code Kubernetes Extension** looking for namespace declaration
   - **Fix**: Ignore - charts are valid
   - **Why**: Extension sometimes shows warnings for templated values

2. **VS Code Language Server** not recognizing Helm syntax
   - **Fix**: Install "Helm" extension in VS Code
   - **How**: 
     - VS Code → Extensions
     - Search "Helm"
     - Install by "technosophos"

3. **YAML validation** being too strict
   - **Fix**: Disable strict validation
   - **How**:
     ```json
     // VS Code settings.json
     "yaml.validate": false
     // or
     "yaml.schemaStore.enable": false
     ```

### How to Verify Helm is Fine:

```bash
# Terminal check
helm lint helm/flask-devops-demo
# Output: 1 chart(s) linted, 0 chart(s) failed ✅

# Dry run check
helm template flask-devops-demo helm/flask-devops-demo
# Output: Valid YAML manifests ✅

# Installation check
helm install flask-devops-demo helm/flask-devops-demo --dry-run
# Output: No errors ✅
```

---

## 📋 Credentials Status

### Already Configured ✅
- [x] `dockerhub-creds` - Docker Hub credentials
- [x] `MINIKUBE_KUBECONFIG` - Kubernetes config

### Need to Add ⏳ (2 minutes each)
- [ ] `sonarqube-host-url` - See section 1 above
- [ ] `sonarqube-token` - See section 1 above

### Optional ⏳
- [ ] `argocd-server` - Only if using GitOps
- [ ] `argocd-token` - Only if using GitOps
- [ ] `github-token` - Only if using webhooks

### No Credentials Needed ✅
- [x] Trivy - Auto-installed, no auth
- [x] Prometheus - Auto-deployed, no auth

---

## 🚀 What to Do Now

### Step 1: Add SonarQube (5 minutes)

**Go to Jenkins:**
1. Manage Jenkins → Manage Credentials
2. Global → Add Credentials
3. Add `sonarqube-host-url`:
   - Kind: Secret text
   - Secret: `https://sonarcloud.io`
   - ID: `sonarqube-host-url`
4. Add `sonarqube-token`:
   - Kind: Secret text
   - Secret: (from sonarcloud.io/account/security)
   - ID: `sonarqube-token`

### Step 2: Test Pipeline (1 minute)

**Go to Jenkins:**
1. Click `flask-devops-demo` job
2. Click **Build Now**
3. Wait for completion

**You should see:**
```
✅ Stage 1: Checkout
✅ Stage 2: Unit Tests
✅ Stage 3: SonarQube Analysis ← Uses your new credentials
✅ Stage 4: Build Docker
✅ Stage 5: Trivy Image Scanning ← No credentials needed
...
✅ Stage 10: Prometheus Monitoring ← No credentials needed
✅ Stage 11: Grafana Dashboards
```

### Step 3: Fix VS Code Helm Red (Optional)

If you still see red in VS Code:

**Option A: Install Helm Extension (Recommended)**
1. VS Code → Extensions
2. Search: "Helm"
3. Click install on "Helm" by technosophos
4. Reload VS Code

**Option B: Disable YAML Validation**
1. VS Code → Settings (Cmd + ,)
2. Search: "yaml.validate"
3. Uncheck the box

---

## 📊 Complete Credentials Checklist

```
JENKINS CREDENTIALS NEEDED:

✅ ALREADY DONE:
   □ dockerhub-creds (Docker Hub username & token)
   □ MINIKUBE_KUBECONFIG (~/.kube/config file)

⏳ NEED TO ADD (2 credentials):
   □ sonarqube-host-url (https://sonarcloud.io)
   □ sonarqube-token (generate from sonarcloud.io)

⏳ OPTIONAL (3 credentials):
   □ argocd-server (ArgoCD URL)
   □ argocd-token (ArgoCD token)
   □ github-token (GitHub personal token)

✅ NO CREDENTIALS NEEDED:
   ✓ Trivy (auto-installs, no auth)
   ✓ Prometheus (auto-deploys, no auth)
```

---

## 🎯 Summary

| Question | Answer | Action |
|----------|--------|--------|
| **Where is SonarQube secret?** | https://sonarcloud.io | Generate token, add to Jenkins |
| **Where is Trivy secret?** | ✅ Not needed! | Skip - auto-installs during pipeline |
| **Where is Prometheus secret?** | ✅ Not needed! | Skip - auto-deploys during pipeline |
| **Why Helm showing red?** | ✅ Helm is valid! Linting passed | Optional: Install Helm VS Code extension |

---

## 🚀 Next Action

**Do this now (5 minutes):**
1. Go to: https://sonarcloud.io/account/security
2. Generate token
3. Add 2 credentials to Jenkins (sonarqube-host-url, sonarqube-token)
4. Run `Build Now` on pipeline
5. Watch all 11 stages execute ✅

---

## 📞 Help Commands

```bash
# Verify Helm is valid
helm lint helm/flask-devops-demo

# Test Helm templates
helm template flask-devops-demo helm/flask-devops-demo

# Check Jenkins credentials exist
# UI: Manage Jenkins → Manage Credentials → Global

# View pipeline logs
# UI: Jenkins job → Recent builds → Console Output

# Check pod logs for metrics
kubectl logs -f deployment/flask-devops-demo | grep prometheus
```

---

**Status**: Ready to add SonarQube credentials  
**Time**: 5 minutes  
**Next**: Sections in SECRETS_SETUP.md for detailed instructions
