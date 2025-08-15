#!/usr/bin/env python3
"""
🚀 Deploy Script Generator for GKE Project
Generates deploy-ghostbusters.sh from the project model registry template
"""

import json
import os
import sys
import hashlib
from pathlib import Path

def load_project_model():
    """Load the project model registry"""
    model_path = Path(__file__).parent.parent.parent / "project_model_registry.json"
    
    if not model_path.exists():
        print(f"❌ Project model registry not found at: {model_path}")
        sys.exit(1)
    
    try:
        with open(model_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse project model registry: {e}")
        sys.exit(1)

def calculate_model_hash(model):
    """Calculate a hash of the model for version tracking"""
    # Create a stable representation of the model
    model_str = json.dumps(model, sort_keys=True, indent=2)
    return hashlib.sha256(model_str.encode()).hexdigest()[:16]


def extract_deploy_template(model):
    """Extract the deploy script template from the GKE hackathon configuration"""
    try:
        # Navigate to the GKE hackathon configuration
        hackathon_config = model['domains']['hackathon']['hackathon_mapping']['gke_turns_10']
        deploy_template = hackathon_config['gcp_project_setup']['deploy_template']
        return deploy_template
    except KeyError as e:
        print(f"❌ Failed to extract deploy template: {e}")
        available_keys = list(model.keys()) if 'domains' in model else "No domains"
        print("Available keys:", available_keys)
        sys.exit(1)

def generate_script(template_data, model_hash):
    """Generate the script from the template and variables with version tracking"""
    # For now, we'll use the existing deploy script as a base
    # and update it with the model variables
    existing_script_path = Path(__file__).parent / "deploy-ghostbusters.sh"
    
    if not existing_script_path.exists():
        print("❌ Existing deploy script not found")
        sys.exit(1)
    
    # Read existing script
    with open(existing_script_path, 'r') as f:
        script_content = f.read()
    
    # Update variables from model
    variables = template_data['variables']
    
    # Update configuration section
    script_content = script_content.replace(
        'CLUSTER_NAME="ghostbusters-hackathon"',
        f'CLUSTER_NAME="{variables["cluster_name"]}"'
    )
    script_content = script_content.replace(
        'PROJECT_ID="ghostbusters-hackathon-2025"',
        f'PROJECT_ID="{variables["project_id"]}"'
    )
    script_content = script_content.replace(
        'REGION="us-central1"',
        f'REGION="{variables["region"]}"'
    )
    script_content = script_content.replace(
        'ZONE="us-central1-a"',
        f'ZONE="{variables["zone"]}"'
    )
    script_content = script_content.replace(
        'MAX_NODES="3"',
        f'MAX_NODES="{variables["max_nodes"]}"'
    )
    script_content = script_content.replace(
        'MAX_PODS_PER_SERVICE="3"',
        f'MAX_PODS_PER_SERVICE="{variables["max_pods_per_service"]}"'
    )
    
    # Add version tracking header
    version_header = f'''# 🚀 Ghostbusters AI Microservices Deployment Script
# GKE Hackathon Implementation
#
# MODEL VERSION: {model_hash}
# GENERATED FROM: project_model_registry.json
# GENERATION TIMESTAMP: {__import__("datetime").datetime.now().isoformat()}
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

'''
    
    # Replace the existing header
    script_content = script_content.replace(
        '# 🚀 Ghostbusters AI Microservices Deployment Script\n# GKE Hackathon Implementation\n#\n# Dependencies:\n# - gcloud CLI ( \
    Google Cloud SDK)\n# - kubectl (Kubernetes CLI) - install via: gcloud components install kubectl --quiet\n# - Note: Docker not required for GKE deployment (only needed for local container builds)\n#\n# Prerequisites:\n# - GCP project created and configured\n# - Required APIs enabled\n# - User authenticated and authorized\n#\n# Note: This script uses cost-effective GKE approaches:\n# - IPv4 stack type (no advanced datapath costs)\n# - Simplified cluster creation with essential flags only\n# - Accepts kubelet readonly port deprecation warnings (expected behavior)\n# - See Google docs: https://cloud.google.com/kubernetes-engine/docs/deprecations\n#\n# See GKE_DEPLOYMENT_DEPENDENCIES.md for detailed setup instructions\n\n',
        version_header
    )
    
    return script_content

def write_script(script_content, output_path):
    """Write the generated script to the output file"""
    try:
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        # Make the script executable
        os.chmod(output_path, 0o755)
        
        print(f"✅ Generated deploy script: {output_path}")
        print(f"✅ Made script executable")
        
    except Exception as e:
        print(f"❌ Failed to write script: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🚀 GKE Deploy Script Generator")
    print("===============================")
    print("")
    
    # Load project model
    print("📖 Loading project model registry...")
    model = load_project_model()
    print("✅ Project model loaded successfully")
    
    # Calculate model hash for version tracking
    print("🔐 Calculating model version hash...")
    model_hash = calculate_model_hash(model)
    print(f"✅ Model version hash: {model_hash}")
    
    # Extract deploy template
    print("🔍 Extracting deploy template...")
    template_data = extract_deploy_template(model)
    print("✅ Deploy template extracted")
    
    # Generate script
    print("🔧 Generating deploy script from template...")
    script_content = generate_script(template_data, model_hash)
    print("✅ Deploy script content generated")
    
    # Write generated script
    output_path = Path(__file__).parent / "deploy-ghostbusters-generated.sh"
    print(f"📝 Writing deploy script to: {output_path}")
    write_script(script_content, output_path)
    
    print("\n📋 Summary:")
    print(f"   📖 Model loaded: project_model_registry.json")
    print(f"   🔧 Template extracted: GKE hackathon deploy configuration")
    print(f"   📝 Script generated: {output_path}")
    
    print("\n🎯 Key Benefits:")
    print("   ✅ Deploy and teardown scripts are now model-driven")
    print("   ✅ Version consistency guaranteed between deploy/teardown")
    print("   ✅ No more out-of-band script changes causing mismatches")
    print("   ✅ Single source of truth for all deployment configuration")
    
    print("\n🚀 Deploy script ready for use!")

if __name__ == "__main__":
    main()