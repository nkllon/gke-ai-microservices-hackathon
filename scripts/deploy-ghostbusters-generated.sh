#!/bin/bash

# 🚀 Ghostbusters AI Microservices Deployment Script
# GKE Hackathon Implementation
#
# MODEL VERSION: df6775bb15b5b375
# GENERATED FROM: project_model_registry.json
# GENERATION TIMESTAMP: 2025-08-14T16:52:33.744973
#
# ⚠️  IMPORTANT: This script was generated from a specific model version
# ⚠️  DO NOT EDIT MANUALLY - regenerate from model instead
# ⚠️  Version mismatch between deploy/teardown = BROKEN CLEANUP
#
# Dependencies:
# - gcloud CLI (Google Cloud SDK)
# - kubectl (Kubernetes CLI) - install via: gcloud components install kubectl --quiet
# - Note: Docker not required for GKE deployment (only needed for local container builds)
#
# Prerequisites:
# - GCP project created and configured
# - Required APIs enabled
# - User authenticated and authorized
#
# Note: This script uses cost-effective GKE approaches:
# - IPv4 stack type (no advanced datapath costs)
# - Simplified cluster creation with essential flags only
# - Accepts kubelet readonly port deprecation warnings (expected behavior)
# - See Google docs: https://cloud.google.com/kubernetes-engine/docs/deprecations
#
# See GKE_DEPLOYMENT_DEPENDENCIES.md for detailed setup instructions

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
        print_info "Installation: curl https://sdk.cloud.google.com | bash"
        exit 1
    fi
    
    # Check gcloud version
    GCLOUD_VERSION=$(gcloud version | head -1)
    print_info "gcloud version: "GCLOUD_VERSIO"N"
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install it first."
        print_info "Installation: gcloud components install kubectl --quiet"
        exit 1
    fi
    
    # Check kubectl version
    KUBECTL_VERSION=$(kubectl version --client --output=yaml | grep gitVersion | cut -d' ' -f4)
    print_info "kubectl version: "KUBECTL_VERSIO"N"
    
    # Note: Docker is not required for GKE deployment
    # Docker is only needed if building containers locally
    print_info "Docker check skipped - not required for GKE deployment"
    
    # Check if user is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."
        exit 1
    fi
    
    # Check if project is set
    CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
    if [ ""CURRENT_PROJEC"T" != ""PROJECT_I"D" ]; then
        print_warning "Current project is '"CURRENT_PROJECT"', expected '"PROJECT_ID"'"
        print_info "Setting project to "PROJECT_ID"..."
        gcloud config set project "PROJECT_I"D
    fi
    
    # Check if project exists and is accessible
    if ! gcloud projects describe "PROJECT_I"D &> /dev/null; then
        print_error "Project "PROJECT_I"D not found or not accessible"
        exit 1
    fi
    
    # Check if required APIs are enabled
    print_info "Verifying required APIs are enabled..."
    REQUIRED_APIS=(
        "container.googleapis.com"
        "compute.googleapis.com"
        "monitoring.googleapis.com"
        "logging.googleapis.com"
        "cloudresourcemanager.googleapis.com"
        "iam.googleapis.com"
    )
    
    for api in "${REQUIRED_APIS[@]}"; do
        if gcloud services list --enabled --project="PROJECT_I"D --filter="name:"ap"i" | grep -q ""ap"i"; then
            print_status "API enabled: "ap"i"
        else
            print_error "Required API not enabled: "ap"i"
            print_info "Enable with: gcloud services enable "ap"i --project="PROJECT_I"D"
            exit 1
        fi
    done
    
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
    gcloud config set project "PROJECT_I"D
    print_status "Project set to: "PROJECT_I"D"
}

# Create GKE cluster
create_gke_cluster() {
    print_info "Creating GKE cluster: "CLUSTER_NAM"E"
    
    # Check if cluster already exists
    if gcloud container clusters describe "CLUSTER_NAM"E --zone="ZON"E &> /dev/null; then
        print_warning "Cluster "CLUSTER_NAM"E already exists"
        return
    fi
    
    # Create cluster with essential cost optimization flags (IPv4 for cost-effectiveness)
    gcloud container clusters create "CLUSTER_NAM"E \
        --zone="ZON"E \
        --machine-type=e2-micro \
        --disk-size=20 \
        --disk-type=pd-standard \
        --preemptible \
        --enable-autoscaling \
        --min-nodes=1 \
        --max-nodes="MAX_NODE"S \
        --enable-autorepair \
        --no-enable-autoupgrade \
        --enable-ip-alias \
        --labels=cost-center=hackathon,environment=development,auto-shutdown=true
    
    # Note: Using IPv4 stack type for cost-effectiveness:
    # 1. No advanced datapath requirements (keeps costs low)
    # 2. Simpler networking setup (easier for hackathon)
    # 3. Better documentation and troubleshooting support
    # 
    # Note: The kubelet readonly port (10255) deprecation warning is expected
    # This is a Google deprecation notice and doesn't affect functionality
    # See: https://cloud.google.com/kubernetes-engine/docs/how-to/disable-kubelet-readonly-port
    
    print_status "GKE cluster created successfully"
}

# Enable logging and monitoring (optional, can be done after cluster creation)
enable_logging_monitoring() {
    print_info "Enabling logging and monitoring..."
    
    # Enable logging
    gcloud container clusters update "CLUSTER_NAM"E \
        --zone="ZON"E \
        --logging=SYSTEM,WORKLOAD \
        --quiet
    
    # Enable monitoring
    gcloud container clusters update "CLUSTER_NAM"E \
        --zone="ZON"E \
        --monitoring=SYSTEM,WORKLOAD \
        --quiet
    
    print_status "Logging and monitoring enabled"
}

# Get cluster credentials
get_cluster_credentials() {
    print_info "Getting cluster credentials..."
    
    gcloud container clusters get-credentials "CLUSTER_NAM"E --zone="ZON"E
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
    echo "🎯 GKE Cluster: "CLUSTER_NAM"E"
    echo "🌐 Project: "PROJECT_I"D"
    echo "📍 Zone: "ZON"E"
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
    echo "  - Max Nodes: "MAX_NODE"S"
    echo "  - Max Pods per Service: "MAX_PODS_PER_SERVIC"E"
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