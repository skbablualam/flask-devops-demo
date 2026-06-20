# ⚡ Quick Reference - Flask DevOps Demo

## 🚀 30-Second Startup

```bash
# Terminal 1
open -a Docker && sleep 120 && minikube start && eval $(minikube docker-env)

# Terminal 2
kubectl port-forward svc/flask-devops-demo 5000:5000

# App is ready at: http://localhost:5000 ✅
```

---

## 📍 Essential URLs

```
Home:       http://localhost:5000/
Health:     http://localhost:5000/health
Metrics:    http://localhost:5000/metrics
```

---

## 🛠️ Essential Commands

| Task | Command |
|------|---------|
| **Start Docker** | `open -a Docker` |
| **Start Minikube** | `minikube start` |
| **Point to Minikube** | `eval $(minikube docker-env)` |
| **Port Forward** | `kubectl port-forward svc/flask-devops-demo 5000:5000` |
| **View Pods** | `kubectl get pods` |
| **View Logs** | `kubectl logs -f deployment/flask-devops-demo` |
| **Rebuild Image** | `docker build -t flask-devops-demo:latest .` |
| **Redeploy** | `kubectl rollout restart deployment/flask-devops-demo` |
| **Scale to 5 replicas** | `kubectl scale deployment flask-devops-demo --replicas=5` |
| **Shell in Pod** | `kubectl exec -it <pod-name> -- /bin/bash` |
| **Stop Everything** | `minikube stop` |

---

## 📊 Status Check

```bash
# All in one command
docker ps && minikube status && kubectl get pods && kubectl get svc
```

---

## 🔄 Rebuild & Test

```bash
# After code changes
docker build -t flask-devops-demo:latest . && \
kubectl rollout restart deployment/flask-devops-demo && \
sleep 5 && \
kubectl port-forward svc/flask-devops-demo 5000:5000 &
sleep 2 && \
curl http://localhost:5000/health
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **MACBOOK_SETUP.md** | 📋 Daily operations & common tasks |
| **LOCAL_SETUP.md** | 🔧 Detailed local setup guide |
| **QUICKSTART.md** | 🚀 Jenkins pipeline setup |
| **DEVOPS_SETUP.md** | 📖 Full architecture guide |
| **CONFIG_SUMMARY.md** | 📝 Complete technical reference |
| **CURRENT_STATUS.txt** | ✅ Current system status |

---

## 🆘 Quick Fixes

**Docker Won't Start**
```bash
pkill -f Docker && open -a Docker
```

**Minikube Issues**
```bash
minikube delete && minikube start
```

**Metrics Not Working**
```bash
kubectl rollout restart deployment/flask-devops-demo
```

**Pod Keep Crashing**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

---

## ✅ Verify Everything Works

```bash
# Test all endpoints
curl http://localhost:5000/             # Should show app message
curl http://localhost:5000/health        # Should show {"status":"UP"}
curl http://localhost:5000/metrics | head -5  # Should show metrics
```

---

## 📊 System Status

- 🐳 Docker: Running ✅
- ☸️ Minikube: Running ✅
- 📦 Flask App: 3/3 pods ✅
- 🔧 Gunicorn: 4 workers ✅

---

## 🎯 Next Steps

1. **Local Dev**: Edit code → rebuild → redeploy
2. **Testing**: `pytest --cov=.`
3. **Jenkins**: Follow QUICKSTART.md

---

**Print this page for quick reference!**
