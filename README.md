# Flask DevOps Demo 🚀

A complete end-to-end DevOps project demonstrating CI/CD automation using Jenkins, Docker, Kubernetes (Minikube), and GitHub.

The application is a simple Python Flask web application that is automatically tested, containerized, pushed to Docker Hub, and deployed to Kubernetes running on Minikube.

---

## 📌 Project Overview

This project showcases a modern DevOps workflow:

GitHub → Jenkins Pipeline → Docker Build → Docker Hub → Kubernetes (Minikube)

### CI/CD Pipeline Stages

✅ Source Code Checkout

✅ Python Dependency Installation

✅ Automated Testing with Pytest

✅ Docker Image Build

✅ Docker Image Push to Docker Hub

✅ Kubernetes Deployment using kubectl

---

## 🏗️ Tech Stack

- Python Flask
- Pytest
- Jenkins
- Docker
- Docker Hub
- Kubernetes
- Minikube
- GitHub
- macOS (MacBook)

---

## 📂 Project Structure

```text
flask-devops-demo/
│
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
└── README.md
```

---

## ⚙️ Prerequisites

Install the following:

- Docker Desktop
- Minikube
- kubectl
- Jenkins
- Git
- Python 3

Verify installation:

```bash
docker --version
kubectl version --client
minikube version
git --version
python3 --version
```

---

## 🚀 Run Application Locally

Clone the repository:

```bash
git clone https://github.com/skbablualam/flask-devops-demo.git

cd flask-devops-demo
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
python app.py
```

Access:

```text
http://localhost:5000
```

---

## 🧪 Run Tests

```bash
pytest
```

Expected Result:

```text
1 passed
```

---

## 🐳 Build Docker Image

```bash
docker build -t flask-devops-demo .
```

Run container:

```bash
docker run -d -p 5001:5000 flask-devops-demo
```

Access application:

```text
http://localhost:5001
```

---

## 📦 Push Image to Docker Hub

Build image:

```bash
docker build -t <dockerhub-username>/flask-devops-demo:v1 .
```

Login:

```bash
docker login
```

Push image:

```bash
docker push <dockerhub-username>/flask-devops-demo:v1
```

---

## ☸️ Kubernetes Deployment (Minikube)

Start Minikube:

```bash
minikube start
```

Apply manifests:

```bash
kubectl apply -f k8s/
```

Verify deployment:

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
```

Access service:

```bash
minikube service flask-service
```

---

## 🔄 Jenkins CI/CD Pipeline

The Jenkins pipeline performs the following actions automatically:

1. Checkout source code from GitHub
2. Install Python dependencies
3. Execute Pytest test cases
4. Build Docker image
5. Push image to Docker Hub
6. Deploy application to Kubernetes (Minikube)

Pipeline file:

```text
Jenkinsfile
```

---

## 📸 Successful Pipeline Execution

The project has been successfully tested and deployed using:

- Jenkins running in Docker container
- Docker Desktop on macOS
- Minikube Kubernetes Cluster
- Docker Hub Registry

Pipeline Status:

```text
SUCCESS
```
![alt text](<Screenshot 1948-03-29 at 7.24.11 PM.png>) ![alt text](<Screenshot 1948-03-29 at 7.25.18 PM.png>)

All stages completed successfully:

✅ Checkout

✅ Test

✅ Build Docker

✅ Push Docker

✅ Deploy to Kubernetes

---

## 🌐 Docker Hub Repository

```text
https://hub.docker.com/r/skbablualam03031997/flask-devops-demo
```

---

## 📈 Future Enhancements

- SonarQube Code Analysis
- Trivy Image Scanning
- Helm Charts
- ArgoCD GitOps Deployment
- Prometheus Monitoring
- Grafana Dashboards

---

## 👨‍💻 Author

**Bablu Alam**

DevOps Engineer

GitHub:
https://github.com/skbablualam

LinkedIn:
https://www.linkedin.com/in/bablu-alam

---

## 🎯 Learning Outcome

This project demonstrates practical experience with:

- CI/CD Pipeline Creation
- Jenkins Automation
- Docker Containerization
- Docker Hub Integration
- Kubernetes Deployments
- Minikube Cluster Management
- GitHub Integration
- DevOps Best Practices

⭐ If you found this project useful, feel free to fork, star, and contribute.

# flask-devops-demo
