pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "cogent-precinct-458914-g5"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins.........'
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/vivek2002-deb/MLOPS-Deployment-Project.git',
                            credentialsId: 'github-token'
                        ]]
                    ])
                }
            }
        }

        stage('Setting up virtual envionment and installing dependencies') {
            steps {
                script {
                    echo 'Setting up virtual envionment and installing dependencies.........'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and pushing docker image to GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script {
                        echo 'Building and pushing docker image to GCP.........'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/mlops-deployment-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/mlops-deployment-project:latest
                        '''
                    }
                }
            }
        }
    }
}
