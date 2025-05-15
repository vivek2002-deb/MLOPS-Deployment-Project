pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
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
    }
}
