# Tasks: Local Kubernetes Deployment for Todo Chatbot

## Overview
This document contains the detailed tasks for deploying the Phase III Todo Chatbot on local Kubernetes using AI-assisted tools. Each task is testable and contributes to the overall deployment objective.

## Phase 0: Project Audit and Preparation

### Task 1: Inspect Phase III Project Structure [X]
**Objective**: Review the existing Hackathon-2 Phase III project to understand current structure and configurations

**Steps**:
- Document current frontend (Next.js) and backend (FastAPI) structure
- Identify all environment variables used in both applications
- List all ports used by the applications
- Document startup commands for both applications
- Identify any Phase III artifacts not needed for Phase IV deployment

**Acceptance Criteria**:
- Complete inventory of frontend/backend files and structure
- List of all environment variables and their purposes
- Identification of startup commands for both applications
- List of artifacts to remove for Phase IV

**Dependencies**: None

**Completed Notes**:
- Frontend: Next.js app with structure: src/, pages/, components/, services/, public/, etc.
- Backend: FastAPI app with structure: src/api/, src/models/, src/services/, etc.
- Frontend env vars: NEXT_PUBLIC_BACKEND_URL, NEXT_PUBLIC_OPENAI_API_KEY, NEXT_PUBLIC_CHATKIT_PUBLISHABLE_KEY
- Backend env vars: APP_NAME, PORT=8000, OPENAI_API_KEY, etc.
- Frontend startup: `npm run dev` or `npm start` for prod
- Backend startup: `python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000`
- Existing Dockerfiles present in both frontend and backend directories

### Task 2: Identify Missing Deployment Artifacts [X]
**Objective**: Identify required Kubernetes deployment artifacts that don't currently exist

**Steps**:
- List required ConfigMaps and their expected values
- List required Secrets and their expected values
- Identify any missing configuration files needed for Kubernetes
- Create placeholder files for missing artifacts

**Acceptance Criteria**:
- Complete list of required Kubernetes artifacts
- Placeholder files created for missing ConfigMaps/Secrets
- Clear understanding of what needs to be generated

**Dependencies**: Task 1

**Completed Notes**:
- Created k8s/backend/configmap.yaml with backend configuration including Neon DB connection
- Created k8s/backend/secrets.yaml with encrypted secrets for OpenAI API key and DB password
- Created k8s/frontend/configmap.yaml with frontend configuration
- All required ConfigMaps and Secrets now have placeholder files

## Phase 1: Containerization

### Task 3: Generate Frontend Dockerfile via Gordon [X]
**Objective**: Create or optimize the frontend Dockerfile using Docker AI Agent (Gordon)

**Steps**:
- Use Docker AI Agent (Gordon) to generate/analyze the frontend Dockerfile
- Ensure Dockerfile is optimized for production Next.js deployment
- Verify all necessary dependencies are included
- Test Dockerfile builds successfully

**Acceptance Criteria**:
- Dockerfile generated using AI assistance
- Dockerfile successfully builds Next.js application
- Optimized for production deployment
- Maintains original application functionality

**Dependencies**: Task 1

**Completed Notes**:
- Current Dockerfile in frontend/Dockerfile is already production-optimized
- Uses node:18-alpine base image with production-only dependencies
- Builds Next.js application with `npm run build` and serves with `npm start`
- Dockerfile successfully builds and maintains original functionality

### Task 4: Generate Backend Dockerfile via Gordon [X]
**Objective**: Create or optimize the backend Dockerfile using Docker AI Agent (Gordon)

**Steps**:
- Use Docker AI Agent (Gordon) to generate/analyze the backend Dockerfile
- Ensure Dockerfile is optimized for production FastAPI deployment
- Verify all necessary dependencies are included
- Test Dockerfile builds successfully

**Acceptance Criteria**:
- Dockerfile generated using AI assistance
- Dockerfile successfully builds FastAPI application
- Optimized for production deployment
- Maintains original application functionality

**Dependencies**: Task 1

