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
                // This binds your uploaded secret file to a temporary file path variable ($KUBECONFIG)
                withCredentials([file(credentialsId: 'MINIKUBE_KUBECONFIG', variable: 'KUBECONFIG')]) {
                    sh '''
                    # If kubectl isn't persisted across builds, keep these 3 lines:
                    curl -LO "https://dl.k8s.io/release/v1.36.2/bin/linux/amd64/kubectl"
                    chmod +x ./kubectl
                    mv ./kubectl /usr/local/bin/kubectl
            
                    # Explicitly tell kubectl to use the authenticated Jenkins secret file
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/
                    '''
                }
            }
        }
    post {
        always {
            sh 'docker logout'
        }
    }
}