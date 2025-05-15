pipeline {
    agent any

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins.........'
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/master']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/vivek2002-deb/MLOPS-Deployment-Project.git',
                            credentialsId: 'github-token'
                        ]]
                    ])
                }
            }
        }
    }
}
