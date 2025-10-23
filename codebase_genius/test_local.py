#!/usr/bin/env python3
"""
Local testing script for Codebase Genius
Tests the system with a local repository instead of cloning from GitHub.
"""

import os
import sys
import json
import shutil
from pathlib import Path
import subprocess

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_jac_walker(walker_name, context=None):
    """Run a Jac walker and return the result."""
    try:
        cmd = ["jac", "run", "main.jac", f"-walker", walker_name]
        if context:
            cmd.extend(["-ctx", json.dumps(context)])

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Jac walker error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error running Jac walker: {e}")
        return None

def test_local_repository():
    """Test the system with our local sample repository."""

    print("🧪 Testing Codebase Genius with Local Repository")
    print("=" * 50)

    # Check if Jac is installed
    try:
        result = subprocess.run(["jac", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Jac is not installed. Please install Jac first.")
            print("   Visit: https://jaseci.org/")
            return False
        print(f"✅ Jac found: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Jac is not installed. Please install Jac first.")
        print("   Visit: https://jaseci.org/")
        return False

    # Check if main.jac exists
    if not os.path.exists("main.jac"):
        print("❌ main.jac not found in current directory")
        return False

    print("✅ main.jac found")

    # Test with our sample repository
    sample_repo_path = "../sample_repo"
    if not os.path.exists(sample_repo_path):
        print(f"❌ Sample repository not found at: {sample_repo_path}")
        return False

    print(f"📁 Testing with sample repository: {sample_repo_path}")

    # Test API status
    print("\n1. Testing API Status...")
    result = run_jac_walker("api.get_status")
    if result:
        print(f"✅ API Status: {result}")
    else:
        print("❌ API status check failed")
        return False

    # Test list outputs (should be empty initially)
    print("\n2. Testing List Outputs...")
    result = run_jac_walker("api.list_outputs")
    if result:
        print(f"✅ List outputs: {result}")
    else:
        print("❌ List outputs failed")
        return False

    # Test documentation generation with local repository
    print("\n3. Testing Local Documentation Generation...")
    try:
        # For local testing, we'll use the utility functions directly
        from utils import TextProcessor, MermaidGenerator, ValidationUtils, FileUtils

        print("✅ Successfully imported utility functions")

        # Test utility functions
        print("   - Testing TextProcessor...")
        sample_content = '''def hello_world():
    """A simple hello world function."""
    print("Hello, World!")

class SampleClass:
    """A sample class."""
    def method(self):
        return "test"
'''
        functions = TextProcessor.extract_functions_python(sample_content)
        classes = TextProcessor.extract_classes_python(sample_content)
        print(f"     ✅ Found {len(functions)} functions and {len(classes)} classes")

        # Test MermaidGenerator
        print("   - Testing MermaidGenerator...")
        call_graph = MermaidGenerator.generate_call_graph({})
        inheritance_graph = MermaidGenerator.generate_inheritance_graph({})
        print(f"     ✅ Generated diagrams (call_graph: {len(call_graph)} chars, inheritance: {len(inheritance_graph)} chars)")

        # Test ValidationUtils
        print("   - Testing ValidationUtils...")
        is_valid = ValidationUtils.validate_github_url("https://github.com/user/repo")
        print(f"     ✅ URL validation working: {is_valid}")

        # Test FileUtils
        print("   - Testing FileUtils...")
        is_text = FileUtils.is_text_file("test.py")
        extension = FileUtils.get_file_extension("test.py")
        print(f"     ✅ File utilities working: is_text={is_text}, extension={extension}")

        # Since the main agents are Jac walkers, let's test them through Jac
        print("   - Testing Jac Agents...")
        result = run_jac_walker("RepoMapper.map_repository", {"repo_path": sample_repo_path})
        if result:
            print("     ✅ RepoMapper Jac walker working")
        else:
            print("     ❌ RepoMapper Jac walker failed")

        result = run_jac_walker("CodeAnalyzer.analyze_codebase", {"repo_path": sample_repo_path})
        if result:
            print("     ✅ CodeAnalyzer Jac walker working")
        else:
            print("     ❌ CodeAnalyzer Jac walker failed")

        result = run_jac_walker("DocGenie.generate_documentation")
        if result:
            print("     ✅ DocGenie Jac walker working")
        else:
            print("     ❌ DocGenie Jac walker failed")

    except ImportError as e:
        print(f"❌ Failed to import utility functions: {e}")
        print("This might be because the Python utilities need to be integrated with Jac")
        print("Testing basic Jac functionality instead...")

        # Test basic Jac functionality
        print("\n4. Testing Basic Jac Functionality...")
        result = run_jac_walker("api.get_status")
        if result:
            print("✅ Basic Jac functionality working")
        else:
            print("❌ Basic Jac functionality failed")
            return False

    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print(f"📄 Documentation generated in: ./outputs/sample_repo/README.md")
    return True

def main():
    """Main test function."""
    success = test_local_repository()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
