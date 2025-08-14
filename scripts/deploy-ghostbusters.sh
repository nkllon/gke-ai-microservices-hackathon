#!/bin/bash

# 🚀 Ghostbusters AI Microservices Deployment Script
# GKE Hackathon Implementation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLUSTER_NAME="ghostbusters-hackathon"
PROJECT_ID="ghostbusters-hackathon-2025"
REGION="us-central1"
ZONE="us-central1-a"

# Cost control thresholds
MAX_NODES=3
MAX_PODS_PER_SERVICE=3

echo -e "${BLUE}🚀 Ghostbusters AI Microservices Deployment${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install it first."
        exit 1
    fi
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    print_status "All prerequisites are satisfied"
}

# Authenticate with GCP
authenticate_gcp() {
    print_info "Authenticating with GCP..."
    
    # Check if already authenticated
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_status "Already authenticated with GCP"
    else
        gcloud auth login
        print_status "GCP authentication completed"
    fi
    
    # Set project
    gcloud config set project $PROJECT_ID
    print_status "Project set to: $PROJECT_ID"
}

# Create GKE cluster
create_gke_cluster() {
    print_info "Creating GKE cluster: $CLUSTER_NAME"
    
    # Check if cluster already exists
    if gcloud container clusters describe $CLUSTER_NAME --zone=$ZONE &> /dev/null; then
        print_warning "Cluster $CLUSTER_NAME already exists"
        return
    fi
    
    # Create cluster with cost optimization
    gcloud container clusters create $CLUSTER_NAME \
        --zone=$ZONE \
        --machine-type=e2-micro \
        --disk-size=20 \
        --disk-type=pd-standard \
        --preemptible \
        --enable-autoscaling \
        --min-nodes=1 \
        --max-nodes=$MAX_NODES \
        --enable-autorepair \
        --no-enable-autoupgrade \
        --enable-network-policy \
        --enable-ip-alias \
        --enable-stackdriver-kubernetes \
        --labels=cost-center=hackathon,environment=development,auto-shutdown=true
    
    print_status "GKE cluster created successfully"
}

# Get cluster credentials
get_cluster_credentials() {
    print_info "Getting cluster credentials..."
    
    gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE
    print_status "Cluster credentials obtained"
}

# Create namespaces
create_namespaces() {
    print_info "Creating namespaces..."
    
    kubectl apply -f k8s/namespaces/ghostbusters-namespace.yaml
    print_status "Namespaces created"
}

# Deploy configuration
deploy_configuration() {
    print_info "Deploying configuration..."
    
    kubectl apply -f k8s/config/ghostbusters-config.yaml
    print_status "Configuration deployed"
}

# Deploy core services
deploy_core_services() {
    print_info "Deploying core services..."
    
    # Deploy orchestrator
    kubectl apply -f k8s/services/orchestrator-service.yaml
    print_status "Orchestrator service deployed"
    
    # Deploy AI agents
    kubectl apply -f k8s/services/ai-agents.yaml
    print_status "AI agents deployed"
    
    # Wait for deployments to be ready
    print_info "Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/ghostbusters-orchestrator -n ghostbusters-ai
    kubectl wait --for=condition=available --timeout=300s deployment/ghostbusters-security-agent -n ghostbusters-ai
    kubectl wait --for=condition=available --timeout=300s deployment/ghostbusters-quality-agent -n ghostbusters-ai
    kubectl wait --for=condition=available --timeout=300s deployment/ghostbusters-test-agent -n ghostbusters-ai
    kubectl wait --for=condition=available --timeout=300s deployment/ghostbusters-performance-agent -n ghostbusters-ai
    
    print_status "All core services are ready"
}

# Deploy ingress and frontend
deploy_ingress() {
    print_info "Deploying ingress and frontend..."
    
    kubectl apply -f k8s/ingress/ghostbusters-ingress.yaml
    print_status "Ingress and frontend deployed"
}

