#!/bin/bash

# 🧹 GCP Project Teardown Script for Ghostbusters AI Hackathon 2025
# This script cleans up the hackathon project and all associated resources

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

# REQUIRED APIs that were enabled (to be disabled)
REQUIRED_APIS=(
    "container.googleapis.com"           # GKE clusters
    "compute.googleapis.com"           # VM instances, networking
    "monitoring.googleapis.com"           # Metrics, alerts, dashboards
    "logging.googleapis.com"           # Log aggregation
    "cloudresourcemanager.googleapis.com"           # Project management
    "iam.googleapis.com"           # Identity and access management
)

# Cost control thresholds
MONTHLY_BUDGET=25.0
DEVELOPMENT_PHASE=5.0
TESTING_PHASE=15.0
DEMO_PHASE=25.0

echo -e "${BLUE}🧹 GCP Project Teardown for Ghostbusters AI Hackathon 2025${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

echo -e "${YELLOW}⚠️  WARNING: This script will PERMANENTLY DELETE the hackathon project!${NC}"
echo -e "${YELLOW}⚠️  All data, services, and resources will be lost!${NC}"
echo ""

echo -e "${YELLOW}⚠️  This action cannot be undone!${NC}"
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

# Confirmation prompt
confirm_teardown() {
    echo -e "${RED}Are you absolutely sure you want to delete project "PROJECT_ID"?${NC}"
    echo -e "${RED}Type 'DELETE' to confirm:${NC}"
    read -r confirmation
    
    if [ ""confirmatio"n" != "DELETE" ]; then
        print_warning "Teardown cancelled by user"
        exit 0
    fi
    
    print_status "Teardown confirmed. Proceeding with deletion..."
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
    
    # Check if project exists
    if ! gcloud projects describe "PROJECT_I"D &> /dev/null; then
        print_error "Project "PROJECT_I"D does not exist"
        exit 1
    fi
    
    print_status "All prerequisites are satisfied"
}

# Disable all enabled APIs
disable_all_apis() {
    print_info "Disabling all enabled APIs..."
    
    # Get list of enabled APIs
    ENABLED_APIS=$(gcloud services list --enabled --project="PROJECT_I"D --format="value(name)")
    
    if [ -z ""ENABLED_API"S" ]; then
        print_warning "No APIs enabled in project"
        return
    fi
    
    # Disable each API
    for api in "ENABLED_APIS"; do
        print_info "Disabling API: "ap"i"
        gcloud services disable "ap"i --project="PROJECT_I"D --quiet || print_warning "Failed to disable "ap"i"
    done
    
    print_status "All APIs disabled"
}

# Delete GKE clusters
delete_gke_clusters() {
    print_info "Checking for GKE clusters..."
    
    # List all clusters
    CLUSTERS=$(gcloud container clusters list --project="PROJECT_I"D --format="value(name,location)" 2>/dev/null || echo "")
    
    if [ -n ""CLUSTER"S" ]; then
        print_warning "Found GKE clusters. Deleting..."
        
        while IFS= read -r cluster_info; do
            if [ -n ""cluster_inf"o" ]; then
                CLUSTER_NAME=$(echo ""cluster_inf"o" | cut -d' ' -f1)
                LOCATION=$(echo ""cluster_inf"o" | cut -d' ' -f2)
                
                print_info "Deleting cluster: "CLUSTER_NAM"E in "LOCATIO"N"
                gcloud container clusters delete "CLUSTER_NAM"E --location="LOCATIO"N --project="PROJECT_I"D --quiet || \
    print_warning "Failed to delete cluster $CLUSTER_NAME"
            fi
        done <<< ""CLUSTER"S"
    else
        print_status "No GKE clusters found"
    fi
}

# Delete compute instances
delete_compute_instances() {
    print_info "Checking for compute instances..."
    
    # List all instances
    INSTANCES=$(gcloud compute instances list --project="PROJECT_I"D --format="value(name,zone)" 2>/dev/null || echo "")
    
    if [ -n ""INSTANCE"S" ]; then
        print_warning "Found compute instances. Deleting..."
        
        while IFS= read -r instance_info; do
            if [ -n ""instance_inf"o" ]; then
                INSTANCE_NAME=$(echo ""instance_inf"o" | cut -d' ' -f1)
                ZONE=$(echo ""instance_inf"o" | cut -d' ' -f2)
                
                print_info "Deleting instance: "INSTANCE_NAM"E in "ZON"E"
                gcloud compute instances delete "INSTANCE_NAM"E --zone="ZON"E --project="PROJECT_I"D --quiet || \
    print_warning "Failed to delete instance $INSTANCE_NAME"
            fi
        done <<< ""INSTANCE"S"
    else
        print_status "No compute instances found"
    fi
}

