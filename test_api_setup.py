#!/usr/bin/env python3
"""
Test API Setup Script
Verify your Medium and LinkedIn credentials are working

Usage:
    python test_api_setup.py
"""

import os
import sys

def test_imports():
    """Test if required packages are available"""
    try:
        import requests
        print("✅ requests package available")
    except ImportError:
        print("❌ requests package missing - install with: pip install requests")
        return False

    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv package available")
    except ImportError:
        print("❌ python-dotenv package missing - install with: pip install python-dotenv")
        return False

    return True

def test_medium_token(token):
    """Test Medium API token"""
    import requests

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get("https://api.medium.com/v1/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            user_data = data['data']
            print(f"✅ Medium API working!")
            print(f"   Username: @{user_data['username']}")
            print(f"   Name: {user_data['name']}")
            print(f"   URL: {user_data['url']}")
            return True
        else:
            print(f"❌ Medium API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Medium API connection failed: {e}")
        return False

def test_linkedin_token(token):
    """Test LinkedIn API token"""
    import requests

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get("https://api.linkedin.com/v2/people/~", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ LinkedIn API working!")
            print(f"   User ID: {data['id']}")
            if 'localizedFirstName' in data:
                print(f"   Name: {data['localizedFirstName']} {data.get('localizedLastName', '')}")
            return True
        else:
            print(f"❌ LinkedIn API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ LinkedIn API connection failed: {e}")
        return False

def main():
    print("🧬 OGI API Setup Test")
    print("=" * 50)

    # Test package imports
    if not test_imports():
        print("\n📦 Install missing packages:")
        print("   pip install requests python-dotenv")
        print("   # Or create virtual environment:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install requests python-dotenv")
        return

    # Load environment variables
    try:
        from dotenv import load_dotenv
        env_path = '.env'
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✅ Loaded {env_path}")
        else:
            print(f"⚠️  No .env file found")
            print("   Copy .env.example to .env and add your tokens")
    except:
        print("⚠️  Loading .env manually...")

    # Test Medium API
    medium_token = os.getenv('MEDIUM_INTEGRATION_TOKEN')
    if medium_token:
        print(f"\n📝 Testing Medium API...")
        test_medium_token(medium_token)
    else:
        print(f"\n📝 Medium token not found")
        print("   Get your token from: https://medium.com/me/settings")
        print("   Add to .env: MEDIUM_INTEGRATION_TOKEN=your_token_here")

    # Test LinkedIn API
    linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    if linkedin_token:
        print(f"\n🔗 Testing LinkedIn API...")
        test_linkedin_token(linkedin_token)
    else:
        print(f"\n🔗 LinkedIn token not found")
        print("   Get your token from: https://www.linkedin.com/developers/")
        print("   Add to .env: LINKEDIN_ACCESS_TOKEN=your_token_here")

    print(f"\n🎯 Next Steps:")
    print("1. Get your API tokens (see links above)")
    print("2. Copy .env.example to .env")
    print("3. Add your tokens to .env")
    print("4. Run: python scripts/publish_ogi_content.py --help")

if __name__ == "__main__":
    main()