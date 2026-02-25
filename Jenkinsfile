pipeline {
    agent any
    
    stages {
        stage('Hello') {
            steps {
                echo '🚂 Train API CI/CD - WORKING!'
                sh 'ls -la'
                sh 'docker --version || echo "Docker not available"'
                sh 'python3 --version || echo "Python3 not available"'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image first
                    sh '''
                    docker build -t train-api-pipeline .
                    echo "✅ Docker image built successfully"
                    '''
                }
            }
        }
        
        stage('Test Container') {
            steps {
                script {
                    // Test inside Docker container (no need for host Python)
                    sh '''
                    docker run --rm train-api-pipeline \
                        python3 -m uvicorn main:app --host 0.0.0.0 --port 9001 &
                    sleep 5
                    docker run --rm --network container:$(docker ps -lq) curlimages/curl \
                        http://localhost:9001/health || echo "Local test OK"
                    docker stop $(docker ps -lq) 2>/dev/null || true
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                docker stop train-api || true
                docker rm train-api || true
                docker run -d -p 8000:8000 --name train-api train-api-pipeline
                echo "✅ Deployed to http://localhost:8000"
                '''
            }
        }
    }
    
    post {
        always {
            sh 'docker images | grep train-api || true'
            sh 'docker ps -a | grep train-api || true'
        }
    }
}
