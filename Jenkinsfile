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
                
                apt-get install -y \\
                curl \\
                procps \\
                build-essential \\
                libffi-dev \\
                libssl-dev \\
                python3-dev \\
                cargo
                
                pip install --upgrade pip
                pip install wheel setuptools
                
                pip install -r requirements.txt
                pip install pytest  # 🔥 TEST DEPENDENCY
                
                # 🔥 RUN TESTS WITH JUNIT XML
                pytest test/ \\
                    --junitxml=test-results.xml \\
                    --verbose \\
                    -s
                
                # 🔥 VERIFY XML CREATED
                ls -la test-results.xml
                '''
            }
            
            // 🔥 FIXED SYNTAX - testResults NOT testResultsSpec
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                }
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

    stage('🚀 Deploy to Render') {
    steps {
        withCredentials([string(credentialsId: 'render-api-key', variable: 'RENDER_API_KEY')]) {
            sh '''
            curl -X POST \\
                -H "Authorization: Bearer ${RENDER_API_KEY}" \\
                -H "Content-Type: application/json" \\
                https://api.render.com/v1/services/YOUR-SERVICE-ID/deploys
            '''
        }
    }
}


    post {
        always {
            sh 'docker system prune -f'
        }
        success {
            echo "🚀 Docker Image pushed: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
        }
        failure {
            echo "❌ Pipeline Failed!"
        }
    }
}