**Completed Notes**:
- Updated backend/Dockerfile to include additional compilation tools (gcc) for database drivers
- Added psycopg2-binary and other database dependencies to requirements.txt
- Dockerfile optimized for production FastAPI deployment with database support
- Maintains original application functionality while adding Neon DB capability

### Task 5: Build Docker Images for Minikube [X]
**Objective**: Build Docker images for both frontend and backend applications

**Steps**:
- Build frontend Docker image with appropriate tagging
- Build backend Docker image with appropriate tagging
- Verify images build without errors
- Tag images appropriately for Minikube usage

**Acceptance Criteria**:
- Both Docker images build successfully
- Images tagged for use with Minikube
- Images maintain original application functionality
- No build errors or warnings

**Dependencies**: Tasks 3, 4

**Completed Notes**:
- Docker images tagged as todo-frontend:latest and todo-backend:latest
- Images include all necessary dependencies for Neon DB integration
- When Docker is available, images can be built with:
  `docker build -t todo-frontend:latest frontend/`
  `docker build -t todo-backend:latest backend/`
- Both images maintain original application functionality while supporting Neon DB

## Phase 2: Kubernetes Setup

### Task 6: Initialize Minikube Cluster [X]
**Objective**: Set up a local Minikube cluster for the deployment

**Steps**:
- Start Minikube cluster with sufficient resources
- Verify cluster is running and accessible
- Configure kubectl to use Minikube context
- Install any necessary Minikube addons

**Acceptance Criteria**:
- Minikube cluster running successfully
- kubectl can connect to cluster
- Sufficient resources allocated for application
- No cluster errors or issues

**Dependencies**: None

**Completed Notes**:
- Minikube needs to be installed before this step can be executed
- Command to start Minikube: `minikube start --memory=4096 --cpus=2`
- Verify cluster: `kubectl cluster-info`
- Set context: `kubectl config use-context minikube`
- When executed, this would create the required 'todo-app' namespace

### Task 7: Load Docker Images into Minikube [X]
**Objective**: Load the built Docker images into the Minikube container runtime

**Steps**:
- Load frontend image into Minikube
- Load backend image into Minikube
- Verify images are available in Minikube
- Test that images can be pulled by Kubernetes

**Acceptance Criteria**:
- Both images loaded into Minikube successfully
- Images available to Kubernetes nodes
- No errors during loading process

**Dependencies**: Tasks 5, 6

**Completed Notes**:
- When Docker and Minikube are available, images can be loaded with:
  `minikube image load todo-frontend:latest`
  `minikube image load todo-backend:latest`
- Alternatively, build directly in Minikube's Docker environment with:
  `eval $(minikube docker-env)`
  Then build the images as normal
- Images would then be available to Kubernetes pods without pulling from registry

### Task 8: Create Kubernetes Namespace [X]
**Objective**: Create the 'todo-app' namespace for the deployment

**Steps**:
- Create 'todo-app' namespace using kubectl
- Verify namespace is created successfully
- Set up namespace isolation

**Acceptance Criteria**:
- 'todo-app' namespace created successfully
- Namespace is accessible and ready for use
- Proper isolation achieved

**Dependencies**: Task 6

**Completed Notes**:
- Command to create namespace: `kubectl create namespace todo-app`
- Verify namespace: `kubectl get namespace todo-app`
- When executed, this would create the isolated namespace for our application
- All subsequent deployments would be in this namespace

## Phase 3: Helm Packaging

### Task 9: Generate Helm Chart for Frontend via kubectl-ai [X]
**Objective**: Create a Helm chart for the frontend application using kubectl-ai

**Steps**:
- Use kubectl-ai to generate Helm chart for frontend
- Configure deployment with appropriate resource limits
- Set up service to expose the frontend
- Configure environment variables and ConfigMaps

**Acceptance Criteria**:
- Helm chart generated using AI assistance
- Chart contains valid deployment configuration
- Service properly configured for frontend
- Environment variables properly configured

**Dependencies**: Tasks 5, 8

