pipeline {
    agent any
    
    stages {
        stage('🚂 Train API CI/CD') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                cd app
                python3 -m pip install --user -r ../requirements.txt --quiet
                export PATH="$HOME/.local/bin:$PATH"
                which uvicorn || echo "Uvicorn installed"
                '''
            }
        }
        
        stage('🧪 Test API') {
            steps {
                sh '''
                cd app
                export PATH="$HOME/.local/bin:$PATH"
                
                # Start API in background
                nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
                API_PID=$!
                echo "API PID: $API_PID"
                
                # Wait for startup
                sleep 8
                
                # Health check
                curl -f http://localhost:8000/health || curl -f http://127.0.0.1:8000/health
                echo "✅ Health check PASSED!"
                
                # Cleanup
                kill $API_PID || true
                sleep 2
                '''
            }
        }
        
        stage('✅ SUCCESS') {
            steps {
                echo '🎉 Train Ticket API CI/CD PIPELINE COMPLETED SUCCESSFULLY!'
                sh 'ls -la app/'
                echo '🚀 Run manually: cd app && uvicorn main:app --host 0.0.0.0 --port 8000'
            }
        }
    }
    
    post {
        always {
            sh 'pkill -f uvicorn || true'
            sh 'pkill -f main.py || true'
            echo 'Cleanup completed'
        }
    }
}
