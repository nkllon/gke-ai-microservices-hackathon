#!/usr/bin/env python3
"""
🧹 Teardown Script Generator for GCP Project
Generates teardown-gcp-project.sh from the project model registry template
"""

import json
import os
import sys
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

def extract_teardown_template(model):
    """Extract the teardown script template from the GKE hackathon configuration"""
    try:
        # Navigate to the GKE hackathon configuration
        hackathon_config = model['domains']['hackathon']['hackathon_mapping']['gke_turns_10']
        teardown_template = hackathon_config['gcp_project_setup']['teardown_template']
        return teardown_template
    except KeyError as e:
        print(f"❌ Failed to extract teardown template: {e}")
        available_keys = list(model.keys()) if 'domains' in model else "No domains"
        print("Available keys:", available_keys)
        sys.exit(1)

def generate_script(template_data):
    """Generate the script from the template and variables"""
    template = template_data['template']
    variables = template_data['variables']
    
    # Replace template variables
    script_content = template
    
    for var_name, var_value in variables.items():
        placeholder = f"{{{{{var_name}}}}}"
        
        # Handle special cases for arrays
        if var_name == 'required_apis':
            # Convert JSON array to bash array format
            if isinstance(var_value, list):
                api_list = var_value
            else:
                # Fallback to string processing
                api_list = var_value.strip().split('\n')
                api_list = [api.strip() for api in api_list if api.strip()]
            
            # Create bash array with comments
            api_comments = {
                "container.googleapis.com": "GKE clusters",
                "compute.googleapis.com": "VM instances, networking",
                "monitoring.googleapis.com": "Metrics, alerts, dashboards",
                "logging.googleapis.com": "Log aggregation",
                "cloudresourcemanager.googleapis.com": "Project management",
                "iam.googleapis.com": "Identity and access management"
            }
            
            bash_array_lines = []
            for api in api_list:
                comment = api_comments.get(api, "")
                if comment:
                    bash_array_lines.append(f'    "{api}"           # {comment}')
                else:
                    bash_array_lines.append(f'    "{api}"')
            
            bash_array = '\n'.join(bash_array_lines)
            script_content = script_content.replace(placeholder, bash_array)
            
        elif var_name == 'excluded_apis':
            # Convert JSON array to bash array format
            if isinstance(var_value, list):
                api_list = var_value
            else:
                # Fallback to string processing
                api_list = var_value.strip().split('\n')
                api_list = [api.strip() for api in api_list if api.strip()]
            
            # Create bash array with comments
            api_comments = {
                "cloudfunctions.googleapis.com": "Not using serverless",
                "run.googleapis.com": "Not using Cloud Run",
                "firestore.googleapis.com": "Not using Firestore",
                "pubsub.googleapis.com": "Not using messaging",
                "storage.googleapis.com": "Not using Cloud Storage"
            }
            
            bash_array_lines = []
            for api in api_list:
                comment = api_comments.get(api, "")
                if comment:
                    bash_array_lines.append(f'    "{api}"           # {comment}')
                else:
                    bash_array_lines.append(f'    "{api}"')
            
            bash_array = '\n'.join(bash_array_lines)
            script_content = script_content.replace(placeholder, bash_array)
            
        else:
            # Handle regular variables
            script_content = script_content.replace(placeholder, str(var_value))
    
    return script_content

def write_script(script_content, output_path):
    """Write the generated script to the output file"""
    try:
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        # Make the script executable
        os.chmod(output_path, 0o755)
        
        print(f"✅ Generated teardown script: {output_path}")
        print(f"✅ Made script executable")
        
    except Exception as e:
        print(f"❌ Failed to write script: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🧹 GCP Project Teardown Script Generator")
    print("=========================================")
    print("")
    
    # Load project model
    print("📖 Loading project model registry...")
    model = load_project_model()
    print("✅ Project model loaded successfully")
    
    # Extract teardown template
    print("🔍 Extracting teardown template...")
    template_data = extract_teardown_template(model)
    print("✅ Teardown template extracted")
    
    # Generate script
    print("🔧 Generating teardown script from template...")
    script_content = generate_script(template_data)
    print("✅ Teardown script content generated")
    
    # Write generated script
    output_path = Path(__file__).parent / "teardown-gcp-project.sh"
    print(f"📝 Writing teardown script to: {output_path}")
    write_script(script_content, output_path)
    
    print("\n📋 Summary:")
    print(f"   📖 Model loaded: project_model_registry.json")
    print(f"   🔧 Template extracted: GKE hackathon teardown configuration")
    print(f"   📝 Script generated: {output_path}")
    
    print("\n🚨 IMPORTANT WARNING:")
    print("   ⚠️  This teardown script will PERMANENTLY DELETE the hackathon project!")
    print("   ⚠️  All data, services, and resources will be lost!")
    print("   ⚠️  This action cannot be undone!")
    print("")
    print("   💡 Use this script ONLY when you're completely done with the hackathon!")
    print("   💡 It will clean up all costs and free up billing quota!")
    
    print("\n🚀 Teardown script ready for use!")

if __name__ == "__main__":
    main()
