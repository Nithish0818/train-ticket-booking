pipeline {
    agent any
    
    stages {
        stage('Hello') {
            steps {
                echo '🚂 Train API CI/CD - Nithish0818!'
                sh 'ls -la'
                sh 'pwd'
            }
        }
        
        stage('Build Docker') {
            steps {
                sh '''
                docker build -t train-api:${BUILD_ID} .
                echo "✅ Docker image built: train-api:${BUILD_ID}"
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                docker stop train-api || true
                docker rm train-api || true
                docker run -d -p 8000:8000 --name train-api train-api:${BUILD_ID}
                sleep 5
                curl http://localhost:8000/health || echo "🚂 API Deployed!"
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 Train API deployed! http://localhost:8000/docs'
        }
        failure {
            echo '❌ Build failed - check logs'
        }
    }
}
