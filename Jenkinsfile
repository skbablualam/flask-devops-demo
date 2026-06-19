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
                sh '''
                # Download the stable kubectl binary
                curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                # Make it executable and move it to a system path
                chmod +x ./kubectl
                mv ./kubectl /usr/local/bin/kubectl
                # Run your deployment
                kubectl apply -f k8s/
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