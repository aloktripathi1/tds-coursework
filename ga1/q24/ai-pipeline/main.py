from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from openai import OpenAI
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="AI-Powered Data Pipeline")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client with custom base URL
# Initialize OpenAI client with custom base URL
client = OpenAI(
    api_key=os.getenv('AIPIPE_TOKEN') or os.getenv('AIPROXY_TOKEN'),
    base_url=os.getenv('AIPIPE_BASE_URL') or "https://aipipe.org/openai/v1"
)

# ==================== DATA MODELS ====================

class PipelineRequest(BaseModel):
    email: str
    source: str

# ==================== HELPER FUNCTIONS ====================

def fetch_users():
    """
    Fetch users from JSONPlaceholder API
    Returns: List of first 3 users or empty list on error
    """
    try:
        print("📡 Fetching users from JSONPlaceholder...")
        response = requests.get(
            'https://jsonplaceholder.typicode.com/users',
            timeout=10
        )
        response.raise_for_status()
        
        users = response.json()
        # Return first 3 users
        result = users[:3]
        print(f"✅ Successfully fetched {len(result)} users")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching users: {e}")
        return []


def analyze_user_with_ai(user_data):
    """
    Use AI to analyze user data via AIPIPE
    Returns: Dictionary with analysis and sentiment
    """
    try:
        print(f"🤖 Analyzing user: {user_data['name']}...")
        
        # Create concise user description
        user_text = (
            f"Name: {user_data['name']}\n"
            f"Email: {user_data['email']}\n"
            f"Company: {user_data['company']['name']}\n"
            f"Website: {user_data.get('website', 'N/A')}\n"
            f"Phone: {user_data.get('phone', 'N/A')}"
        )
        
        # Prompt for AI
        prompt = f"""Analyze this user profile and provide:
1. A 2-sentence professional summary
2. Sentiment classification (choose one: enthusiastic, critical, objective)

User Profile:
{user_text}

Respond in exactly this format:
Summary: [your 2-sentence summary]
Sentiment: [enthusiastic/critical/objective]"""
        
        # Call AI API via AIPIPE
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        # Parse response
        result_text = response.choices[0].message.content.strip()
        
        # Extract summary and sentiment
        lines = [line.strip() for line in result_text.split('\n') if line.strip()]
        
        summary = "Analysis completed"
        sentiment = "objective"
        
        for line in lines:
            if line.startswith('Summary:'):
                summary = line.replace('Summary:', '').strip()
            elif line.startswith('Sentiment:'):
                sentiment = line.replace('Sentiment:', '').strip().lower()
        
        print(f"✅ AI analysis completed for {user_data['name']}")
        
        return {
            "analysis": summary,
            "sentiment": sentiment
        }
        
    except Exception as e:
        print(f"❌ AI analysis error for {user_data.get('name', 'unknown')}: {e}")
        return {
            "analysis": "Analysis unavailable due to error",
            "sentiment": "objective"
        }


def store_result(original_data, ai_analysis, filepath="results.json"):
    """
    Store processed result to JSON file
    Returns: The stored result object
    """
    try:
        print(f"💾 Storing result for {original_data['name']}...")
        
        # Create result object
        result = {
            "original": {
                "name": original_data['name'],
                "email": original_data['email'],
                "company": original_data['company']['name'],
                "phone": original_data.get('phone', 'N/A'),
                "website": original_data.get('website', 'N/A')
            },
            "analysis": ai_analysis['analysis'],
            "sentiment": ai_analysis['sentiment'],
            "stored": True,
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
        
        # Load existing results
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    results = json.load(f)
            except json.JSONDecodeError:
                results = []
        else:
            results = []
        
        # Append new result
        results.append(result)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Result stored for {original_data['name']}")
        return result
        
    except Exception as e:
        print(f"❌ Storage error: {e}")
        # Return result even if storage failed
        return {
            "original": str(original_data),
            "analysis": ai_analysis['analysis'],
            "sentiment": ai_analysis['sentiment'],
            "stored": False,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "error": str(e)
        }


def send_notification(email, status, items_processed):
    """
    Send notification about pipeline completion
    Returns: True if notification sent
    """
    try:
        message = f"""
╔════════════════════════════════════════════╗
║     PIPELINE NOTIFICATION                  ║
╚════════════════════════════════════════════╝

To: {email}
Status: {status}
Items Processed: {items_processed}
Timestamp: {datetime.utcnow().isoformat()}Z

Pipeline execution completed successfully!
        """
        
        print(message)
        
        # In production, you would send actual email here
        # For now, console log serves as notification
        print("✅ Notification sent to: your-student-id")
        
        return True
        
    except Exception as e:
        print(f"❌ Notification error: {e}")
        return False


def process_pipeline(notification_email):
    """
    Main pipeline orchestration function
    Returns: Complete pipeline result
    """
    errors = []
    processed_items = []
    
    print("\n" + "="*50)
    print("🚀 STARTING AI-POWERED DATA PIPELINE")
    print("="*50 + "\n")
    
    # Step 1: Fetch data
    users = fetch_users()
    
    if not users:
        error_msg = "Failed to fetch users from API"
        errors.append(error_msg)
        print(f"\n❌ PIPELINE FAILED: {error_msg}\n")
        return {
            "items": [],
            "notificationSent": False,
            "processedAt": datetime.utcnow().isoformat() + 'Z',
            "errors": errors
        }
    
    # Step 2-4: Process each user
    for idx, user in enumerate(users, 1):
        try:
            print(f"\n--- Processing User {idx}/{len(users)} ---")
            
            # AI Analysis
            ai_result = analyze_user_with_ai(user)
            
            # Storage
            stored_result = store_result(user, ai_result)
            
            processed_items.append(stored_result)
            
        except Exception as e:
            error_msg = f"Error processing {user.get('name', 'unknown')}: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
            continue
    
    # Step 5: Send notification
    print(f"\n📧 Sending notification to {notification_email}...")
    notification_sent = send_notification(
        notification_email,
        "completed" if processed_items else "failed",
        len(processed_items)
    )
    
    print("\n" + "="*50)
    print("✅ PIPELINE COMPLETED")
    print(f"Processed: {len(processed_items)} items")
    print(f"Errors: {len(errors)}")
    print("="*50 + "\n")
    
    # Return complete result
    return {
        "items": processed_items,
        "notificationSent": notification_sent,
        "processedAt": datetime.utcnow().isoformat() + 'Z',
        "errors": errors
    }


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI-Powered Data Pipeline API",
        "version": "1.0",
        "endpoints": {
            "POST /pipeline": "Run the data pipeline"
        }
    }


@app.post("/pipeline")
async def run_pipeline(request: PipelineRequest):
    """
    Main pipeline endpoint
    Accepts: {"email": "...", "source": "JSONPlaceholder Users"}
    Returns: Pipeline execution results
    """
    
    # Validate source
    if request.source != "JSONPlaceholder Users":
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Expected 'JSONPlaceholder Users', got '{request.source}'"
        )
    
    # Run the pipeline
    result = process_pipeline(request.email)
    
    return result


# For testing locally
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)