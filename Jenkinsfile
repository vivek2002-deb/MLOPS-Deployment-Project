pipeline{
    agent any

    stages{
        stages{'Cloning Github repo to Jenskins'}{
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins.........'
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/vivek2002-deb/MLOPS-Deployment-Project.git']])
            }
        }
    }
}