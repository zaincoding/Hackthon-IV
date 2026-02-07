# Quickstart Guide: Local Kubernetes Deployment for Todo Chatbot

## Prerequisites

1. **Install Required Tools**:
   - Docker Desktop (version 4.53 or higher)
   - Minikube
   - kubectl
   - kubectl-ai plugin
   - Helm
   - Docker AI Agent (Gordon)

2. **Start Minikube Cluster**:
   ```bash
   minikube start
   ```

3. **Verify Cluster**:
   ```bash
   kubectl cluster-info
   ```

## Deployment Steps

### 1. Prepare Environment
```bash
# Clone or navigate to the project directory
cd Local\ Kubernetes\ Deployment/

# Ensure you're in the correct directory with frontend/ and backend/ folders
ls -la
```

### 2. Containerize Applications with Docker AI Agent (Gordon)
```bash
# Navigate to frontend directory and generate Dockerfile with Gordon
cd frontend/
# Use Docker AI Agent to generate or optimize Dockerfile if needed
cd ..

# Navigate to backend directory and generate Dockerfile with Gordon
cd backend/
# Use Docker AI Agent to generate or optimize Dockerfile if needed
cd ..
```

### 3. Build Docker Images
```bash
# Build frontend image
docker build -t todo-frontend:latest frontend/

# Build backend image
docker build -t todo-backend:latest backend/
```

### 4. Load Images into Minikube
```bash
# Load images into Minikube's container runtime
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 5. Generate Helm Charts with kubectl-ai
```bash
# Use kubectl-ai to generate Helm charts for both applications
# This step requires kubectl-ai to be properly configured
kubectl ai create helm-chart todo-frontend --image todo-frontend:latest
kubectl ai create helm-chart todo-backend --image todo-backend:latest
```

### 6. Create Namespace
```bash
kubectl create namespace todo-app
```

### 7. Deploy Applications
```bash
# Deploy backend first (since frontend depends on it)
helm install todo-backend ./charts/todo-backend --namespace todo-app --set image.repository=todo-backend,image.tag=latest

# Deploy frontend
helm install todo-frontend ./charts/todo-frontend --namespace todo-app --set image.repository=todo-frontend,image.tag=latest
```

### 8. Expose Frontend Service
```bash
# Verify services are running
kubectl get svc -n todo-app

# The frontend should already be exposed as NodePort via the Helm chart
```

### 9. Access the Application
```bash
# Get the NodePort for the frontend service
minikube service todo-frontend -n todo-app --url
```

### 10. Validate Deployment
```bash
# Check pod statuses
kubectl get pods -n todo-app

# Check service connectivity
kubectl get svc -n todo-app

# View application logs
kubectl logs -l app=todo-backend -n todo-app
kubectl logs -l app=todo-frontend -n todo-app
```

## AI-Assisted Operations

### Scale Backend Pods
```bash
# Use Kagent or kubectl-ai to scale backend
kubectl ai scale deployment todo-backend --replicas 3 -n todo-app
```

### Analyze Cluster Resources
```bash
# Use Kagent for cluster analysis
kubectl ai analyze resources -n todo-app
```

### Debug Issues
```bash
# Use kubectl-ai for debugging
kubectl ai debug pod <pod-name> -n todo-app
```

## Cleanup
```bash
# Uninstall Helm releases
helm uninstall todo-frontend -n todo-app
helm uninstall todo-backend -n todo-app

# Delete namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop
```