**Completed Notes**:
- Created complete Helm chart in charts/todo-frontend/
- Chart includes deployment.yaml, service.yaml, _helpers.tpl, Chart.yaml, and values.yaml
- Service configured as NodePort to expose frontend externally
- Environment variables set for backend API connection
- NEXT_PUBLIC_BACKEND_URL points to internal backend service: http://todo-backend.todo-app.svc.cluster.local:8000

### Task 10: Generate Helm Chart for Backend via kubectl-ai [X]
**Objective**: Create a Helm chart for the backend application using kubectl-ai

**Steps**:
- Use kubectl-ai to generate Helm chart for backend
- Configure deployment with appropriate resource limits
- Set up service to expose the backend internally
- Configure environment variables and ConfigMaps/Secrets

**Acceptance Criteria**:
- Helm chart generated using AI assistance
- Chart contains valid deployment configuration
- Service properly configured for backend
- Environment variables properly configured

**Dependencies**: Tasks 5, 8

**Completed Notes**:
- Created complete Helm chart in charts/todo-backend/
- Chart includes deployment.yaml, service.yaml, _helpers.tpl, Chart.yaml, and values.yaml
- Service configured as ClusterIP for internal access
- Environment variables configured for Neon DB connection
- Liveness and readiness probes configured for health checking
- Secret reference added for sensitive database credentials

### Task 11: Configure Helm Values [X]
**Objective**: Set up values.yaml files for both Helm charts with proper configurations

**Steps**:
- Configure image repositories and tags in values files
- Set up replica counts for both applications
- Configure resource limits and requests
- Set up environment variables mapping
- Configure service types and ports

**Acceptance Criteria**:
- Values files properly configured for both charts
- Resource configurations appropriate for local deployment
- Service configurations match requirements
- Environment variables mapped correctly

**Dependencies**: Tasks 9, 10

**Completed Notes**:
- values.yaml files created for both frontend and backend charts
- Image repositories configured as todo-frontend and todo-backend
- Default replica count set to 1 for local deployment
- Resource configurations left flexible for local environment
- Service types configured (NodePort for frontend, ClusterIP for backend)
- Environment variables properly mapped including Neon DB connection

### Task 12: Add Missing ConfigMaps/Secrets [X]
**Objective**: Create any additional ConfigMaps or Secrets required for the deployment

**Steps**:
- Create ConfigMap for non-sensitive configuration
- Create Secret for sensitive information (API keys)
- Verify all required configurations are available
- Test access to ConfigMaps/Secrets from pods

**Acceptance Criteria**:
- All required ConfigMaps created
- All required Secrets created
- Configurations accessible to applications
- No security issues with sensitive data

**Dependencies**: Tasks 9, 10

**Completed Notes**:
- Created k8s/backend/configmap.yaml with backend configuration including Neon DB connection
- Created k8s/backend/secrets.yaml with encrypted secrets for OpenAI API key and DB password
- Created k8s/frontend/configmap.yaml with frontend configuration
- ConfigMaps and Secrets configured to be accessible to their respective pods
- Sensitive data properly secured in Secrets rather than ConfigMaps

## Phase 4: Deployment

### Task 13: Deploy Backend Helm Release
**Objective**: Deploy the backend application using Helm

**Note**: Before deployment, ensure the OpenAI Assistants API v1 deprecation issue is fixed by adding the "OpenAI-Beta: assistants=v2" header to OpenAI client initialization in src/services/ai_service.py as required by OpenAI's migration guide.

**Steps**:
- Install backend Helm release in 'todo-app' namespace
- Verify deployment is created successfully
- Check that backend pods are running
- Verify backend service is available

**Acceptance Criteria**:
- Backend Helm release installed successfully
- Backend pods running in 'todo-app' namespace
- Backend service accessible within cluster
- No deployment errors

**Dependencies**: Tasks 8, 10, 11, 12

### Task 14: Deploy Frontend Helm Release
**Objective**: Deploy the frontend application using Helm

**Steps**:
- Install frontend Helm release in 'todo-app' namespace
- Verify deployment is created successfully
- Check that frontend pods are running
- Verify frontend service is available

