<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Added sections: Phase IV Deployment Principles, Allowed Tools Policy, Deployment Constraints
Removed sections: None
Modified principles: N/A (new constitution)
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending review
Runtime docs: README.md ⚠ pending review
Follow-up TODOs: None
-->

# Local Kubernetes Deployment Constitution

## Core Principles

### I. Phase IV Deployment Focus
Containerization and local Kubernetes deployment must be achieved using AI-assisted tools only; No manual coding changes to Phase III app logic unless absolutely required for deployment; Maintain integrity of original Hackathon-2 Todo Chatbot codebase.

### II. AI-Assisted Tool Chain
All containerization, image building, and deployment tasks must utilize AI-enabled tools: Docker AI Agent (Gordon) for Dockerfiles, kubectl-ai for Helm deployments, and Kagent for cluster optimization; Manual Dockerfile/Helm chart creation prohibited.

### III. Local-Only Deployment (NON-NEGOTIABLE)
Deployment restricted to local Minikube environment only; No cloud or production deployment allowed; All infrastructure remains within local development environment; Zero-touch cloud deployment capabilities deliberately excluded.

### IV. Containerization Requirements
Frontend (Next.js) and Backend (FastAPI) applications must be containerized separately; Docker images must preserve original application environment variables and port configurations from Phase III; All dependencies must be properly encapsulated in containers.

### V. Configuration Preservation
Environment variables, ports, and configuration settings from Phase III application must remain unchanged in deployment; Application logic and behavior must be identical post-deployment; No modifications to app-level business logic permitted.

### VI. AI Operations (AI-Ops) Integration
Kubernetes orchestration must include AI-assisted scaling, debugging, and resource optimization capabilities; Deployment must support intelligent monitoring and self-healing; AI-generated logs and operational insights must be preserved for analysis.

## Allowed Tools Policy

The following tools are authorized for Phase IV deployment activities:
- Docker Desktop (version 4.53 or higher) for containerization
- Docker AI Agent (Gordon) for automated Dockerfile generation and image building
- kubectl-ai for Helm chart generation, deployment, scaling, and debugging
- Kagent for cluster health analysis and optimization
- Minikube for local Kubernetes cluster management

No other tools or manual intervention methods are permitted for core deployment tasks.

## Deployment Constraints

- Phase III Hackathon-2 Todo Chatbot code must remain unchanged unless required for Phase IV deployment
- Deployment is strictly local-only using Minikube
- Frontend and backend must be containerized separately (Next.js and FastAPI respectively)
- All Docker images and Helm charts must be AI-generated with no manual editing
- No CI/CD pipeline or cloud deployment required
- Environment variables and ports must exactly match Phase III app specifications
- AI-generated logs and operational data must be preserved for audit and analysis

## Scope of Work

- Complete containerization of frontend and backend applications
- AI-generated Helm chart creation and deployment
- Kubernetes orchestration with proper service networking
- AI Operations: automated scaling, debugging, and resource optimization
- Local validation of frontend-backend communication
- Node.js runtime environment preservation
- Complete local development environment validation

## Governance

This constitution governs all Phase IV deployment activities and supersedes any conflicting practices or procedures. All deployment tasks must comply with AI-assisted tool requirements and local-only constraints. Any deviation from these principles requires formal amendment documentation and approval. All Dockerfiles, Helm charts, and deployment configurations must be generated through AI tools without manual intervention. Code changes are prohibited except where necessary for deployment compatibility only.

**Version**: 1.0.0 | **Ratified**: 2026-01-28 | **Last Amended**: 2026-01-28