pipeline {
    agent any
    environment{ 
        JIRA_BASE_URL = "https://powercom-team-trdn5d9i.atlassian.net"
        JIRA_CREDS = credentials('Jira-Jenkins-Integration')
    }

    stages {
        stage('Get Ticket ID From Commit') {
            steps {
                script {
                    def commitMessage = sh(
                        script: "git log -1 --pretty=%B",
                        returnStdout: true
                    ).trim()
                    echo "Commit message: ${commitMessage}"

                    def matcher = commitMessage =~ /([A-Z]+-\d+)/
                    if (!matcher) {
                        error "No Jira ticket ID found in commit message"
                    }
                    env.TICKET_ID = matcher[0][1]
                    echo "Ticket ID: ${env.TICKET_ID}"
                }
            }
        }
    // Refer to https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/#api-rest-api-3-issue-issueidorkey-comment-post
        stage('Add Comment To Ticket') {
            steps {
                script {
                    sh """
                        curl -s -u "${JIRA_CREDS_USR}:${JIRA_CREDS_PSW}" \
                        -X POST \
                        -H "Content-Type: application/json" \
                        --data '{"body": {"type": "doc","version": 1, \
                        "content": [{"type": "paragraph","content": [{"type": "text", \
                        "text": "Deployed successfully - build #${BUILD_NUMBER}"}]}]}}' \
                        ${JIRA_BASE_URL}/rest/api/3/issue/${TICKET_ID}/comment
                    """
                }
            }
        }
        stage('Get Done transition & Close jira ticket'){
            //For get the id to move the task to Done {It can change any task}
            steps {
                script {
                   def response = sh (
                        script: """
                            curl -u "${JIRA_CREDS_USR}:${JIRA_CREDS_PSW}" \
                            -X GET \
                            -H "Accept: application/json" \
                            "${JIRA_BASE_URL}/rest/api/3/issue/${TICKET_ID}/transitions"
                        """,
                        returnStdout: true
                    ).trim()
                    def json = readJSON text: response
                   
                    def doneTransition = json.transitions.find { it.name == "Done" }
                    if (!doneTransition) { // Prevent crushing
                       error "No 'Done' transition available for this issue"
                    }
                    echo "Found Done transition ID: ${doneTransition.id}"
            
                    sh """
                        curl -u "${JIRA_CREDS_USR}:${JIRA_CREDS_PSW}" \
                        -X POST \
                        -H "Content-Type: application/json" \
                        ${JIRA_BASE_URL}/rest/api/3/issue/${TICKET_ID}/transitions \
                        -d '{
                            "transition": {
                                "id": "${doneTransition.id}"
                            }
                        }'
                    """
                }
            }
        }
        
    }
}
