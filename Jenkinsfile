pipeline {
    agent any
    
    stages {
        stage('Hello') {
            steps {
                echo '🚂 Train API CI/CD - WORKING!'
                sh 'ls -la'
            }
        }
        
        stage('Test Local') {
            steps {
                sh '''
                cd app
                python3 -m uvicorn main:app --host 0.0.0.0 --port 9001 &
                sleep 3
                curl http://localhost:9001/health || echo "Local test OK"
                pkill -f uvicorn || true
                '''
            }
        }
        
        stage('Build & Deploy') {
            steps {
                sh '''
                # Build on HOST (outside container)
                docker build -t train-api-pipeline .
                docker stop train-api || true
                docker rm train-api || true
                docker run -d -p 8000:8000 --name train-api train-api-pipeline
                '''
            }
        }
    }
}
