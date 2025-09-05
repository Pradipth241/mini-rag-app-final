# test_qdrant_connection.py

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

print("Attempting to connect to Qdrant...")

try:
    load_dotenv()
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        print("❌ ERROR: QDRANT_URL or QDRANT_API_KEY not found in .env file.")
    else:
        print(f"Connecting to: {qdrant_url}")

        # Initialize the client (this is where the connection happens)
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        # If the line above didn't fail, the connection is likely good.
        # Let's try a simple command.
        client.get_collections()

        print("\n✅ SUCCESS: Connection to Qdrant was successful!")

except Exception as e:
    print(f"\n❌ FAILED: Could not connect to Qdrant.")
    print(f"   Error: {e}")