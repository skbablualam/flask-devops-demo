pipeline {

    agent any

    environment {
        IMAGE = "YOUR_DOCKERHUB_USER/flask-devops-demo:v1"
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
                apt update
                apt install python3.13-venv
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Push Docker') {
            steps {
                sh 'docker push $IMAGE'
            }
        }

        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}