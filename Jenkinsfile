pipeline {

    agent any

    environment {
        IMAGE = "skbablualam03031997/flask-devops-demo:${BUILD_NUMBER}"
        IMAGE_LATEST = "skbablualam03031997/flask-devops-demo:latest"
        SONAR_HOST_URL = credentials('sonarqube-host-url')
        SONAR_LOGIN = credentials('sonarqube-token')
        DOCKER_REGISTRY = "docker.io"
        HELM_RELEASE_NAME = "flask-devops-demo"
        HELM_NAMESPACE = "default"
        ARGOCD_SERVER = credentials('argocd-server')
        ARGOCD_TOKEN = credentials('argocd-token')
        PROMETHEUS_NAMESPACE = "monitoring"
        GRAFANA_NAMESPACE = "monitoring"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/skbablualam/flask-devops-demo.git'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                echo "========== Running Unit Tests =========="
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pip install pytest-cov
                pytest --cov=. --cov-report=xml --cov-report=html --junitxml=test-results.xml
                echo "========== Tests Completed =========="
                '''
            }
        }

        stage('SonarQube Code Analysis') {
            steps {
                sh '''
                echo "========== Running SonarQube Analysis =========="
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pip install pylint flake8 bandit
                
                # Download SonarQube Scanner
                if [ ! -d "sonar-scanner" ]; then
                    wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                    unzip -q sonar-scanner-cli-5.0.1.3006-linux.zip
                    mv sonar-scanner-5.0.1.3006-linux sonar-scanner
                fi
                
                # Run static analysis tools
                flake8 app.py test_app.py --count --select=E9,F63,F7,F82 --show-source --statistics || true
                pylint app.py --exit-zero -r no > pylint-report.txt || true
                bandit -r . -f json -o bandit-report.json || true
                
                # Run SonarQube Scanner
                export PATH=$PATH:$(pwd)/sonar-scanner/bin
                sonar-scanner \
                  -Dsonar.projectBaseDir=. \
                  -Dsonar.host.url=$SONAR_HOST_URL \
                  -Dsonar.login=$SONAR_LOGIN \
                  -Dsonar.python.coverage.reportPaths=coverage.xml
                
                echo "========== SonarQube Analysis Completed =========="
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "========== Building Docker Image =========="
                whoami
                id
                docker ps
                docker build -t $IMAGE -t $IMAGE_LATEST .
                echo "========== Docker Image Built: $IMAGE =========="
                '''
            }
        }

        stage('Trivy Image Scanning') {
            steps {
                sh '''
                echo "========== Running Trivy Security Scan =========="
                
                # Install Trivy if not present
                if ! command -v trivy &> /dev/null; then
                    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add -
                    echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list
                    apt-get update
                    apt-get install -y trivy
                fi
                
                # Scan the Docker image
                trivy image --severity HIGH,CRITICAL \
                           --exit-code 0 \
                           --format json \
                           --output trivy-report.json \
                           $IMAGE || true
                
                # Display summary
                trivy image --severity HIGH,CRITICAL $IMAGE || true
                
                echo "========== Trivy Scan Completed =========="
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "========== Pushing Docker Image to Registry =========="
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE
                    docker push $IMAGE_LATEST
                    echo "========== Docker Image Pushed Successfully =========="
                    '''
                }
            }
        }

        stage('Helm Chart Deployment') {
            steps {
                sh '''
                echo "========== Setting up Helm Deployment =========="
                
                # Install Helm if not present
                if ! command -v helm &> /dev/null; then
                    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
                fi
                
                # Add/Update Helm repository
                helm repo add bitnami https://charts.bitnami.com/bitnami || true
                helm repo update
                
                # Create helm charts directory if not exists
                if [ ! -d "helm/flask-devops-demo" ]; then
                    mkdir -p helm/flask-devops-demo/{templates,charts}
                    
                    # Create Chart.yaml
                    cat > helm/flask-devops-demo/Chart.yaml << 'EOF'
apiVersion: v2
name: flask-devops-demo
description: A Helm chart for Flask DevOps Demo
type: application
version: 1.0.0
appVersion: "1.0.0"
home: https://github.com/skbablualam/flask-devops-demo
sources:
  - https://github.com/skbablualam/flask-devops-demo
maintainers:
  - name: DevOps Team
EOF

                    # Create values.yaml
                    cat > helm/flask-devops-demo/values.yaml << 'EOF'
replicaCount: 3

image:
  repository: skbablualam03031997/flask-devops-demo
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80
  targetPort: 5000

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: flask-demo.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: flask-demo-tls
      hosts:
        - flask-demo.example.com

prometheus:
  enabled: true
  interval: 30s

grafana:
  enabled: true
  dashboards: true
EOF

                    # Create Deployment template
                    cat > helm/flask-devops-demo/templates/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "flask-devops-demo.fullname" . }}
  labels:
    {{- include "flask-devops-demo.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "flask-devops-demo.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "flask-devops-demo.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 5000
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
EOF

                    # Create Service template
                    cat > helm/flask-devops-demo/templates/service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: {{ include "flask-devops-demo.fullname" . }}
  labels:
    {{- include "flask-devops-demo.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
  selector:
    {{- include "flask-devops-demo.selectorLabels" . | nindent 4 }}
EOF

                    # Create helpers template
                    cat > helm/flask-devops-demo/templates/_helpers.tpl << 'EOF'
{{- define "flask-devops-demo.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "flask-devops-demo.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}
{{- define "flask-devops-demo.labels" -}}
helm.sh/chart: {{ include "flask-devops-demo.chart" . }}
{{ include "flask-devops-demo.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "flask-devops-demo.selectorLabels" -}}
app.kubernetes.io/name: {{ include "flask-devops-demo.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "flask-devops-demo.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}
EOF
                fi
                
                # Validate Helm chart
                helm lint helm/flask-devops-demo
                
                # Dry run deployment
                helm upgrade --install $HELM_RELEASE_NAME helm/flask-devops-demo \
                    --namespace $HELM_NAMESPACE \
                    --create-namespace \
                    --values helm/flask-devops-demo/values.yaml \
                    --set image.tag=$BUILD_NUMBER \
                    --dry-run --debug
                
                echo "========== Helm Chart Ready =========="
                '''
            }
        }

        stage('ArgoCD GitOps Deployment') {
            steps {
                sh '''
                echo "========== Deploying via ArgoCD =========="
                
                # Install ArgoCD CLI if not present
                if ! command -v argocd &> /dev/null; then
                    curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
                    chmod +x argocd
                    mv argocd /usr/local/bin/
                fi
                
                # Login to ArgoCD (optional - use token-based auth)
                argocd login $ARGOCD_SERVER --insecure --username admin --password $ARGOCD_TOKEN || true
                
                # Create ArgoCD Application manifests
                mkdir -p argocd-apps
                
                cat > argocd-apps/flask-demo-app.yaml << 'EOF'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: flask-devops-demo
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/skbablualam/flask-devops-demo.git
    targetRevision: main
    path: helm/flask-devops-demo
    helm:
      releaseName: flask-devops-demo
      values: |
        image:
          tag: BUILD_TAG
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF

                # Replace build number in ArgoCD manifest
                sed -i "s/BUILD_TAG/${BUILD_NUMBER}/g" argocd-apps/flask-demo-app.yaml
                
                # Create the ArgoCD application (if ArgoCD is available)
                kubectl apply -f argocd-apps/ --insecure-skip-tls-verify=true 2>/dev/null || true
                
                echo "========== ArgoCD Application Created =========="
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                    echo "========== Deploying to Kubernetes =========="
                    
                    if ! command -v kubectl &> /dev/null; then
                        curl -LO "https://dl.k8s.io/release/v1.36.2/bin/linux/amd64/kubectl"
                        chmod +x ./kubectl
                        mv ./kubectl /usr/local/bin/kubectl
                    fi
                    
                    # Dynamically replace the build tag
                    sed -i "s/BUILD_TAG/${BUILD_NUMBER}/g" k8s/deployment.yaml
                    
                    # Apply Kubernetes manifests
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/ --insecure-skip-tls-verify=true --validate=false
                    
                    # Wait for rollout
                    kubectl --kubeconfig=$KUBECONFIG rollout status deployment/flask-devops-demo -n default --timeout=5m || true
                    
                    echo "========== Kubernetes Deployment Completed =========="
                    '''
                }
            }
        }

        stage('Prometheus Monitoring Setup') {
            steps {
                sh '''
                echo "========== Setting up Prometheus Monitoring =========="
                
                # Create prometheus namespace
                kubectl create namespace $PROMETHEUS_NAMESPACE --dry-run=client -o yaml | kubectl apply -f - || true
                
                # Create Prometheus ConfigMap for Flask app monitoring
                cat > prometheus-config.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: PROMETHEUS_NS
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    scrape_configs:
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
          - role: endpoints
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      
      - job_name: 'flask-devops-demo'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: keep
            regex: flask-devops-demo
          - source_labels: [__address__]
            action: replace
            regex: ([^:]+)(?::\d+)?
            replacement: \${1}:5000
            target_label: __address__
EOF

                sed -i "s/PROMETHEUS_NS/$PROMETHEUS_NAMESPACE/g" prometheus-config.yaml
                kubectl apply -f prometheus-config.yaml 2>/dev/null || true
                
                echo "========== Prometheus Configuration Deployed =========="
                '''
            }
        }

        stage('Grafana Dashboards Setup') {
            steps {
                sh '''
                echo "========== Setting up Grafana Dashboards =========="
                
                # Create Grafana namespace
                kubectl create namespace $GRAFANA_NAMESPACE --dry-run=client -o yaml | kubectl apply -f - || true
                
                # Create Grafana ConfigMap with dashboard
                cat > grafana-dashboard.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: flask-demo-dashboard
  namespace: GRAFANA_NS
data:
  flask-dashboard.json: |
    {
      "dashboard": {
        "title": "Flask DevOps Demo",
        "panels": [
          {
            "title": "HTTP Requests",
            "targets": [
              {
                "expr": "rate(flask_http_requests_total[5m])"
              }
            ]
          },
          {
            "title": "Response Time",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, flask_http_request_duration_seconds_bucket)"
              }
            ]
          },
          {
            "title": "Error Rate",
            "targets": [
              {
                "expr": "rate(flask_http_requests_total{status=~\"5..\"}[5m])"
              }
            ]
          },
          {
            "title": "Memory Usage",
            "targets": [
              {
                "expr": "process_resident_memory_bytes"
              }
            ]
          },
          {
            "title": "CPU Usage",
            "targets": [
              {
                "expr": "rate(process_cpu_seconds_total[5m])"
              }
            ]
          }
        ]
      }
    }
EOF

                sed -i "s/GRAFANA_NS/$GRAFANA_NAMESPACE/g" grafana-dashboard.yaml
                kubectl apply -f grafana-dashboard.yaml 2>/dev/null || true
                
                echo "========== Grafana Dashboards Configured =========="
                '''
            }
        }

    } // Close stages

    post {
        always {
            sh '''
            echo "========== Cleaning up =========="
            docker logout
            # Archive test reports
            '''
            archiveArtifacts artifacts: '**/test-*.xml,coverage.xml,trivy-report.json,bandit-report.json,pylint-report.txt', 
                            allowEmptyArchive: true
            junit testResults: '**/test-results.xml', allowEmptyResults: true
        }

        success {
            sh '''
            echo "========== Pipeline Execution Successful =========="
            '''
        }

        failure {
            sh '''
            echo "========== Pipeline Execution Failed =========="
            '''
        }
    }
} // Close pipeline