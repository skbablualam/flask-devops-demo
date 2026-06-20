# Jenkins Setup Guide for Flask DevOps Demo

Complete guide to install, configure, and run Jenkins for the Flask DevOps Demo CI/CD pipeline.

---

## 📋 Prerequisites

Before starting Jenkins, ensure you have:

✅ Docker Desktop running on macOS
✅ Minikube cluster running (`minikube status` = Running)
✅ kubectl configured (`kubectl config current-context`)
✅ Git installed
✅ Docker Hub account (username & token)
✅ GitHub account with repository access
✅ 8GB+ available disk space

---

## 🚀 Step 1: Install Jenkins

### Option A: Docker (Recommended) ⭐

The easiest and cleanest way to run Jenkins on macOS.

```bash
# Create Jenkins volume directory
mkdir -p /Users/mac/jenkins

# Run Jenkins in Docker
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /Users/mac/jenkins:/var/jenkins_home \
  -v /Users/mac/.kube:/root/.kube:ro \
  jenkins/jenkins:lts-alpine

# Wait for Jenkins to start (30-60 seconds)
sleep 60

# Get initial admin password
docker logs jenkins | grep -A 5 "Jenkins initial setup is required"
# or
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Save the password somewhere safe!

**Verify Jenkins is running:**
```bash
docker ps | grep jenkins
# Should see: jenkins container running on port 8080
```

### Option B: Homebrew (macOS Only)

If you prefer native macOS installation:

```bash
# Install Jenkins
brew install jenkins-lts

# Start Jenkins service
brew services start jenkins-lts

# Check status
brew services list | grep jenkins

# View logs
cat /usr/local/var/log/jenkins.log

# Stop Jenkins
brew services stop jenkins-lts
```

### Option C: Manual Download

```bash
# Download Jenkins WAR
cd /Users/mac && mkdir -p jenkins-standalone
cd jenkins-standalone
curl -O http://mirrors.jenkins.io/war-stable/latest/jenkins.war

# Run Jenkins
java -jar jenkins.war --httpPort=8080

# Access: http://localhost:8080
```

---

## 🔐 Step 2: Initial Jenkins Setup

### Access Jenkins UI

1. Open browser: `http://localhost:8080`
2. You'll see the "Unlock Jenkins" page
3. Paste the initial admin password from Step 1

### Complete Setup Wizard

1. **Unlock Jenkins** - Paste the admin password
2. **Customize Jenkins** - Click "Install suggested plugins"
3. **Wait for plugins** to install (5-10 minutes)
4. **Create Admin User**:
   - Username: `admin`
   - Password: Create a strong password
   - Full name: `DevOps Admin`
   - Email: Your email
5. **Jenkins URL** - Keep as `http://localhost:8080/`
6. **Start using Jenkins** - Click to finish

### Initial Configuration

After setup, go to **Manage Jenkins → System Configuration**:

- Configure system hostname if needed
- Set email notifications (optional)
- Keep other defaults

---

## 🔑 Step 3: Install Required Plugins

### Via Jenkins UI

1. **Manage Jenkins** → **Manage Plugins**
2. Click **Available plugins** tab
3. Search and install these plugins:

| Plugin | Purpose |
|--------|---------|
| Git | Clone repositories |
| Pipeline | Jenkins Declarative Pipelines |
| Docker Pipeline | Docker integration |
| Kubernetes | Kubernetes plugin |
| SonarQube Scanner | Code quality analysis |
| Performance | Performance test result reporting |
| Email Extension | Email notifications |
| Blue Ocean | Better UI (optional but nice) |
| AnsiColor | Colorful logs |

**Installation Steps:**
1. Search for plugin
2. Check checkbox
3. Click "Install without restart"
4. After all installed, restart Jenkins

**Restart Jenkins:**
```bash
# Docker
docker restart jenkins

# Homebrew
brew services restart jenkins-lts
```

---

## 🔐 Step 4: Configure Credentials

### Add Docker Hub Credentials

