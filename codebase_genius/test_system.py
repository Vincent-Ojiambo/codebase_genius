#!/usr/bin/env python3
"""
Test script for Codebase Genius
Tests the system with sample repositories and validates functionality.
"""

import requests
import json
import time
import sys
import os

class CodebaseGeniusTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_repos = [
            # Small, well-structured repositories for testing
            "https://github.com/octocat/Hello-World",
            "https://github.com/jasonrudolph/keyboard",
            "https://github.com/github/gitignore"
        ]

    def test_api_status(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.base_url}/walker/api/get_status")
            if response.status_code == 200:
                print("✓ API status check passed")
                return True
            else:
                print(f"✗ API status check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ API connection failed: {e}")
            return False

    def test_documentation_generation(self, repo_url):
        """Test documentation generation for a repository"""
        try:
            print(f"Testing documentation generation for: {repo_url}")

            payload = {"repo_url": repo_url}
            response = requests.post(
                f"{self.base_url}/walker/api/generate_docs",
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✓ Documentation generation successful: {result}")

                # Check if output was created
                self.check_output_exists(repo_url)
                return True
            else:
                print(f"✗ Documentation generation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"✗ Documentation generation error: {e}")
            return False

    def check_output_exists(self, repo_url):
        """Check if documentation output was created"""
        repo_name = repo_url.split('/')[-1]
        output_path = f"./outputs/{repo_name}/README.md"

        if os.path.exists(output_path):
            print(f"✓ Output file created: {output_path}")

            # Show file size and first few lines
            size = os.path.getsize(output_path)
            print(f"  File size: {size} bytes")

            with open(output_path, 'r') as f:
                lines = f.readlines()[:5]
                print("  First few lines:")
                for line in lines:
                    print(f"    {line.strip()}")
        else:
            print(f"✗ Output file not found: {output_path}")

    def test_list_outputs(self):
        """Test listing available outputs"""
        try:
            response = requests.get(f"{self.base_url}/walker/api/list_outputs")
            if response.status_code == 200:
                print("✓ List outputs endpoint working")
                print(f"Available outputs: {response.text}")
                return True
            else:
                print(f"✗ List outputs failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ List outputs error: {e}")
            return False

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 Starting Codebase Genius Test Suite\n")

        # Test 1: API Status
        print("1. Testing API Status...")
        if not self.test_api_status():
            print("❌ API not available. Please start the Jac server first:")
            print("   jac serve main.jac")
            return False

        print()

        # Test 2: List Outputs (should be empty initially)
        print("2. Testing List Outputs...")
        self.test_list_outputs()
        print()

        # Test 3: Documentation Generation
        print("3. Testing Documentation Generation...")
        test_repo = self.test_repos[0]  # Use first repo for testing

        start_time = time.time()
        success = self.test_documentation_generation(test_repo)
        end_time = time.time()

        if success:
            print(f"✓ Documentation generation completed in {end_time - start_time:.2f} seconds")
        else:
            print("✗ Documentation generation failed")

        print()

        # Test 4: List Outputs (should have content now)
        print("4. Testing List Outputs (after generation)...")
        self.test_list_outputs()
        print()

        # Summary
        print("📊 Test Summary:")
        print(f"Repository tested: {test_repo}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")

        if success:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed")
            return False

def main():
    """Main test function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"

    print(f"Testing Codebase Genius at: {base_url}")

    tester = CodebaseGeniusTester(base_url)
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
