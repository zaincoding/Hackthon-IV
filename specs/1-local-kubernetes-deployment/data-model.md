# Data Model: Local Kubernetes Deployment for Todo Chatbot

## Overview
This document defines the data entities and structures for the Kubernetes deployment of the Todo Chatbot application. Since this is primarily a deployment feature, the data model focuses on the configuration and deployment entities rather than application data.

## Kubernetes Configuration Entities

### Frontend Service
**Description**: Next.js application that serves the Todo Chatbot UI
- **Name**: todo-frontend
- **Type**: Deployment, Service
- **Ports**:
  - Container Port: 3000 (Next.js default)
  - Service Port: 80
- **Environment Variables**:
  - NEXT_PUBLIC_BACKEND_URL: Points to backend service
  - NEXT_PUBLIC_OPENAI_API_KEY: From secret
- **Relationships**: Depends on backend service for API access

### Backend Service
**Description**: FastAPI application that provides the Todo Chatbot API endpoints
- **Name**: todo-backend
- **Type**: Deployment, Service
- **Ports**:
  - Container Port: 8000 (FastAPI default)
  - Service Port: 80
- **Environment Variables**:
  - OPENAI_API_KEY: From secret
  - HOST: 0.0.0.0
  - PORT: 8000
- **Relationships**: Provides API endpoints for frontend service

### Namespace
**Description**: Kubernetes namespace for organizing the deployment
- **Name**: todo-app
- **Purpose**: Isolate the Todo Chatbot deployment from other applications

### ConfigMap
**Description**: Configuration data for the applications
- **Name**: todo-app-config
- **Data**: Non-sensitive configuration values
- **Usage**: Store application settings that don't require encryption

### Secret
**Description**: Sensitive configuration data for the applications
- **Name**: todo-app-secrets
- **Data**: API keys and other sensitive values
- **Usage**: Store OpenAI API key and other sensitive configuration

## Helm Chart Structure

### Frontend Helm Chart
- **Chart Name**: todo-frontend
- **Components**:
  - Deployment manifest
  - Service manifest
  - ConfigMap/Secret references
  - Resource limits and requests

### Backend Helm Chart
- **Chart Name**: todo-backend
- **Components**:
  - Deployment manifest
  - Service manifest
  - ConfigMap/Secret references
  - Health checks
  - Resource limits and requests

## Deployment Parameters

### Environment Variables Mapping
- Frontend NEXT_PUBLIC_BACKEND_URL → Backend service internal URL
- Frontend NEXT_PUBLIC_OPENAI_API_KEY → Secret value
- Backend OPENAI_API_KEY → Secret value
- Backend SESSION_TIMEOUT_HOURS → ConfigMap value

### Resource Requirements
- CPU limits and requests for both frontend and backend
- Memory limits and requests for both frontend and backend
- Replica counts (initially 1 for both)

### Service Configuration
- Frontend exposed via NodePort for external access
- Backend accessible internally within the cluster
- Network policies (if required)