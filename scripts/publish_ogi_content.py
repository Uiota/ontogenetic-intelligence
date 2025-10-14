#!/usr/bin/env python3
"""
OGI Content Publishing Script
Automated posting to Medium and LinkedIn with your credentials

Usage:
    python scripts/publish_ogi_content.py --medium-draft
    python scripts/publish_ogi_content.py --medium-public
    python scripts/publish_ogi_content.py --linkedin
    python scripts/publish_ogi_content.py --all

Author: Michael Gibson / Uniqstic Research Group
"""

import sys
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from social_api_integration import OGIContentPublisher

def load_credentials():
    """Load credentials from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded credentials from {env_path}")
    else:
        print(f"⚠️  No .env file found at {env_path}")
        print("   Copy .env.example to .env and add your credentials")
        return None, None

    medium_token = os.getenv('MEDIUM_INTEGRATION_TOKEN')
    linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')

    return medium_token, linkedin_token

def publish_to_medium(publisher, public=False):
    """Publish OGI article to Medium"""
    status = "public" if public else "draft"

    print(f"\n📝 Publishing to Medium as {status}...")

    try:
        result = publisher.publish_ogi_article_to_medium(publish_status=status)
        print(f"✅ Medium article {'published' if public else 'saved as draft'}!")
        print(f"📖 URL: {result['url']}")
        print(f"📊 ID: {result['id']}")
        return result['url']
    except Exception as e:
        print(f"❌ Failed to publish to Medium: {e}")
        return None

def share_on_linkedin(publisher, medium_url=None):
    """Share OGI content on LinkedIn"""
    print(f"\n🔗 Sharing on LinkedIn...")

    try:
        result = publisher.share_on_linkedin(medium_url=medium_url)
        print(f"✅ Shared on LinkedIn!")
        print(f"📊 Post ID: {result.get('id', 'Unknown')}")
        return result
    except Exception as e:
        print(f"❌ Failed to share on LinkedIn: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Publish OGI content to social media')
    parser.add_argument('--medium-draft', action='store_true', help='Publish to Medium as draft')
    parser.add_argument('--medium-public', action='store_true', help='Publish to Medium publicly')
    parser.add_argument('--linkedin', action='store_true', help='Share on LinkedIn')
    parser.add_argument('--all', action='store_true', help='Publish to Medium (public) and share on LinkedIn')

    args = parser.parse_args()

    if not any([args.medium_draft, args.medium_public, args.linkedin, args.all]):
        parser.print_help()
        return

    print("🧬 OGI Content Publisher")
    print("=" * 50)

    # Load credentials
    medium_token, linkedin_token = load_credentials()

    if not medium_token and not linkedin_token:
        print("\n❌ No API credentials found!")
        print("\n📋 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Get Medium token: https://medium.com/me/settings")
        print("3. Get LinkedIn token: https://www.linkedin.com/developers/")
        print("4. Add tokens to .env file")
        return

    # Initialize publisher
    publisher = OGIContentPublisher(medium_token, linkedin_token)

    medium_url = None

    # Execute requested actions
    if args.all:
        # Publish to Medium first, then share on LinkedIn
        if medium_token:
            medium_url = publish_to_medium(publisher, public=True)
        if linkedin_token:
            share_on_linkedin(publisher, medium_url)
    else:
        if args.medium_draft and medium_token:
            medium_url = publish_to_medium(publisher, public=False)

        if args.medium_public and medium_token:
            medium_url = publish_to_medium(publisher, public=True)

        if args.linkedin and linkedin_token:
            share_on_linkedin(publisher, medium_url)

    print(f"\n🎉 Publishing complete!")

    if medium_url:
        print(f"📰 Medium: {medium_url}")

    print(f"🔗 GitHub: https://github.com/Uiota/ontogenetic-intelligence")
    print(f"👤 LinkedIn: https://www.linkedin.com/in/michael-gibson-216641244/")

if __name__ == "__main__":
    main()