# Deploy monitoring
deploy_monitoring() {
    print_info "Deploying monitoring stack..."
    
    kubectl apply -f k8s/monitoring/ghostbusters-monitoring.yaml
    print_status "Monitoring stack deployed"
}

# Verify deployment
verify_deployment() {
    print_info "Verifying deployment..."
    
    # Check namespaces
    echo "Namespaces:"
    kubectl get namespaces | grep ghostbusters
    
    # Check pods
    echo ""
    echo "Pods in ghostbusters-ai:"
    kubectl get pods -n ghostbusters-ai
    
    echo ""
    echo "Pods in ghostbusters-ingress:"
    kubectl get pods -n ghostbusters-ingress
    
    echo ""
    echo "Pods in ghostbusters-monitoring:"
    kubectl get pods -n ghostbusters-monitoring
    
    # Check services
    echo ""
    echo "Services:"
    kubectl get services --all-namespaces | grep ghostbusters
    
    # Check ingress
    echo ""
    echo "Ingress:"
    kubectl get ingress -n ghostbusters-ingress
    
    print_status "Deployment verification completed"
}

# Show access information
show_access_info() {
    print_info "Access Information:"
    echo ""
    echo "🎯 GKE Cluster: $CLUSTER_NAME"
    echo "🌐 Project: $PROJECT_ID"
    echo "📍 Zone: $ZONE"
    echo ""
    echo "🔗 Services:"
    echo "  - Orchestrator: http://ghostbusters-orchestrator.ghostbusters-ai.svc.cluster.local:8080"
    echo "  - Security Agent: http://ghostbusters-security-agent.ghostbusters-ai.svc.cluster.local:8080"
    echo "  - Quality Agent: http://ghostbusters-quality-agent.ghostbusters-ai.svc.cluster.local:8080"
    echo "  - Test Agent: http://ghostbusters-test-agent.ghostbusters-ai.svc.cluster.local:8080"
    echo "  - Performance Agent: http://ghostbusters-performance-agent.ghostbusters-ai.svc.cluster.local:8080"
    echo ""
    echo "📊 Monitoring:"
    echo "  - Prometheus: http://prometheus.ghostbusters-monitoring.svc.cluster.local:9090"
    echo "  - Grafana: http://grafana.ghostbusters-monitoring.svc.cluster.local:3000"
    echo ""
    echo "💰 Cost Control:"
    echo "  - Max Nodes: $MAX_NODES"
    echo "  - Max Pods per Service: $MAX_PODS_PER_SERVICE"
    echo "  - Preemptible Instances: Enabled (50% cost savings)"
    echo "  - Machine Type: e2-micro (smallest, cheapest)"
    echo ""
    echo "📝 Next Steps:"
    echo "  1. Wait for ingress IP to be assigned"
    echo "  2. Update DNS with the ingress IP"
    echo "  3. Test the services"
    echo "  4. Monitor costs with: python scripts/gcp_billing_daily_reporter.py"
}

# Main deployment function
main() {
    echo -e "${BLUE}Starting Ghostbusters AI deployment...${NC}"
    echo ""
    
    check_prerequisites
    authenticate_gcp
    create_gke_cluster
    get_cluster_credentials
    create_namespaces
    deploy_configuration
    deploy_core_services
    deploy_ingress
    deploy_monitoring
    verify_deployment
    show_access_info
    
    echo ""
    print_status "🎉 Ghostbusters AI deployment completed successfully!"
    echo ""
    print_info "Monitor your deployment with:"
    echo "  kubectl get pods --all-namespaces"
    echo "  kubectl get services --all-namespaces"
    echo "  kubectl get ingress --all-namespaces"
    echo ""
    print_info "Check costs with:"
    echo "  python scripts/gcp_billing_daily_reporter.py"
    echo ""
    print_warning "Remember: This is a cost-optimized deployment for hackathon development!"
}

# Run main function
main "$@"
