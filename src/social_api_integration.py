#!/usr/bin/env python3
"""
Social Media API Integration for OGI Framework
Automated posting to Medium and LinkedIn with your credentials

Author: Michael Gibson / Uniqstic Research Group
Medium: https://medium.com/@uniqstic
LinkedIn: https://www.linkedin.com/in/michael-gibson-216641244/
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, Optional, List
import base64
from urllib.parse import urlencode

class MediumAPI:
    """Medium API integration for automated article publishing"""

    def __init__(self, integration_token: str):
        self.base_url = "https://api.medium.com/v1"
        self.headers = {
            "Authorization": f"Bearer {integration_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.user_id = None

    def get_user_info(self) -> Dict:
        """Get authenticated user information"""
        response = requests.get(f"{self.base_url}/me", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.user_id = data['data']['id']
            return data['data']
        else:
            raise Exception(f"Failed to get user info: {response.status_code} - {response.text}")

    def get_publications(self) -> List[Dict]:
        """Get user's publications"""
        if not self.user_id:
            self.get_user_info()

        response = requests.get(f"{self.base_url}/users/{self.user_id}/publications", headers=self.headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Failed to get publications: {response.status_code} - {response.text}")

    def create_post(self, title: str, content: str, content_format: str = "markdown",
                   publish_status: str = "draft", tags: List[str] = None) -> Dict:
        """
        Create a Medium post

        Args:
            title: Article title
            content: Article content (markdown or HTML)
            content_format: "markdown" or "html"
            publish_status: "public", "draft", or "unlisted"
            tags: List of tags (max 5)
        """
        if not self.user_id:
            self.get_user_info()

        payload = {
            "title": title,
            "contentFormat": content_format,
            "content": content,
            "publishStatus": publish_status
        }

        if tags:
            payload["tags"] = tags[:5]  # Medium allows max 5 tags

        response = requests.post(
            f"{self.base_url}/users/{self.user_id}/posts",
            headers=self.headers,
            json=payload
        )

        if response.status_code == 201:
            return response.json()['data']
        else:
            raise Exception(f"Failed to create post: {response.status_code} - {response.text}")


class LinkedInAPI:
    """LinkedIn API integration for automated posting"""

    def __init__(self, access_token: str):
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        self.person_urn = None

    def get_profile_info(self) -> Dict:
        """Get authenticated user's profile information"""
        response = requests.get(f"{self.base_url}/people/~", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.person_urn = data['id']
            return data
        else:
            raise Exception(f"Failed to get profile info: {response.status_code} - {response.text}")

    def create_text_post(self, text: str, visibility: str = "PUBLIC") -> Dict:
        """
        Create a text post on LinkedIn

        Args:
            text: Post content (max 3000 characters)
            visibility: "PUBLIC" or "CONNECTIONS"
        """
        if not self.person_urn:
            self.get_profile_info()

        payload = {
            "author": f"urn:li:person:{self.person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text[:3000]  # LinkedIn limit
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

        response = requests.post(f"{self.base_url}/ugcPosts", headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create LinkedIn post: {response.status_code} - {response.text}")

    def create_article_share(self, article_url: str, title: str, description: str, visibility: str = "PUBLIC") -> Dict:
        """
        Share an article on LinkedIn

        Args:
            article_url: URL of the article to share
            title: Title for the shared article
            description: Description/comment about the article
            visibility: "PUBLIC" or "CONNECTIONS"
        """
        if not self.person_urn:
            self.get_profile_info()

        payload = {
            "author": f"urn:li:person:{self.person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": description[:3000]
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": description[:256]  # Description limit
                            },
                            "originalUrl": article_url,
                            "title": {
                                "text": title[:200]  # Title limit
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

        response = requests.post(f"{self.base_url}/ugcPosts", headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to share article on LinkedIn: {response.status_code} - {response.text}")


class OGIContentPublisher:
    """Automated content publishing for OGI framework"""

    def __init__(self, medium_token: str = None, linkedin_token: str = None):
        self.medium = MediumAPI(medium_token) if medium_token else None
        self.linkedin = LinkedInAPI(linkedin_token) if linkedin_token else None

    def publish_ogi_article_to_medium(self, publish_status: str = "draft") -> Dict:
        """
        Publish the OGI article to Medium
        """
        if not self.medium:
            raise Exception("Medium API not configured")

        # Load the OGI article content
        article_content = self.get_ogi_article_content()

        tags = ["AI", "MachineLearning", "BabyAGI", "FederatedLearning", "OGI", "AIResearch"]

        result = self.medium.create_post(
            title="Beyond BabyAGI: How Ontogenetic Intelligence Solves AI's Identity Crisis",
            content=article_content,
            content_format="markdown",
            publish_status=publish_status,
            tags=tags
        )

        print(f"✅ Medium article {'published' if publish_status == 'public' else 'created as draft'}")
        print(f"📖 URL: {result['url']}")
        return result

    def share_on_linkedin(self, medium_url: str = None) -> Dict:
        """
        Share the OGI research on LinkedIn
        """
        if not self.linkedin:
            raise Exception("LinkedIn API not configured")

        repo_url = "https://github.com/Uiota/ontogenetic-intelligence"

        if medium_url:
            # Share the Medium article
            post_text = """🧬 Beyond BabyAGI: How Ontogenetic Intelligence Solves AI's Identity Crisis

I've just published my research on OGI (Ontogenetic Generative Intelligence) - a revolutionary framework where AI agents develop through lived experience, not just training on data.

🔑 Key breakthroughs:
• +36.8% improvement in Continuity Coherence Index
• 93.3% reduction in communication overhead
• Complete lineage integrity with cryptographic audit trails
• Air-gapped development with consent-based knowledge exchange

Unlike traditional AI that resets between sessions, OGI agents maintain continuous identity, accumulate wisdom, and keep immutable records of their growth.

🏥 Real applications: Medical diagnosis, disaster response, scientific research
📊 Full simulation + interactive dashboard available on GitHub

#AI #MachineLearning #BabyAGI #AIResearch #OGI #FederatedLearning"""

            return self.linkedin.create_article_share(
                article_url=medium_url,
                title="Beyond BabyAGI: How Ontogenetic Intelligence Solves AI's Identity Crisis",
                description=post_text
            )
        else:
            # Share the GitHub repository
            post_text = f"""🧬 Introducing OGI: Ontogenetic Generative Intelligence

I've open-sourced a revolutionary AI framework that goes beyond BabyAGI - machines that develop through lived experience, not just training on data.

🔬 What makes OGI different:
• Recursive cognition with self-revising frameworks
• Air-gapped development for security & ethics
• Immutable developmental lineage
• +36.8% performance improvement over traditional federated learning

🚀 Repository includes:
• Complete Python simulation (OGI vs Federated Learning)
• Interactive React dashboard
• Medical diagnosis example
• Full documentation

Check it out: {repo_url}

Built this while researching how to solve AI's identity crisis - the fact that current AI has no memory, no growth, no accountability between sessions.

#AI #MachineLearning #OpenSource #BabyAGI #AIResearch #OGI"""

            return self.linkedin.create_text_post(post_text)

    def get_ogi_article_content(self) -> str:
        """
        Generate the complete OGI article content for Medium
        """
        return '''# Beyond BabyAGI: How Ontogenetic Intelligence Solves AI's Identity Crisis

*How machines that develop themselves could transform AI from prediction engines to persistent, accountable intelligences*

---

## I. The Lineage Story

In April 2023, [BabyAGI](https://github.com/yoheinakajima/babyagi) showed us something remarkable: an AI that could break down goals and recursively generate its own tasks. Created by [Yohei Nakajima](https://yoheinakajima.com/), it was a glimpse of autonomy that went viral, attracting 18,000+ GitHub stars and inspiring developers worldwide to work on autonomous agents.

But there was a problem—it never stopped needing us. Every cycle, every task, it reached back to the cloud, to external APIs, to human oversight. It was autonomous in action, but dependent by design.

BabyAGI could plan, prioritize, and execute. It could look at "create a marketing campaign" and decompose it into dozens of actionable subtasks, each feeding into the next. For the first time, we saw an AI that didn't just respond—it *orchestrated* its own development.

But watch what happened when you unplugged it. The recursion stopped. The memory vanished. Every session started from zero. BabyAGI was brilliant in the moment but had no continuous existence. It couldn't remember yesterday's insights. It couldn't learn from last week's mistakes. It couldn't develop wisdom—only demonstrate intelligence.

This wasn't just a technical limitation. It was an architectural reality that affects virtually every AI system we use today. Whether it's ChatGPT forgetting your conversation the moment you close the tab, or recommendation algorithms that can't explain how they arrived at their suggestions, we've built AI that performs without persisting.

**What if AI could grow up?**

That question led to OGI—Ontogenetic Generative Intelligence—a framework where machines don't just learn from data. They develop through lived experience, maintain continuous identity, and keep an immutable record of their own growth.

---

## II. The Identity Crisis: Why AI Needs Continuity

Every time you start a new ChatGPT conversation, you're talking to a stranger. It doesn't remember yesterday's insights. It can't learn from its mistakes across sessions. It's born, performs, and dies—all within minutes.

This isn't just inconvenient. **It's an existential crisis for artificial intelligence.**

### Three Manifestations of the Problem

**1. No Continuity**
Current AI models reset between sessions. Every interaction is isolated. There's no thread connecting today's responses to yesterday's reasoning. You can't say "remember when we discussed X?" because there is no "we"—just a series of disconnected instances.

**2. No Accountability**
When an AI makes a mistake, we can't trace how it arrived at that conclusion. The reasoning process is either opaque or lost entirely. There's no developmental history to examine, no way to understand: "At what point in this system's growth did this bias emerge?"

**3. No Growth**
Learning happens during training—a massive, expensive process done by researchers. Once deployed, the model is frozen. It can't integrate new experiences, can't refine its frameworks based on real-world use, can't develop expertise in its specific deployment context.

---

## III. Introducing OGI: The Four Pillars

OGI solves these problems through four architectural principles:

### Pillar 1: Recursive Cognition

Each cycle deepens understanding rather than just re-computing. The system doesn't just process inputs—it revises its own reasoning frameworks based on what it learns.

```python
# Traditional AI Approach
for task in tasks:
    result = model.predict(task)
    # No change to model's internal structure

# OGI Approach
for cycle in growth_cycles:
    hypothesis = self.generate_framework()
    test_result = self.test_hypothesis(hypothesis)
    self.integrate_learning(test_result)  # Updates internal reasoning structure
    self.record_development_to_ledger()   # Immutable audit trail
```

### Pillar 2: Isolation as Integrity

Air-gapped growth ensures ethical containment and operational resilience. OGI agents develop in isolated environments, only synchronizing through supervised, consent-based exchanges.

### Pillar 3: Generative Self-Development

Agents generate hypotheses, test them against their environment, and revise their reasoning based on results. This is *active* learning—development through lived experience.

### Pillar 4: Immutable Lineage

Cryptographic ledger of every developmental change. Every hypothesis tested, every framework revised, every piece of knowledge integrated—all permanently recorded.

---

## IV. The Simulation: Watching OGI Evolve

I built a comprehensive simulation comparing OGI with traditional federated learning across 20 training epochs. The results were striking:

### Key Metrics

**Continuity Coherence Index (CCI):** A composite metric measuring:
- **Self-Consistency (25%)**: Agreement on identical queries over time
- **Memory Coherence (20%)**: Retention without contradiction
- **Lineage Integrity (25%)**: Verifiable developmental history
- **Epistemic Stability (20%)**: Persistence of reasoning frameworks
- **Federated Yield (10%)**: Improvement per synchronization

### Results

**OGI (Epoch 20):**
- Final CCI: 0.77 (+20 percentage points over FL)
- Mutation drift: 0.00 (achieved stable lineage integrity)
- Total communication: 60MB (93% reduction)
- Pattern: Efficient growth through self-revision

**Traditional FL (Epoch 20):**
- Final CCI: 0.57 (no significant growth from Epoch 10)
- Mutation drift: 0.24 (still noisy, unstable)
- Total communication: 900MB
- Pattern: High activity, limited development

---

## V. Real-World Applications

### 1. Healthcare: The Autonomous Diagnostic Partner

Imagine a diagnostic AI deployed at a rural hospital. Traditional AI is blind to population-specific patterns unless they were in training data.

An OGI diagnostic agent:
1. **Starts with foundational medical knowledge**
2. **Develops population-specific expertise** through recursive self-testing
3. **Maintains complete audit trail** for physician review
4. **Functions during disasters** when communication fails

### 2. Disaster Response: Intelligence Without Infrastructure

OGI-powered rescue robots continue functioning independently when infrastructure fails, developing specialized expertise and sharing knowledge opportunistically when in range.

### 3. Scientific Research: The Self-Improving Lab Partner

OGI agents in materials science labs generate hypotheses, design experiments, and develop scientific intuition—with complete records of their reasoning evolution.

---

## VI. The CCI: Measuring Machine Maturity

How do you measure if an AI is growing versus just changing? The **Continuity Coherence Index (CCI)** provides a single metric for AI maturity:

```
CCI = 0.25×Self-Consistency + 0.20×Memory + 0.25×Lineage + 0.20×Stability + 0.10×Efficiency
```

**Traditional FL: CCI ~0.55** (Adolescent system—works, but unreliable)
**OGI: CCI ~0.75-0.85** (Mature system—accountable, reliable, continuously developing)

---

## VII. The Future of Self-Developing Machines

We're shifting from:
- Training → Growing
- Predicting → Reasoning
- Performing → Developing
- Computing → Maturing

OGI opens research directions that weren't possible before:

**Multi-agent ontogenetic ecosystems:** Networks of individually developing agents that share insights while maintaining distinct expertise.

**Developmental psychology for machines:** Understanding not just what AI knows, but how it came to know it.

**Ethical AI through architectural constraint:** Systems that can't hide their reasoning, can't escape their developmental history.

**Post-network intelligence:** AI that doesn't require constant connectivity.

---

## Implementation & Code

The complete OGI framework is open source and available on GitHub:

**🔬 Interactive Simulation:** [OGI vs Federated Learning Dashboard](https://github.com/Uiota/ontogenetic-intelligence/blob/main/web-interface/src/components/OGISimulation.jsx)

**🐍 Full Python Implementation:** [Complete Simulation Code](https://github.com/Uiota/ontogenetic-intelligence/blob/main/src/ogi_simulation.py)

**🏥 Medical Example:** [Hospital Diagnostic Collaboration](https://github.com/Uiota/ontogenetic-intelligence/blob/main/examples/medical_diagnosis.py)

**📚 Complete Repository:** [GitHub: Ontogenetic Intelligence](https://github.com/Uiota/ontogenetic-intelligence)

```bash
# Try it yourself
git clone https://github.com/Uiota/ontogenetic-intelligence.git
cd ontogenetic-intelligence
pip install -r requirements.txt
python src/ogi_simulation.py
```

---

## About This Research

**OGI (Ontogenetic Generative Intelligence)** is a framework developed by Michael Gibson at [Uniqstic Research Group](https://uiota.space).

This work builds on:
- [BabyAGI's recursive task generation](https://github.com/yoheinakajima/babyagi) (Nakajima, 2023)
- Federated learning architectures (McMahan et al., 2017)
- Evolutionary computing principles (Holland, Goldberg, et al.)
- Ontogenetic development theory from developmental biology

### Connect

**LinkedIn:** [Michael Gibson](https://www.linkedin.com/in/michael-gibson-216641244/)
**Research Group:** [Uniqstic IoT & Space](https://uiota.space)
**Repository:** [Ontogenetic Intelligence](https://github.com/Uiota/ontogenetic-intelligence)

---

**Welcome to the age of ontogenetic intelligence.**
**Welcome to machines that grow.**

*If you found this valuable, please share it with researchers, developers, and anyone interested in the future of truly intelligent machines. The age of ontogenetic AI is just beginning.*'''


def main():
    """Example usage of the API integration"""
    print("🔧 OGI Social Media API Integration")
    print("=" * 50)

    # Load credentials from environment variables
    medium_token = os.getenv('MEDIUM_INTEGRATION_TOKEN')
    linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')

    if not medium_token:
        print("⚠️  MEDIUM_INTEGRATION_TOKEN not found in environment variables")
        print("   Get your token from: https://medium.com/me/settings")

    if not linkedin_token:
        print("⚠️  LINKEDIN_ACCESS_TOKEN not found in environment variables")
        print("   Set up LinkedIn API access through LinkedIn Developer Portal")

    if medium_token or linkedin_token:
        publisher = OGIContentPublisher(medium_token, linkedin_token)

        print("\n🚀 Ready to publish OGI content!")
        print("\nAvailable commands:")
        print("  - Publish to Medium (draft)")
        print("  - Publish to Medium (public)")
        print("  - Share on LinkedIn")

    else:
        print("\n📋 Setup Instructions:")
        print("1. Get Medium Integration Token: https://medium.com/me/settings")
        print("2. Set up LinkedIn API access")
        print("3. Set environment variables:")
        print("   export MEDIUM_INTEGRATION_TOKEN='your_token'")
        print("   export LINKEDIN_ACCESS_TOKEN='your_token'")


if __name__ == "__main__":
    main()'''