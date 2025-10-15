#!/bin/bash

# Kubernetes deployment script for Emotion Diary

set -e

echo "🚀 Starting Emotion Diary Kubernetes deployment..."

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot access Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Apply Kubernetes manifests in order
echo "📦 Applying Kubernetes manifests..."

echo "  📝 Creating namespace and configuration..."
kubectl apply -f k8s/00-namespace-config.yaml

echo "  🗄️  Deploying PostgreSQL..."
kubectl apply -f k8s/01-postgres.yaml

echo "  ⏳ Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n emotion-diary --timeout=300s

echo "  🔧 Deploying backend..."
kubectl apply -f k8s/02-backend.yaml

echo "  ⏳ Waiting for backend to be ready..."
kubectl wait --for=condition=ready pod -l app=backend -n emotion-diary --timeout=300s

echo "  🌐 Deploying frontend..."
kubectl apply -f k8s/03-frontend.yaml

echo "  ⏳ Waiting for frontend to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend -n emotion-diary --timeout=300s

echo "  📡 Deploying Redis..."
kubectl apply -f k8s/05-redis.yaml

echo "  ⏳ Waiting for Redis to be ready..."
kubectl wait --for=condition=ready pod -l app=redis -n emotion-diary --timeout=300s

echo "  🌍 Deploying Ingress..."
kubectl apply -f k8s/04-ingress.yaml

echo "🎉 Deployment completed successfully!"

echo ""
echo "📊 Deployment status:"
kubectl get pods -n emotion-diary
echo ""
kubectl get services -n emotion-diary
echo ""
kubectl get ingress -n emotion-diary

echo ""
echo "🔗 Access your application:"
echo "   Local: http://emotion-diary.local (add to /etc/hosts)"
echo "   API Docs: http://emotion-diary.local/api/docs"

echo ""
echo "📝 Useful commands:"
echo "   View logs: kubectl logs -f deployment/backend -n emotion-diary"
echo "   Scale up: kubectl scale deployment backend --replicas=3 -n emotion-diary"
echo "   Delete all: kubectl delete namespace emotion-diary"