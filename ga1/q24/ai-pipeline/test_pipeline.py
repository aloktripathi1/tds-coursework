import requests
import json

def test_pipeline():
    """
    Test the pipeline endpoint locally
    """
    
    # API endpoint
    url = "http://localhost:8000/pipeline"
    
    # Request payload
    payload = {
        "email": "your-student-id",
        "source": "JSONPlaceholder Users"
    }
    
    print("🧪 Testing Pipeline Endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")
    
    try:
        # Send POST request
        response = requests.post(url, json=payload, timeout=60)
        
        # Check status
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS! Pipeline executed successfully\n")
            print("="*50)
            print(json.dumps(result, indent=2))
            print("="*50)
            
            # Validate response
            assert "items" in result, "Missing 'items' field"
            assert "notificationSent" in result, "Missing 'notificationSent' field"
            assert "processedAt" in result, "Missing 'processedAt' field"
            assert "errors" in result, "Missing 'errors' field"
            assert len(result["items"]) > 0, "No items processed"
            
            print("\n✅ All validations passed!")
            print(f"✅ Processed {len(result['items'])} items")
            print(f"✅ Notification sent: {result['notificationSent']}")
            
        else:
            print(f"\n❌ FAILED with status {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_pipeline()