# Mini Project – GitHub Webhooks + Jenkins + Jira

A complete CI/CD pipeline system that automates building, deploying, and tracking Docker-based applications using GitHub webhooks, Jenkins, DockerHub, and Jira.

---

## Architecture

| Server | Role |
|---|---|
| Jenkins Master | Manages all pipelines and automation |
| Jenkins Slave 1 (Infrastructure) | Runs CI pipeline – builds and pushes Docker images |
| Jenkins Slave 2 (Application) | Runs CD pipeline – deploys the application container |
| Jira Cloud | Issue tracking and ticket automation |

---

## Folder Structure

```
Mini_Project_GitHub_Webhooks_Jenkins_Jira/
├── jenkins/
│   ├── docker-compose.yml
│   └── jenkins-slave/
│       └── Dockerfile
├── pipelines/
│   ├── ci.Jenkinsfile
│   ├── cd.Jenkinsfile
│   └── track.Jenkinsfile
├── app/
│   ├── Dockerfile
│   └── src/
└── README.md
```

---

## How to Run

### Requirements
- Docker + Docker Compose
- Jenkins credentials configured (see below)

### Start Jenkins

```bash
cd jenkins
docker compose up -d
```

Jenkins will be available at `http://localhost:8080`

### Credentials needed in Jenkins

| ID | Type | Used for |
|---|---|---|
| `GH_PAT` | Username/Password | Git checkout from GitHub |
| `GH_TOKEN` | Secret Text | GitHub CLI (gh pr create) |
| `DOCKER_PAT` | Username/Password | DockerHub login |
| `Jira-Jenkins-Integration` | Username/Password | Jira REST API |

---

## Pipelines

### CI Pipeline (`ci.Jenkinsfile`)
- **Trigger:** Push to `develop` branch
- **Agent:** Infrastructure Slave
- **Flow:**
  1. Docker login
  2. Build image tagged with commit SHA
  3. Push to private DockerHub registry
  4. Docker logout
  5. Automatically create PR from `develop` to `main`

### CD Pipeline (`cd.Jenkinsfile`)
- **Trigger:** Pull Request targeting `main`
- **Agent:** Application Slave
- **Flow:**
  1. Docker login
  2. Pull image by commit SHA
  3. Stop and remove existing container
  4. Run new container on port 3000
  5. Docker logout
  6. Trigger Jira pipeline on success

### Jira Track Pipeline (`track.Jenkinsfile`)
- **Trigger:** After CD pipeline completes successfully
- **Agent:** Any (Jenkins Master)
- **Flow:**
  1. Extract Jira ticket ID from commit message (e.g. `KAN-1`)
  2. Add deployment comment to the ticket
  3. Move ticket to Done

---

## Commit Message Format

Commits must include a Jira ticket ID for the track pipeline to work:

```
KAN-1 your commit message here
```

---

## Branch Strategy

```
main     → Production (merges via PR only)
develop  → Development (all work done here)
```

---

## Docker Images

| Image | Visibility |
|---|---|
| `danpowercom/mini-project-jenkins-github-webhook:slave` | Public |
| `danpowercom/mini-project-2-private-repo` | Private |

---

## Tech Stack

- Jenkins
- Docker / Docker Compose
- GitHub + GitHub CLI
- DockerHub
- Jira Cloud (REST API v3)
- React + TypeScript + Vite
- Node.js 22
