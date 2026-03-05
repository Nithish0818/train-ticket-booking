pipeline {
    // Jenkins can run this pipeline on any available agent/node
    agent any

    environment {
        // Docker image name stored in DockerHub
        DOCKER_IMAGE = "nithiish08/train-ticket"

        // Your deployed Render service URL
        APP_URL = "https://train-ticket-api-5s89.onrender.com"
		
    }

    stages {

        /*
        ======================================================
        STAGE 1 — CI: Run Unit Tests using pytest
        ======================================================

        Runs your test files inside a clean Python container.
        This ensures tests run in a predictable environment.
        */

        stage('CI - Run Pytest Tests') {
            agent {
                docker {
                    image 'python:3.10-slim'
                    args '-u root:root'
                }
            }

            steps {
                sh '''
                echo "Installing dependencies..."

                apt-get update
                apt-get install -y build-essential libffi-dev libssl-dev python3-dev

                pip install --upgrade pip
                pip install wheel setuptools

                pip install -r requirements.txt

                echo "Running pytest..."

                pytest test/ \
                    --junitxml=test-results.xml \
                    --verbose \
                    -s
                '''
            }

            post {
                always {
                    // Publish test results to Jenkins UI
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                }
            }
        }

        /*
        ======================================================
        STAGE 2 — Build Docker Image
        ======================================================

        After tests pass, build the application container.
        This image becomes the deployable artifact.
        */

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        /*
        ======================================================
        STAGE 3 — Push Docker Image to DockerHub
        ======================================================

        Store the built image in DockerHub so it can be
        pulled by deployment platforms like Render.
        */

        stage('Push Image to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {

                        def app = docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}")

                        // push versioned image
                        app.push()

                        // push "latest" tag
                        app.push("latest")
                    }
                }
            }
        }

        /*
        ======================================================
        STAGE 4 — Deploy to Render
        ======================================================

        Trigger a deployment through Render API.
        This tells Render to pull the new Docker image
        from DockerHub and redeploy the service.
        */

        stage('Deploy to Render') {
            steps {

                withCredentials([string(credentialsId: 'render-api-key', variable: 'RENDER_API_KEY')]) {

                    sh '''
                    echo "Triggering deployment on Render..."

                    curl -X POST \
                    -H "Authorization: Bearer $RENDER_API_KEY" \
                    -H "Content-Type: application/json" \
                    https://api.render.com/v1/services/srv-d6iok4vkijhs7389ou6g/deploys
                    '''
                }
            }
        }

        /*
        ======================================================
        STAGE 5 — Wait for Service Startup
        ======================================================

        Render takes time to pull image and restart container.
        We wait before testing the endpoints.
        */

        stage('Wait for Deployment') {
            steps {
                sh '''
                echo "Waiting for service to start..."
                until curl -f $APP_URL; do
				echo "Waiting for service..."
				sleep 5
				done
                '''
            }
        }

        /*
        ======================================================
        STAGE 6 — Smoke Tests (Post Deployment)
        ======================================================

        Verify the deployed system is reachable and alive.

        These tests confirm:
        - Application started
        - Routing works
        - Old functionality still responds
        */

        stage('Smoke Test - Verify Deployment') {
            steps {

                sh '''
				echo "Testing service at: $APP_URL"
                echo "Running smoke tests against deployed service..."

                echo "Checking root endpoint..."
                curl -f $APP_URL/

                echo "Checking API documentation..."
                curl -f $APP_URL/docs

                echo "Checking health endpoint..."
                curl -f $APP_URL/health

                echo "Smoke tests completed successfully"
                '''
            }
        }

    }

    /*
    ======================================================
    POST PIPELINE ACTIONS
    ======================================================
    */

    post {

        always {
            // Clean unused Docker images to prevent disk overflow
            sh 'docker system prune -f'
        }

        success {
            echo "CI/CD pipeline completed successfully."
            echo "Docker Image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
        }

        failure {
            echo "Pipeline failed. Check logs for errors."
        }
    }
}
