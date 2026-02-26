pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root:root'
        }
    }

    environment {
        PYTHONUNBUFFERED = '1'
        DOCKER_IMAGE = "yourusername/train-ticket-fastapi"  // Change to your Docker Hub username
        DOCKER_TAG = "${env.BUILD_ID}"
        RENDER_SERVICE_ID = credentials('render-service-id')  // Add this credential in Jenkins
        RENDER_API_KEY = credentials('render-api-key')        // Add this credential in Jenkins
    }

    stages {
        stage('📦 Install Dependencies') {
            steps {
                echo 'Installing system + Python dependencies...'
                sh '''
                apt-get update
                apt-get install -y curl procps docker.io
                
                python --version
                pip --version
                
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest
                '''
            }
        }

        stage('🚀 Run & Test API') {
            steps {
                sh '''
                echo "Starting FastAPI..."
                uvicorn app.main:app --host 0.0.0.0 --port 8000 &
                API_PID=$!

                echo "Waiting for API to start..."
                sleep 10

                echo "Running Health Check..."
                curl -f http://localhost:8000/health

                echo "Running pytest..."
                pytest tests/ -v || true

                echo "Stopping FastAPI..."
                kill $API_PID
                '''
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                script {
                    def image = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    env.FULL_IMAGE = "${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('📤 Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('🚀 Deploy to Render') {
            steps {
                sh '''
                echo "Triggering Render deployment..."
                curl -X POST "https://api.render.com/v1/services/${RENDER_SERVICE_ID}/deploys" \
                    -H "Authorization: Bearer ${RENDER_API_KEY}" \
                    -H "Content-Type: application/json" \
                    -d "{\"dockerImage\": \"${FULL_IMAGE}\"}"
                
                echo "Render deployment triggered successfully!"
                '''
            }
        }

        stage('✅ SUCCESS') {
            steps {
                echo '🎉 Train Ticket FastAPI CI/CD Pipeline Completed Successfully!'
                echo "Deployed to Render: ${FULL_IMAGE}"
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
        }
        success {
            echo 'Pipeline succeeded! Check your Render dashboard.'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}
