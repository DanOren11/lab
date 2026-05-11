pipeline {
    agent { label "Application-Agent" }
    environment {
        GH_TOKEN = credentials("GH_TOKEN")
        DOCKER_PAT = credentials('DOCKER_PAT')
    }

    stages {
        stage('Docker login') {
            when { changeRequest target: 'main' }
            steps {
                sh 'echo "${DOCKER_PAT_PSW}" | docker login --username "${DOCKER_PAT_USR}" --password-stdin'
            }
        }

        stage('Get develop last commit SHA & Pull image') {
            when { changeRequest target: 'main' }
            steps {
                script {
                    def commitSha = sh(
                        script: 'git rev-parse --short=7 HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Commit SHA: ${commitSha}"
                    sh "docker pull danpowercom/mini-project-2-private-repo:${commitSha}"
                    env.IMAGE_SHA = commitSha
                }
            }
        }

        stage('Stop and delete existing container') {
            when { changeRequest target: 'main' }
            steps {
                sh '''
                    docker stop app-container || true
                    docker rm app-container || true
                '''
            }
        }

        stage('Run the new container') {
            when { changeRequest target: 'main' }
            steps {
                sh "docker run -d --name app-container -p 3000:3000 danpowercom/mini-project-2-private-repo:${env.IMAGE_SHA}"
            }
        }

        stage('Docker logout') {
            when { changeRequest target: 'main' }
            steps {
                sh 'docker logout'
            }
        }
        stage('Merging the changes to main branch') {
            when { changeRequest target: 'main' }
            steps {
                sh """
                    gh pr merge ${env.CHANGE_ID} \
                        --merge \
                        --repo DanOren11/Mini_Project_GitHub_Webhooks_Jenkins_Jira
                """
            }
        }
    }
    post {
        success {
            script {
                // This only triggers the Jira pipeline when the CD pipeline actually ran
                if (env.CHANGE_TARGET == 'main'){
                    build job: 'Jira-Pipeline', wait: false
                }
            }   
        }
    }
}
