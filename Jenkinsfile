pipeline {

    agent any

    environment {
        IMAGE = "skbablualam03031997/flask-devops-demo:${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/skbablualam/flask-devops-demo.git'
            }
        }

        stage('Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                whoami
                id
                docker ps
                docker build -t $IMAGE .
                '''
            }
        }
        
        stage('Debug') {
             steps {
                sh '''
                whoami
                id
                ls -l /var/run/docker.sock
                docker ps || true
                '''
            }
        }

        stage('Push Docker') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE
                    '''
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                    # Download and setup kubectl if not cached
                    if ! command -v kubectl &> /dev/null; then
                        curl -LO "https://dl.k8s.io/release/v1.36.2/bin/linux/amd64/kubectl"
                        chmod +x ./kubectl
                        mv ./kubectl /usr/local/bin/kubectl
                    fi
            
                    # Force kubectl to bypass certificate constraints dynamically
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/ --insecure-skip-tls-verify=true --validate=false
                    '''
                }
            }
        }
    } // <-- Added missing brace to close 'stages'

    post {
        always {
            sh 'docker logout'
        }
    }
} // <-- Added missing brace to close 'pipeline'