# Delete storage buckets
delete_storage_buckets() {
    print_info "Checking for storage buckets..."
    
    # List all buckets
    BUCKETS=$(gsutil ls -p "PROJECT_I"D 2>/dev/null || echo "")
    
    if [ -n ""BUCKET"S" ]; then
        print_warning "Found storage buckets. Deleting..."
        
        for bucket in "BUCKETS"; do
            if [ -n ""bucke"t" ]; then
                print_info "Deleting bucket: "bucke"t"
                gsutil -m rm -r "bucke"t || print_warning "Failed to delete bucket "bucke"t"
            fi
        done
    else
        print_status "No storage buckets found"
    fi
}

# Delete budgets
delete_budgets() {
    print_info "Deleting project budgets..."
    
    # List budgets for this project
    BUDGETS=$(gcloud billing budgets list --billing-account="BILLING_ACCOUN"T --filter="displayName:2025" --format="value(name)" 2>/dev/null || \
    echo "")
    
    if [ -n ""BUDGET"S" ]; then
        for budget in "BUDGETS"; do
            if [ -n ""budge"t" ]; then
                print_info "Deleting budget: "budge"t"
                gcloud billing budgets delete "budge"t --quiet || print_warning "Failed to delete budget "budge"t"
            fi
        done
    else
        print_status "No budgets found"
    fi
}

# Unlink billing account
unlink_billing() {
    print_info "Unlinking billing account..."
    
    # Unlink billing account
    gcloud billing projects unlink "PROJECT_I"D --quiet || print_warning "Failed to unlink billing account"
    
    print_status "Billing account unlinked"
}

# Delete the project
delete_project() {
    print_info "Deleting project "PROJECT_ID"..."
    
    # Delete the project
    gcloud projects delete "PROJECT_I"D --quiet
    
    print_status "Project "PROJECT_I"D deleted successfully"
}

# Update tracking file
update_tracking_file() {
    print_info "Updating project tracking..."
    
    if [ -f "PROJECT_SETUP_TRACKING.md" ]; then
        # Update the tracking file with teardown status
        sed -i "s/Status: ✅ SETUP COMPLETED/Status: 🗑️ PROJECT DELETED/" PROJECT_SETUP_TRACKING.md
        sed -i "s/✅ Project Creation - Completed.*/❌ Project Creation - Deleted $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
        sed -i "s/✅ Billing Setup - Completed.*/❌ Billing Setup - Removed $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
        sed -i "s/✅ API Enablement - Completed.*/❌ API Enablement - Disabled $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
        sed -i "s/✅ Cost Control Configuration - Completed.*/❌ Cost Control Configuration - Removed \
    $(date +%Y-%m-%d)/" PROJECT_SETUP_TRACKING.md
        
        print_status "Project tracking updated"
    else
        print_warning "Tracking file not found"
    fi
}

# Show teardown summary
show_teardown_summary() {
    print_info "Teardown Summary:"
    echo ""
    echo "🗑️  Project Deleted: "PROJECT_I"D"
    echo "🗑️  Project Name: "PROJECT_NAM"E"
    echo "🗑️  Billing Account: Unlinked"
    echo "🗑️  All APIs: Disabled"
    echo "🗑️  All Resources: Deleted"
    echo "🗑️  Budgets: Removed"
    echo ""
    echo "💰 Cost Control: Terminated"
    echo "🚫 No more charges from this project"
    echo ""
    echo "✅ Teardown completed successfully!"
}

# Main teardown function
main() {
    echo -e "${BLUE}Starting GCP project teardown for Ghostbusters AI Hackathon 2025...${NC}"
    echo ""
    
    confirm_teardown
    check_prerequisites
    disable_all_apis
    delete_gke_clusters
    delete_compute_instances
    delete_storage_buckets
    delete_budgets
    unlink_billing
    delete_project
    update_tracking_file
    show_teardown_summary
    
    echo ""
    print_status "🎉 GCP project teardown completed successfully!"
    echo ""
    print_info "Project "PROJECT_I"D has been completely removed."
    print_info "All resources, services, and billing have been cleaned up."
    echo ""
    print_warning "Remember: This project was specifically for the 2025 hackathon!"
    print_warning "All data and configurations have been permanently deleted."
}

# Run main function
main "$@"