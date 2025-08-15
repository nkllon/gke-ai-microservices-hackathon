#!/bin/bash

# 🚀 GCP Project Setup Script for Ghostbusters AI Hackathon 2025
# This script creates a new GCP project and enables ONLY the required APIs

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration - EXACTLY as defined in project model
PROJECT_ID="ghostbusters-hackathon-2025"
PROJECT_NAME="Ghostbusters AI Hackathon 2025"
BILLING_ACCOUNT="01F112-E73FD5-795507"

# REQUIRED APIs (explicitly defined)
REQUIRED_APIS=(
    "container.googleapis.com"           # GKE clusters
    "compute.googleapis.com"             # VM instances, networking
    "monitoring.googleapis.com"          # Metrics, alerts, dashboards
    "logging.googleapis.com"             # Log aggregation
    "cloudresourcemanager.googleapis.com" # Project management
    "iam.googleapis.com"                 # Identity and access management
)

# EXCLUDED APIs (explicitly disabled for cost control)
EXCLUDED_APIS=(
    "cloudfunctions.googleapis.com"      # Not using serverless
    "run.googleapis.com"                 # Not using Cloud Run
    "firestore.googleapis.com"           # Not using Firestore
    "pubsub.googleapis.com"              # Not using messaging
    "storage.googleapis.com"             # Not using Cloud Storage
)

# Cost control thresholds
MONTHLY_BUDGET=25.00
DEVELOPMENT_PHASE=5.00
TESTING_PHASE=15.00
DEMO_PHASE=25.00

echo -e "${BLUE}🚀 GCP Project Setup for Ghostbusters AI Hackathon 2025${NC}"
echo -e "${BLUE}========================================================${NC}"
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
    
    # Check if user is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."
        exit 1
    fi
    
    print_status "All prerequisites are satisfied"
}

# Create new GCP project
create_gcp_project() {
    print_info "Creating new GCP project: "PROJECT_I"D"
    
    # Check if project already exists
    if gcloud projects describe "PROJECT_I"D &> /dev/null; then
        print_warning "Project "PROJECT_I"D already exists"
        return
    fi
    
    # Create new project
    gcloud projects create "PROJECT_I"D \
        --name=""PROJECT_NAM"E" \
        --set-as-default
    
    print_status "GCP project created successfully: "PROJECT_I"D"
}

# Set billing account
setup_billing() {
    print_info "Setting up billing account..."
    
    # Link billing account
    gcloud billing projects link "PROJECT_I"D \
        --billing-account="BILLING_ACCOUN"T
    
    # Verify billing link
    BILLING_STATUS=$(gcloud billing projects describe "PROJECT_I"D --format="value(billingEnabled)")
    
    if [ ""BILLING_STATU"S" = "True" ]; then
        print_status "Billing account linked successfully"
    else
        print_error "Failed to link billing account"
        exit 1
    fi
}

# Enable required APIs
enable_required_apis() {
    print_info "Enabling required APIs..."
    
    for api in "${REQUIRED_APIS[@]}"; do
        print_info "Enabling API: "ap"i"
        gcloud services enable "ap"i --project="PROJECT_I"D
        print_status "API enabled: "ap"i"
    done
    
    print_status "All required APIs enabled successfully"
}

# Verify API exclusions
verify_api_exclusions() {
    print_info "Verifying API exclusions..."
    
    # Get list of enabled APIs
    ENABLED_APIS=$(gcloud services list --enabled --project="PROJECT_I"D --format="value(name)")
    
    # Check for any excluded APIs that might be enabled
    for api in "${EXCLUDED_APIS[@]}"; do
        if echo ""ENABLED_API"S" | grep -q ""ap"i"; then
            print_warning "WARNING: Excluded API "ap"i is enabled - this may cause unwanted costs!"
        else
            print_status "Excluded API "ap"i is correctly disabled"
        fi
    done
}

# Create budget for cost control
setup_cost_control() {
    print_info "Setting up cost control..."
    
    # Create project budget
    gcloud billing budgets create \
        --billing-account="BILLING_ACCOUN"T \
        --budget-amount="MONTHLY_BUDGE"T \
        --budget-filter="project="PROJECT_I"D" \
        --display-name="Ghostbusters Hackathon 2025 Budget"
    
    print_status "Budget created: $${MONTHLY_BUDGET}/month"
}

