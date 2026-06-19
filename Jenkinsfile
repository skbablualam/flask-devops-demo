pipeline {

    agent any

    environment {
    IMAGE = "skbablualam03031997/flask-devops-demo:${BUILD_NUMBER}"
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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
        ])      {
            sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push $IMAGE
            '''
            }
        }
    } 
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/'
        }
    }
}