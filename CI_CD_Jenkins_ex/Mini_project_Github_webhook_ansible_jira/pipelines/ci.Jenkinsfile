pipeline {
    agent {label "Infrastructure_Agent"}
    environment {
        GH_TOKEN = credentials("GH_TOKEN")
        DOCKER_PAT = credentials('DOCKER_PAT') 
        repoName = ("DanOren11/Mini_Project_GitHub_Webhooks_Jenkins_Jira")    
    }

    stages {
        stage('Docker login') {
            steps {
                sh ' echo "${DOCKER_PAT_PSW}" | docker login --username "${DOCKER_PAT_USR}" --password-stdin'
                
            }
        }
        stage('Get Commit Hash') {
            steps {
                echo "Commit hash: ${env.GIT_COMMIT}"
            }
        }
         stage('Build & Tag & Push image') {
            steps {
                script {
                    def shortSha = sh(
                        script: 'git rev-parse --short=7 HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Short SHA: ${shortSha}"
                    sh "docker build -t danpowercom/mini-project-2-private-repo:${shortSha} -f app/Dockerfile ./app"
                    sh "docker push danpowercom/mini-project-2-private-repo:${shortSha}"
                }
            }
        }
        stage ('docker logout'){
            steps {
                sh 'docker logout'
            }
        }
        stage('Create PR to main') {
            steps {
                script {
                    // we just nee the develop branch without origin/
                    def branchName = env.GIT_BRANCH?.replaceAll('^origin/', '')
                    echo "Branch: ${branchName}"

                    sh """
                        gh pr create \
                            --title "CI: merge ${branchName} into main" \
                            --body "Automated PR from CI pipeline" \
                            --base main \
                            --head ${branchName} \
                            --repo ${repoName}
                    """
                }
            }
        }
        
    }
}