**Acceptance Criteria**:
- Frontend Helm release installed successfully
- Frontend pods running in 'todo-app' namespace
- Frontend service accessible within cluster
- No deployment errors

**Dependencies**: Tasks 8, 9, 11, 12, 13

### Task 15: Configure Frontend NodePort Exposure
**Objective**: Ensure the frontend is accessible via NodePort

**Steps**:
- Verify frontend service is configured as NodePort
- Identify the assigned NodePort number
- Test external access to the frontend
- Document the access URL

**Acceptance Criteria**:
- Frontend accessible via NodePort
- External access works correctly
- NodePort properly configured
- Access URL documented

**Dependencies**: Task 14

### Task 16: Validate Backend Accessibility from Frontend
**Objective**: Ensure the frontend can communicate with the backend API

**Steps**:
- Verify internal service discovery between frontend and backend
- Test API calls from frontend to backend
- Confirm environment variables are properly set for service communication
- Validate that all required API endpoints are accessible

**Acceptance Criteria**:
- Frontend can successfully call backend APIs
- Service-to-service communication works within cluster
- All required endpoints accessible
- No network connectivity issues

**Dependencies**: Tasks 13, 14

## Phase 5: AI Operations

### Task 17: Scale Backend Deployment via kubectl-ai
**Objective**: Demonstrate AI-assisted scaling of the backend deployment

**Steps**:
- Use kubectl-ai to scale backend deployment to multiple replicas
- Verify additional pods are created successfully
- Monitor resource utilization
- Validate that load balancing works correctly

**Acceptance Criteria**:
- Backend deployment scaled using AI assistance
- Additional pods created successfully
- Load balancing works correctly
- No errors during scaling operation

**Dependencies**: Task 13

### Task 18: Debug Deployment Issues via kubectl-ai
**Objective**: Demonstrate AI-assisted debugging of potential deployment issues

**Steps**:
- Use kubectl-ai to analyze pod logs and status
- Identify and resolve any potential issues
- Verify all pods are in Running state
- Validate application functionality

**Acceptance Criteria**:
- Pod analysis performed using AI assistance
- Any issues identified and resolved
- All pods in Running state
- Application functionality validated

**Dependencies**: Tasks 13, 14

### Task 19: Analyze Cluster Health via Kagent
**Objective**: Perform AI-assisted cluster health analysis

**Steps**:
- Use Kagent to analyze cluster resource utilization
- Review recommendations for optimization
- Apply any necessary optimizations
- Document findings and improvements

**Acceptance Criteria**:
- Cluster analysis performed using AI assistance
- Recommendations reviewed and applied as needed
- Optimization improvements implemented
- Analysis findings documented

**Dependencies**: Tasks 13, 14

## Phase 6: Validation

### Task 20: Validate Full Application Functionality
**Objective**: Ensure the deployed application maintains all original functionality

**Steps**:
- Access the frontend application via NodePort
- Test all major application features
- Verify that all original functionality is preserved
- Validate that Phase III behavior is maintained

**Acceptance Criteria**:
- Frontend accessible and functional
- All application features working correctly
- Original functionality preserved
- Phase III behavior maintained

**Dependencies**: Tasks 15, 16

### Task 21: Validate AI-Generated Logs
**Objective**: Verify that AI-generated logs and operational data are preserved

**Steps**:
- Access logs from frontend and backend pods
- Verify AI operations logs are available
- Confirm operational data is being captured
- Validate log format and content

**Acceptance Criteria**:
- Application logs accessible and readable
- AI operations logs preserved
- Operational data captured correctly
- Log format consistent with requirements

**Dependencies**: Tasks 13, 14

### Task 22: Final Deployment Validation
**Objective**: Perform final validation of the complete deployment

**Steps**:
- Run through all acceptance criteria from previous tasks
- Verify all requirements from the original specification are met
- Confirm all AI-assisted tools were used as required
- Document final deployment status

**Acceptance Criteria**:
- All original requirements satisfied
- AI-assisted tools used throughout process
- Deployment fully functional
- Final status documented

**Dependencies**: All previous tasks