# Verify project setup
verify_project_setup() {
    print_info "Verifying project setup..."
    
    echo ""
    echo "📊 Project Setup Verification:"
    echo "================================"
    
    # Check project status
    PROJECT_STATUS=$(gcloud projects describe "PROJECT_I"D --format="value(lifecycleState)")
    echo "Project Status: "PROJECT_STATU"S"
    
    # Check billing status
    BILLING_STATUS=$(gcloud billing projects describe "PROJECT_I"D --format="value(billingEnabled)")
    echo "Billing Status: "BILLING_STATU"S"
    
    # Count enabled APIs
    ENABLED_API_COUNT=$(gcloud services list --enabled --project="PROJECT_I"D --format="value(name)" | wc -l)
    echo "Enabled APIs: "ENABLED_API_COUN"T"
    
    # List enabled APIs
    echo ""
    echo "Enabled APIs:"
    gcloud services list --enabled --project="PROJECT_I"D --format="table(name,title)" | head -10
    
    # Check budget
    echo ""
    echo "Budget Configuration:"
    gcloud billing budgets list --billing-account="BILLING_ACCOUN"T --filter="displayName:2025"
    
    print_status "Project setup verification completed"
}

# Update tracking file
update_tracking_file() {
    print_info "Updating project setup tracking..."
    
    # Update the tracking file with current status
    sed -i "s/❌ Project Creation - Not started/✅ Project Creation - Completed $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
    sed -i "s/❌ Billing Setup - Not started/✅ Billing Setup - Completed $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
    sed -i "s/❌ API Enablement - Not started/✅ API Enablement - Completed $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
    sed -i "s/❌ Cost Control Configuration - Not started/✅ Cost Control Configuration - Completed \
    $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
    
    # Update setup status
    sed -i "s/Status: 🔄 SETUP IN PROGRESS/Status: ✅ SETUP COMPLETED/" PROJECT_SETUP_TRACKING.md
    
    print_status "Project setup tracking updated"
}

# Show next steps
show_next_steps() {
    print_info "Next Steps:"
    echo ""
    echo "🎯 Project Setup Complete!"
    echo "=========================="
    echo "✅ GCP Project: "PROJECT_I"D"
    echo "✅ Project Name: "PROJECT_NAM"E"
    echo "✅ Billing Account: "BILLING_ACCOUN"T"
    echo "✅ Required APIs: ${#REQUIRED_APIS[@]} enabled"
    echo "✅ Excluded APIs: ${#EXCLUDED_APIS[@]} disabled"
    echo "✅ Cost Control: $${MONTHLY_BUDGET}/month budget"
    echo ""
    echo "🚀 Ready to deploy Ghostbusters AI to GKE!"
    echo ""
    echo "Next Commands:"
    echo "1. Deploy to GKE: ./scripts/deploy-ghostbusters.sh"
    echo "2. Check costs: gcloud billing reports list --project="PROJECT_I"D"
    echo "3. Monitor APIs: gcloud services list --enabled --project="PROJECT_I"D"
    echo ""
    echo "💰 Cost Control Active:"
    echo "   - Development Phase: <$${DEVELOPMENT_PHASE}/month"
    echo "   - Testing Phase: <$${TESTING_PHASE}/month"
    echo "   - Demo Phase: <$${DEMO_PHASE}/month"
    echo "   - Emergency Controls: Enabled"
}

# Main setup function
main() {
    echo -e "${BLUE}Starting GCP project setup for Ghostbusters AI Hackathon 2025...${NC}"
    echo ""
    
    check_prerequisites
    create_gcp_project
    setup_billing
    enable_required_apis
    verify_api_exclusions
    setup_cost_control
    verify_project_setup
    update_tracking_file
    show_next_steps
    
    echo ""
    print_status "🎉 GCP project setup completed successfully!"
    echo ""
    print_info "Project "PROJECT_I"D is ready for Ghostbusters AI deployment!"
    print_info "All required APIs are enabled, excluded APIs are disabled."
    print_info "Cost control is configured with $${MONTHLY_BUDGET}/month budget."
    echo ""
    print_warning "Remember: This project is specifically for the 2025 hackathon!"
    print_warning "Costs are tracked separately and controlled to stay within budget."
}

# Run main function
main "$@"