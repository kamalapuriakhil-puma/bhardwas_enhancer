// Jenkinsfile (for Bhardwas Enhancer)

pipeline {
    // Use a standard Python Docker image for a consistent environment
    agent {
        docker {
            image 'python:3.9-slim'
        }
    }

    // Environment variables
    environment {
        // Set the path for Python virtual environment
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        // 1. Checkout Stage
        stage('Checkout Code') {
            steps {
                // Retrieves the source code from your version control (e.g., Git)
                git branch: 'main', url: 'https://github.com/kamalapuriakhil-puma/bhardwas_enhancer.git' // <-- REPLACE THIS
            }
        }

        // 2. Build and Test Stage
        stage('Build and Test') {
            steps {
                script {
                    // Create a virtual environment
                    sh "python -m venv ${VENV_PATH}"
                    
                    // Activate venv and install dependencies
                    sh """
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python -m unittest discover

                    """

                    // Since you don't have tests, we'll run a static check 
                    // or a simple command to confirm installation
                    echo "Checking installed packages..."
                    sh "${VENV_PATH}/bin/pip freeze"
                    
                    echo "Build complete. Artifacts (dependencies) are ready."
                    
                    // Note: In a real-world app, unit tests would run here:
                    // sh "${VENV_PATH}/bin/pytest"
                }
            }
        }

        // 3. Deployment Stage (Manual Approval for Production)
        // This stage assumes you have a separate EC2/Linux machine for deployment
        stage('Deploy to EC2') {
            // A common practice is to use a dedicated agent/node that has SSH access configured
            agent any // <-- REPLACE THIS WITH A JENKINS NODE LABEL

            steps {
                echo 'Starting deployment to EC2 instance...'
                
                // --- SSH Deployment Script ---
                // NOTE: This assumes you have configured the Jenkins user with SSH access
                // to the EC2 instance (using SSH keys).
                
                // 1. Copy the entire project folder to the EC2 instance
                //    (Replace user@ip:/path/ with your actual details)
                sshagent(['2c007a4a-d4b8-4a93-bce4-ed7a39be03d7']) { // Assumes a pre-configured SSH key in Jenkins credentials
                    sh """
                    scp -r * user@3.110.155.238:/home/user/bhardwas_app/
                    
                    # 2. Connect via SSH and run deployment commands (install dependencies, start service)
                    ssh user@3.110.155.238 << EOF
                        cd /home/user/bhardwas_app
                        
                        # Use system-wide python/pip or set up venv on the server
                        pip3 install -r requirements.txt
                        
                        # Stop existing process (if running) and start the app using screen/tmux or systemd
                        echo "Restarting application..."
                        # Example: Use a 'screen' session to keep it running
                        screen -S bhardwas -X quit || true
                        screen -dmS bhardwas python3 app.py
                    EOF
                    """
                }
                echo 'Deployment successful! Check http://3.110.155.238:5000'
            }
        }
    }
}
