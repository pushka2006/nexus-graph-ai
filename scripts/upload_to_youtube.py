"""
NEXUS GRAPH AI - Automated YouTube Video Uploader
=================================================
Uploads video files to YouTube using the official Google YouTube Data API v3.

Requirements:
    pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

Setup:
    1. Go to Google Cloud Console (https://console.cloud.google.com/)
    2. Enable 'YouTube Data API v3'.
    3. Create OAuth 2.0 Client ID (Application type: Desktop App).
    4. Download JSON credentials and save as 'client_secrets.json' in this folder.
    5. Run:
       python scripts/upload_to_youtube.py --file path/to/demo.mp4 --privacy unlisted
"""

import argparse
import os
import sys
import time
from typing import List

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("\n[ERROR] Missing required libraries. Please install them by running:")
    print("pip install google-api-python-client google-auth-oauthlib google-auth-httplib2\n")
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
DEFAULT_CLIENT_SECRETS_FILE = "client_secrets.json"

DEFAULT_TITLE = "NEXUS GRAPH AI: Autonomous Company Intelligence with FalkorDB & Multi-Agent Coordination"
DEFAULT_DESCRIPTION = """NEXUS GRAPH AI is an enterprise-grade multi-agent autonomous intelligence platform powered by a live FalkorDB graph database and local instruction-tuned LLMs (Qwen2.5).

GitHub Repository: https://github.com/pushka2006/nexus-graph-ai
FalkorDB: https://www.falkordb.com/

TIMESTAMPS:
0:00 - Introduction & The Limits of Vector RAG
0:45 - High-Level Architecture (FalkorDB + Qwen 2.5 + Next.js 16)
1:30 - Scene 1: Company Brain Q&A & Document Citations
3:00 - Scene 2: Security Graph & Multi-Hop Anomaly Correlation
4:30 - Scene 3: Multi-Tier Persistent Memory & Cross-Session Recall
5:45 - Scene 4: Multi-Agent Orchestration & Concurrency Leases
7:00 - Scene 5: MCP Tool Execution & Human Approval Gate
8:15 - Scene 6: Interactive 3D Knowledge Graph Explorer
9:30 - Empirical Evaluation & Benchmarks (100% Pass Rate)

#FalkorDB #GraphDatabase #MultiAgent #AI #NextJS #FastAPI #Qwen #OpenSource
"""

DEFAULT_TAGS = [
    "FalkorDB",
    "Graph Database",
    "Multi-Agent AI",
    "Knowledge Graph",
    "Graph RAG",
    "Autonomous Agents",
    "FastAPI",
    "NextJS",
    "React 19",
    "Cypher Query",
    "Qwen",
    "Artificial Intelligence",
    "LLM"
]

def get_authenticated_service(client_secrets_file: str):
    if not os.path.exists(client_secrets_file):
        print(f"\n[ERROR] Client secrets file not found at: '{client_secrets_file}'")
        print("Please obtain 'client_secrets.json' from Google Cloud Console and place it in the working directory.")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

def upload_video(
    youtube,
    file_path: str,
    title: str,
    description: str,
    tags: List[str],
    privacy_status: str = "unlisted",
    category_id: str = "28"  # 28 = Science & Technology
):
    if not os.path.exists(file_path):
        print(f"\n[ERROR] Video file not found: {file_path}")
        sys.exit(1)

    file_size = os.path.getsize(file_path) / (1024 * 1024)
    print(f"\n[INFO] Starting upload for: {file_path} ({file_size:.2f} MB)")
    print(f"[INFO] Title: {title}")
    print(f"[INFO] Privacy: {privacy_status}")

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(file_path, chunksize=1024 * 1024 * 10, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"[UPLOADING] {progress}% complete...")

    video_id = response.get("id")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print("\n" + "=" * 60)
    print("SUCCESS: Video uploaded successfully!")
    print(f"Video URL: {video_url}")
    print(f"YouTube Studio Edit: https://studio.youtube.com/video/{video_id}/edit")
    print("=" * 60 + "\n")
    return video_url

def main():
    parser = argparse.ArgumentParser(description="Upload NEXUS GRAPH AI demo video to YouTube.")
    parser.add_argument("--file", "-f", required=True, help="Path to the video file (.mp4, .webm, etc.)")
    parser.add_argument("--title", "-t", default=DEFAULT_TITLE, help="Video title")
    parser.add_argument("--secrets", "-s", default=DEFAULT_CLIENT_SECRETS_FILE, help="Path to client_secrets.json")
    parser.add_argument("--privacy", "-p", choices=["public", "unlisted", "private"], default="unlisted", help="Privacy status")
    
    args = parser.parse_args()

    youtube = get_authenticated_service(args.secrets)
    upload_video(
        youtube=youtube,
        file_path=args.file,
        title=args.title,
        description=DEFAULT_DESCRIPTION,
        tags=DEFAULT_TAGS,
        privacy_status=args.privacy
    )

if __name__ == "__main__":
    main()
