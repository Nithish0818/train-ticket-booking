pipeline {

    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root:root'
        }
    }

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {

        stage('📦 Install Dependencies') {
            steps {
                echo 'Installing system + Python dependencies...'
                sh '''
                apt-get update
                apt-get install -y curl procps

                python --version
                pip --version

                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('🚀 Run & Test API') {
            steps {
                echo 'Starting FastAPI and running health check...'
                sh '''
                cd app

                echo "Starting FastAPI..."
                uvicorn main:app --host 0.0.0.0 --port 8000 &
                API_PID=$!

                echo "Waiting for API to start..."
                sleep 10

                echo "Running Health Check..."
                curl -f http://localhost:8000/health

                echo "Stopping FastAPI..."
                kill $API_PID
                '''
            }
        }

        stage('✅ SUCCESS') {
            steps {
                echo 'Train Ticket FastAPI CI Pipeline Completed Successfully!'
            }
        }
    }
}
