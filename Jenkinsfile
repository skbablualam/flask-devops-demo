pipeline {

    agent any

    environment {
        IMAGE = "skbablualam03031997/flask-devops-demo:${BUILD_NUMBER}"
    }

    stages {

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

        // Uncomment later after kubectl is configured
        /*
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
        */
    }
}