1. **Manage Jenkins** → **Manage Credentials**
2. Click **global** under "Global credentials"
3. Click **+ Add Credentials** (top left)

**Credential 1: Docker Hub**
- Kind: **Username with password**
- Username: Your Docker Hub username
- Password: Your Docker Hub access token (generate at hub.docker.com/settings/security)
- ID: `dockerhub-creds`
- Click **Create**

**Credential 2: Minikube Kubeconfig**
- Kind: **Secret file**
- File: Select your `~/.kube/config` file
- ID: `MINIKUBE_KUBECONFIG`
- Click **Create**

**Credential 3: SonarQube Token**
- Kind: **Secret text**
- Secret: Generate SonarQube token (if deployed)
- ID: `sonarqube-token`
- Click **Create**

**Credential 4: ArgoCD Token**
- Kind: **Secret text**
- Secret: Generate ArgoCD token (if deployed)
- ID: `argocd-token`
- Click **Create**

**Credential 5: GitHub Token** (Optional)
- Kind: **Secret text**
- Secret: Generate GitHub Personal Access Token (GitHub Settings → Developer Settings → Personal Access Tokens)
- ID: `github-token`
- Click **Create**

---

## 🔧 Step 5: Configure System Settings

### Configure Git

1. **Manage Jenkins** → **System Configuration**
2. Find **Git** section
3. Set:
   - User name: `Jenkins`
   - User email: `jenkins@example.com`
4. **Apply** → **Save**

### Configure Docker

If using Docker plugin:

1. **Manage Jenkins** → **System Configuration**
2. Find **Docker** section
3. Set:
   - Docker Host URI: `unix:///var/run/docker.sock`
4. **Apply** → **Save**

### Configure SonarQube (Optional)

1. **Manage Jenkins** → **System Configuration**
2. Find **SonarQube Servers** section
3. Add:
   - Name: `sonarqube`
   - Server URL: `http://sonarqube:9000`
   - Server authentication token: Select `sonarqube-token`
4. **Apply** → **Save**

---

## 📝 Step 6: Create Pipeline Job

### Create the Pipeline

1. Click **New Item**
2. Enter job name: `flask-devops-demo`
3. Select **Pipeline** → Click **OK**
4. On the configuration page:

**General Section:**
- Description: `Flask DevOps Demo CI/CD Pipeline`
- Check "GitHub project"
- Project url: `https://github.com/skbablualam/flask-devops-demo`

**Build Triggers Section:**
- Check **GitHub hook trigger for GITScm polling** (for webhooks)

**Pipeline Section:**
- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/skbablualam/flask-devops-demo.git`
- Credentials: Select your GitHub credentials (or None if public repo)
- Branch specifier: `*/main` or `*/master`
- Script path: `Jenkinsfile`

5. Click **Save**

---

## 🚀 Step 7: Run the Pipeline

### Manual Build

1. Open the `flask-devops-demo` job
2. Click **Build Now** (top left)
3. Click on the build number to view progress
4. Click **Console Output** to see logs

### Pipeline Execution

You should see the 11 stages execute:

```
✅ Stage 1: Checkout
✅ Stage 2: Unit Tests
✅ Stage 3: SonarQube Code Analysis
✅ Stage 4: Build Docker Image
✅ Stage 5: Trivy Image Scanning
✅ Stage 6: Push Docker Image
✅ Stage 7: Helm Chart Deployment
✅ Stage 8: ArgoCD GitOps
✅ Stage 9: Deploy to Kubernetes
✅ Stage 10: Prometheus Monitoring
✅ Stage 11: Grafana Dashboards
```

### View Build Status

- **Blue Ocean UI**: Click "Open Blue Ocean" (if installed)
- **Classic UI**: Click the build number
- **Console Output**: Click "Console Output"

---

## 🐛 Step 8: Troubleshooting

### Jenkins won't start

```bash
# Check if port 8080 is in use
lsof -i :8080

# Kill process using port 8080
kill -9 <PID>

