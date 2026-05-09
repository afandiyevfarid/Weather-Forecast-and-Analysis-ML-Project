#!/usr/bin/env python3
"""Verify that the Streamlit dashboard is properly configured."""

import os
import sys

def verify_setup():
    """Check all required directories and files."""
    
    print("\n🔍 Verifying Streamlit Dashboard Setup...")
    print("=" * 60)
    
    # Get project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"\n📁 Project Root: {project_root}")
    
    # Define required directories
    required_dirs = {
        "saved_models1": "SARIMA Models",
        "saved_models_reg": "Regression Models", 
        "saved_models_clasf": "Classification Models",
        "saved_models_clustering": "Clustering Models",
        ".streamlit": "Streamlit Config",
        "plots": "Plot Output Directory"
    }
    
    # Define required files
    required_files = {
        "finalprj.py": "Main Application",
        "utils.py": "Utility Functions",
        "requirements.txt": "Dependencies",
        ".streamlit/config.toml": "Streamlit Configuration",
        "README.md": "Documentation",
        "QUICKSTART.md": "Quick Start Guide"
    }
    
    all_good = True
    
    # Check directories
    print("\n📂 Checking Directories:")
    print("-" * 60)
    total_models = 0
    
    for dir_name, description in required_dirs.items():
        dir_path = os.path.join(project_root, dir_name)
        exists = os.path.exists(dir_path)
        status = "✅" if exists else "❌"
        
        if dir_name.startswith("saved_models"):
            if exists:
                model_files = [f for f in os.listdir(dir_path) if f.endswith(".pkl")]
                count = len(model_files)
                total_models += count
                print(f"{status} {description:30} ({count} models)")
            else:
                print(f"{status} {description:30} (NOT FOUND)")
                all_good = False
        else:
            print(f"{status} {description:30}")
            if not exists:
                all_good = False
    
    # Check files
    print("\n📄 Checking Files:")
    print("-" * 60)
    
    for file_name, description in required_files.items():
        file_path = os.path.join(project_root, file_name)
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"{status} {description:30} ({file_name})")
        if not exists:
            all_good = False
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Total Models Available: {total_models:,}")
    print("=" * 60)
    
    if all_good:
        print("\n✅ ALL CHECKS PASSED! Dashboard is ready to use.")
        print("\n🚀 To start the dashboard, run:")
        print("   source venv/bin/activate")
        print("   streamlit run finalprj.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please verify the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(verify_setup())
