# CI/CD Final Project

**Student:** Kristiann Koome
**Course:** IBM DevOps and Software Engineering Professional Certificate
**Project:** Building a CI/CD Pipeline with GitHub Actions, Tekton, and OpenShift

---

## Overview

This project demonstrates a complete end-to-end CI/CD pipeline using:

- **GitHub Actions** — for continuous integration (linting & unit testing)
- **Tekton** — for pipeline task management on OpenShift
- **OpenShift** — for container orchestration and deployment

---

## Application

A simple Python/Flask counter service that exposes a REST API for managing hit counters.

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check — returns service status |
| `/counters/{name}` | POST | Create a new counter |
| `/counters/{name}` | GET | Read the current counter value |
| `/counters/{name}` | PUT | Increment a counter |
| `/counters/{name}` | DELETE | Delete a counter |

---

## Repository Structure

```
├── .github/
│   └── workflows/
│       └── workflow.yml       # GitHub Actions CI pipeline
├── .tekton/
│   ├── tasks.yml              # Tekton custom tasks (cleanup, nose)
│   ├── pipeline.yml           # Tekton pipeline definition
│   └── pipelinerun.yml        # Tekton pipeline run manifest
├── app/
│   ├── __init__.py
│   └── counter.py             # Flask counter application
├── tests/
│   ├── __init__.py
│   └── test_counter.py        # Unit tests (nosetests)
├── requirements.txt
├── setup.cfg
└── README.md
```

---

## CI Pipeline (GitHub Actions)

The GitHub Actions workflow runs automatically on every `push` and `pull_request`:

1. ✅ **Checkout code**
2. ✅ **Set up Python 3.9**
3. ✅ **Install dependencies**
4. ✅ **Lint with flake8**
5. ✅ **Run unit tests with nose**

---

## CD Pipeline (Tekton / OpenShift)

The Tekton pipeline runs on OpenShift and includes:

1. **cleanup** — Clears the shared workspace before each run
2. **git-clone** — Clones the repository from GitHub
3. **nose** — Runs unit tests with coverage reporting
4. **buildah** — Builds the container image
5. **deploy** — Deploys the application to OpenShift

---

## Getting Started

### Prerequisites

- Python 3.9+
- OpenShift CLI (`oc`)
- Tekton CLI (`tkn`)
- Access to an OpenShift 4.x cluster

### Local Development

```bash
# Clone the repository
git clone https://github.com/<your-username>/CI-CD-pipeline-.git
cd CI-CD-pipeline-

# Install dependencies
pip install -r requirements.txt

# Run the app locally
flask run

# Run linting
flake8 . --count --max-line-length=127 --statistics

# Run tests
nosetests -v --with-spec --spec-color --with-coverage --cover-package=app
```

### Deploy to OpenShift

```bash
# Login to your cluster
oc login --token=<token> --server=<server-url>

# Apply Tekton resources
oc apply -f .tekton/tasks.yml
oc apply -f .tekton/pipeline.yml

# Create the PVC (if not already created)
oc apply -f .tekton/pipelinerun.yml
```

---

## License

This project is part of the IBM DevOps and Software Engineering Professional Certificate on Coursera.