# Restart Jenkins
docker restart jenkins
```

### Pipeline build fails at checkout

```bash
# Check git is installed
git --version

# Check repository is accessible
git clone https://github.com/skbablualam/flask-devops-demo.git
```

### Docker not accessible from Jenkins

```bash
# Verify Docker socket is mounted
docker exec jenkins ls -la /var/run/docker.sock

# Verify Jenkins can run Docker commands
docker exec jenkins docker ps
```

### Credentials not working

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Verify credentials exist
3. Test credentials in job configuration
4. Re-create if needed

### Pod deployment fails

```bash
# Check kubeconfig is accessible
docker exec jenkins ls -la /root/.kube/config

# Test kubectl from Jenkins
docker exec jenkins kubectl get nodes
```

### SonarQube analysis fails

```bash
# Check SonarQube server is running
curl http://sonarqube:9000

# Verify SonarQube token in credentials
# Re-generate token if needed
```

---

## 📊 Step 9: Monitor Pipeline Execution

### During Build

1. Click the build number in Jenkins
2. View **Console Output** for real-time logs
3. Scroll to see each stage's output

### After Build Completes

1. Check **Build Log** for errors
2. View **Artifacts** (test results, reports)
3. Check **Test Results**
4. Review **Code Coverage**

### Pipeline History

1. Click job name
2. View **Build History** on left side
3. Click previous builds to compare
4. Check trends over time

---

## 🔄 Step 10: Setup Webhooks (Optional)

### GitHub Webhook

Enable automatic builds when code is pushed:

1. Go to your GitHub repository
2. **Settings** → **Webhooks** → **Add webhook**
3. Set:
   - Payload URL: `http://your-public-ip:8080/github-webhook/`
   - Content type: `application/json`
   - Trigger: Push events
   - Click **Add webhook**

### GitLab Webhook

Similar process for GitLab:

1. Repository → **Settings** → **Integrations** → **Add**
2. Set URL and trigger events
3. Save

---

## 🛠️ Common Jenkins Tasks

### Stop Jenkins

```bash
# Docker
docker stop jenkins

# Homebrew
brew services stop jenkins-lts
```

### Start Jenkins

```bash
# Docker
docker start jenkins

# Homebrew
brew services start jenkins-lts
```

### View Jenkins Logs

```bash
# Docker
docker logs -f jenkins

# Homebrew
tail -f /usr/local/var/log/jenkins.log
```

### Reset Jenkins Password

```bash
# Docker: Execute script in container
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Homebrew: View logs
cat /usr/local/var/log/jenkins.log
```

### Backup Jenkins

```bash
# Docker: Copy volume
docker cp jenkins:/var/jenkins_home /Users/mac/jenkins-backup

# Homebrew: Copy directory
cp -r /Users/Shared/Jenkins /Users/mac/jenkins-backup
```

---

## 📚 Additional Resources

- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Pipeline Plugin](https://plugins.jenkins.io/docker-workflow/)
- [Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/)

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Jenkins UI accessible at http://localhost:8080
- [ ] Admin user login works
- [ ] All plugins installed successfully
- [ ] Docker credentials configured
- [ ] Kubernetes credentials configured
- [ ] Pipeline job created
- [ ] First build executed successfully
- [ ] All 11 stages completed
- [ ] Flask app deployed to Kubernetes
- [ ] Endpoints accessible (/, /health, /metrics)

---

## 🎉 Next Steps

1. **Monitor Pipeline**: Watch builds in real-time
2. **Configure Alerts**: Set up email notifications
3. **Deploy Infrastructure**: Set up SonarQube, ArgoCD, Prometheus, Grafana
4. **Enable Webhooks**: Auto-trigger on GitHub push
5. **Optimize Performance**: Tune Jenkins settings for faster builds
6. **Backup Configuration**: Save Jenkins home directory regularly

---

**Status**: ✅ Jenkins Ready  
**Last Updated**: 2025-06-20  
**Tested On**: macOS, Docker Desktop
