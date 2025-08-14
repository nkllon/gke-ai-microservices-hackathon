#!/usr/bin/env python3
"""
🚀 Script Generator for GCP Project Setup
Generates setup-gcp-project.sh from the project model registry template
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

def extract_script_template(model):
    """Extract the script template from the GKE hackathon configuration"""
    try:
        # Navigate to the GKE hackathon configuration
        hackathon_config = model['domains']['hackathon']['hackathon_mapping']['gke_turns_10']
        script_template = hackathon_config['gcp_project_setup']['script_template']
        return script_template
    except KeyError as e:
        print(f"❌ Failed to extract script template: {e}")
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
            # Convert newline-separated string to bash array format
            api_list = var_value.strip().split('\n')
            api_list = [api.strip() for api in api_list if api.strip()]
            bash_array = '    "' + '"\n    "'.join(api_list) + '"'
            script_content = script_content.replace(placeholder, bash_array)
        elif var_name == 'excluded_apis':
            # Convert newline-separated string to bash array format
            api_list = var_value.strip().split('\n')
            api_list = [api.strip() for api in api_list if api.strip()]
            bash_array = '    "' + '"\n    "'.join(api_list) + '"'
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
        
        print(f"✅ Generated script: {output_path}")
        print(f"✅ Made script executable")
        
    except Exception as e:
        print(f"❌ Failed to write script: {e}")
        sys.exit(1)

def verify_script_generation(original_path, generated_path):
    """Verify that the generated script matches the original"""
    try:
        with open(original_path, 'r') as f:
            original_content = f.read()
        
        with open(generated_path, 'r') as f:
            generated_content = f.read()
        
        # Remove trailing whitespace and normalize line endings
        original_clean = original_content.rstrip()
        generated_clean = generated_content.rstrip()
        
        if original_clean == generated_clean:
            print("✅ Generated script matches original exactly!")
            return True
        else:
            print("⚠️  Generated script differs from original")
            
            # Show differences
            original_lines = original_clean.split('\n')
            generated_lines = generated_clean.split('\n')
            
            print("\n📊 Line count comparison:")
            print(f"   Original: {len(original_lines)} lines")
            print(f"   Generated: {len(generated_lines)} lines")
            
            # Find first difference
            for i, (orig, gen) in enumerate(zip(original_lines, generated_lines)):
                if orig != gen:
                    print(f"\n🔍 First difference at line {i+1}:")
                    print(f"   Original: {orig}")
                    print(f"   Generated: {gen}")
                    break
            
            return False
            
    except Exception as e:
        print(f"❌ Failed to verify script: {e}")
        return False

def main():
    """Main function"""
    print("🚀 GCP Project Setup Script Generator")
    print("=====================================")
    print("")
    
    # Load project model
    print("📖 Loading project model registry...")
    model = load_project_model()
    print("✅ Project model loaded successfully")
    
    # Extract script template
    print("🔍 Extracting script template...")
    template_data = extract_script_template(model)
    print("✅ Script template extracted")
    
    # Generate script
    print("🔧 Generating script from template...")
    script_content = generate_script(template_data)
    print("✅ Script content generated")
    
    # Write generated script
    output_path = Path(__file__).parent / "setup-gcp-project-generated.sh"
    print(f"📝 Writing generated script to: {output_path}")
    write_script(script_content, output_path)
    
    # Verify against original
    original_path = Path(__file__).parent / "setup-gcp-project.sh"
    if original_path.exists():
        print("\n🔍 Verifying generated script against original...")
        verification_result = verify_script_generation(original_path, output_path)
        
        if verification_result:
            print("\n🎉 SUCCESS: Generated script is equivalent to original!")
            print("✅ The model-driven approach is working perfectly!")
        else:
            print("\n⚠️  WARNING: Generated script differs from original")
            print("🔧 Manual review may be needed")
    else:
        print("\n⚠️  Original script not found for comparison")
        print("📝 Generated script saved as: setup-gcp-project-generated.sh")
    
    print("\n📋 Summary:")
    print(f"   📖 Model loaded: project_model_registry.json")
    print(f"   🔧 Template extracted: GKE hackathon configuration")
    print(f"   📝 Script generated: {output_path}")
    print(f"   🔍 Verification: {'PASSED' if 'verification_result' in locals() and verification_result else 'FAILED'}")
    
    print("\n🚀 Ready to use the generated script!")

if __name__ == "__main__":
    main()
