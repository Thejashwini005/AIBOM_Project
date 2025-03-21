pipeline {
    agent any

    environment {
        GIT_CREDENTIALS_ID = 'github-private-repo'
        REPO_URL = 'https://github.com/Thejashwini005/AIBOM_Project.git'
        MODEL_DIR = '/home/jenkins/models'  // Change this path if needed
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    sh "rm -rf ${MODEL_DIR}"
                    sh "git clone --depth=1 ${REPO_URL} ${MODEL_DIR}"
                    echo "✅ Repository cloned successfully."
                }
            }
        }

        stage('Validate Required Files') {
            steps {
                script {
                    def datasetExists = fileExists("${MODEL_DIR}/dataset.json")
                    def modelInfoExists = fileExists("${MODEL_DIR}/modelinfo.json")

                    if (!datasetExists || !modelInfoExists) {
                        error "❌ Required files missing. Stopping pipeline."
                    }
                    echo "✅ Model files found."
                }
            }
        }

        stage('Run AIBOM Script') {
            steps {
                script {
                    sh "python3 ${MODEL_DIR}/generate_aibom.py --model-path ${MODEL_DIR}"
                    echo "✅ AIBOM script executed."
                }
            }
        }

        stage('Check Reports') {
            steps {
                script {
                    def aibomExists = fileExists("${MODEL_DIR}/reports/aibom.json")
                    def sbomExists = fileExists("${MODEL_DIR}/reports/sbom.json")
                    def vulnExists = fileExists("${MODEL_DIR}/reports/vulnerability_report.json")

                    if (!aibomExists || !sbomExists || !vulnExists) {
                        error "❌ Required reports missing!"
                    }
                    echo "✅ Reports generated successfully."
                }
            }
        }

        stage('Check Vulnerabilities') {
            steps {
                script {
                    def vulnReport = readFile("${MODEL_DIR}/reports/vulnerability_report.json")
                    if (vulnReport.contains("high") || vulnReport.contains("critical")) {
                        echo "⚠️ WARNING: Model not ready for production! ⚠️"
                    } else {
                        echo "✅ No critical vulnerabilities found."
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Pipeline failed. Check logs for details."
        }
        success {
            echo "✅ Pipeline completed successfully."
        }
    }
}
