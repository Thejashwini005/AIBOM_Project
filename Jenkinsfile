pipeline {
    agent any

    environment {
        GIT_CREDENTIALS_ID = 'gihub-credentials'
        MODEL_DIR = 'F:/HPE Project/Model'
        SCRIPT_REPO = 'https://github.com/Thejashwini005/AIBOM_Project.git'
        REPORT_DIR = "${MODEL_DIR}/reports"
    }

    parameters {
        string(name: 'MODEL_GIT_URL', defaultValue: '', description: 'Enter GitHub repo URL for the model (leave empty if using local path)')
        string(name: 'MODEL_LOCAL_PATH', defaultValue: '', description: 'Enter local model path (leave empty if using GitHub)')
    }

    stages {
        stage('Build') {
            steps {
                script {
                    sh "rm -rf ${MODEL_DIR}"
                    if (params.MODEL_GIT_URL) {
                        echo "📥 Cloning model from GitHub: ${params.MODEL_GIT_URL}"
                        sh "git clone ${params.MODEL_GIT_URL} ${MODEL_DIR}"
                    } else if (params.MODEL_LOCAL_PATH) {
                        echo "📂 Copying model from local path: ${params.MODEL_LOCAL_PATH}"
                        sh "cp -r ${params.MODEL_LOCAL_PATH} ${MODEL_DIR}"
                    } else {
                        error "❌ No model source provided!"
                    }
                    echo "✅ Build stage completed."
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "📥 Fetching AIBOM script..."
                    sh "git clone ${SCRIPT_REPO} ${MODEL_DIR}/script"
                    sh "cp ${MODEL_DIR}/script/generate_aibom.py ${MODEL_DIR}/"
                    echo "✅ Deploy stage completed."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "🛠️ Running AIBOM script..."
                    sh "python3 ${MODEL_DIR}/generate_aibom.py --model-path ${MODEL_DIR}"
                    
                    // Ensure report directory exists
                    sh "mkdir -p ${REPORT_DIR}"
                    
                    echo "✅ Test stage completed."
                }
            }
        }

        stage('Promote') {
            steps {
                script {
                    def aibomExists = fileExists("${REPORT_DIR}/aibom.json")
                    def sbomExists = fileExists("${REPORT_DIR}/sbom.json")
                    def vulnExists = fileExists("${REPORT_DIR}/vulnerability_report.json")

                    if (!aibomExists || !sbomExists || !vulnExists) {
                        error "❌ Reports missing! Cannot proceed."
                    }
                    
                    def vulnReport = readFile("${REPORT_DIR}/vulnerability_report.json")
                    if (vulnReport.contains("high") || vulnReport.contains("critical")) {
                        echo "⚠️ WARNING: Model has vulnerabilities! Not ready for production."
                    } else {
                        echo "✅ Model passes security checks."
                    }
                    echo "✅ Promote stage completed."
                }
            }
        }

        stage('Release') {
            steps {
                script {
                    echo "📢 CI/CD Pipeline completed successfully!"
                    echo "Generated Reports:"
                    sh "ls -lh ${REPORT_DIR}"
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Pipeline failed. Check logs for details."
        }
        success {
            echo "✅ Pipeline executed successfully."
        }
    }
}
