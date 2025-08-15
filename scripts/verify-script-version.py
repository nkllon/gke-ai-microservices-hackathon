#!/usr/bin/env python3
"""
🔍 Script Version Verifier
Verifies that generated scripts match the current model version
"""

import json
import hashlib
import re
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


def calculate_model_hash(model):
    """Calculate a hash of the model for version tracking"""
    model_str = json.dumps(model, sort_keys=True, indent=2)
    return hashlib.sha256(model_str.encode()).hexdigest()[:16]


def extract_script_version(script_path):
    """Extract the model version from a generated script"""
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        
        # Look for MODEL VERSION line
        match = re.search(r'MODEL VERSION: ([a-f0-9]{16})', content)
        if match:
            return match.group(1)
        else:
            return None
    except Exception as e:
        print(f"❌ Failed to read script: {e}")
        return None


def verify_script_version(script_path, current_hash):
    """Verify that a script matches the current model version"""
    script_hash = extract_script_version(script_path)
    
    if not script_hash:
        print(f"❌ No version hash found in {script_path}")
        return False
    
    if script_hash == current_hash:
        print(f"✅ Script version matches current model: {script_hash}")
        return True
    else:
        print(f"❌ Version mismatch!")
        print(f"   Script version: {script_hash}")
        print(f"   Current model:  {current_hash}")
        print(f"   Script needs regeneration from current model")
        return False


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python verify-script-version.py <script_path>")
        print("Example: python verify-script-version.py deploy-ghostbusters-generated.sh")
        sys.exit(1)
    
    script_path = Path(sys.argv[1])
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        sys.exit(1)
    
    print("🔍 Script Version Verification")
    print("==============================")
    print("")
    
    # Load current model
    print("📖 Loading current project model...")
    model = load_project_model()
    current_hash = calculate_model_hash(model)
    print(f"✅ Current model hash: {current_hash}")
    
    # Verify script version
    print(f"🔍 Verifying script: {script_path}")
    is_valid = verify_script_version(script_path, current_hash)
    
    print("")
    if is_valid:
        print("🎉 Script is up-to-date with current model!")
        print("✅ Safe to use for deployment/teardown")
    else:
        print("⚠️  Script is outdated!")
        print("❌ Regenerate script from current model before use")
        print("   Run: python generate-deploy-script.py")
    
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
