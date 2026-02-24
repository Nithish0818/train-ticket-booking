pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/YOUR_USERNAME/train-ticket-booking-api.git'
            }
        }
        
        stage('Build Docker') {
            steps {
                script {
                    // Build Docker image
                    def image = docker.build("train-api:${env.BUILD_ID}")
                    
                    // Push to DockerHub (optional)
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-id') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
        
        stage('Test API') {
            steps {
                sh '''
                docker run -d -p 8000:8000 --name test-api train-api:${BUILD_ID}
                sleep 10
                curl http://localhost:8000/health || echo "Health check failed"
                docker stop test-api
                docker rm test-api
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                docker stop train-api || true
                docker rm train-api || true
                docker run -d -p 8000:8000 --name train-api train-api:latest
                '''
            }
        }
    }
    
    post {
        success {
            echo '🚂 Train API deployed successfully! http://localhost:8000'
        }
        failure {
            echo '❌ Deployment failed!'
        }
    }
}
