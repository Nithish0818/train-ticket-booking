pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nithiish08/train-ticket"
    }

    stages {

        stage('CI - Test in Python Container') {
            agent {
                docker {
                    image 'python:3.10-slim'
                    args '-u root:root'
                }
            }

            steps {
                sh '''
                apt-get update
                apt-get install -y curl procps
                pip install --upgrade pip
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('CD - Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('CD - Push Image to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def app = docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                        app.push()
                        app.push("latest")
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
        }
        success {
            echo "Docker Image pushed successfully: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline Failed!"
        }
    }
}
