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
        stage('🚀 Start Train API') {
            steps {
                echo 'Starting FastAPI application...'
                sh '''
                cd app

                nohup uvicorn main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
                echo $! > uvicorn.pid

                sleep 8
                '''
            }
        }

        stage('🧪 Health Check') {
            steps {
                echo 'Checking API health endpoint...'
                sh '''
                curl -f http://localhost:8000/health || curl -f http://127.0.0.1:8000/health
                echo "✅ Health check PASSED!"
                '''
            }
        }

        stage('📁 Debug Logs') {
            steps {
                sh '''
                echo "==== API LOG ===="
                cat app/api.log || true
                '''
            }
        }

        stage('✅ SUCCESS') {
            steps {
                echo '🎉 Train Ticket API CI/CD PIPELINE COMPLETED SUCCESSFULLY!'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up background processes...'
            sh '''
            if [ -f app/uvicorn.pid ]; then
                kill $(cat app/uvicorn.pid) || true
            fi
            pkill -f uvicorn || true
            '''
            echo 'Cleanup completed'
        }
    }
}
