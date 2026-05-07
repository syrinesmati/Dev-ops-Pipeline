pipeline {

    agent any

    environment {
        SONAR_TOKEN_CRED = 'sonarqube-token'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 20, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                echo '── STAGE 1 — Checkout ──'
                checkout scm
                sh '''
                    echo "Branch  : $(git rev-parse --abbrev-ref HEAD)"
                    echo "Commit  : $(git rev-parse HEAD)"
                    echo "Message : $(git log -1 --format='%s')"
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '── STAGE 2 — Install ──'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip --quiet
                    pip install -r requirements.txt --quiet
                    pip list
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo '── STAGE 3 — Unit Tests ──'
                sh '''
                    . .venv/bin/activate
                    pytest tests/ \
                        --cov=app \
                        --cov-report=xml:coverage.xml \
                        --cov-report=term-missing \
                        --junit-xml=test-results.xml \
                        -v
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Static Analysis (SonarQube)') {
            steps {
                echo '── STAGE 4 — SonarQube ──'
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: "${SONAR_TOKEN_CRED}", variable: 'SONAR_TOKEN')]) {
                        sh '''
                            . .venv/bin/activate
                            sonar-scanner \
                                -Dsonar.login=${SONAR_TOKEN} \
                                -Dsonar.projectVersion=${BUILD_NUMBER}
                        '''
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo '── STAGE 5 — Quality Gate ──'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success { echo '✅ Pipeline CI — Quality Gate PASSED' }
        failure { echo '❌ Pipeline CI — FAILED' }
        always  { sh 'rm -rf .venv || true' }
    }
}