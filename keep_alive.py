"""
Keep-alive script for Hugging Face Spaces or other deployments.
This script pings the application health endpoint periodically to prevent sleeping.
"""
import time
import requests
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('keep_alive.log')
    ]
)

def ping_server(url: str, interval_hours: float = 12.0):
    """
    Ping the server periodically to keep it alive.
    
    Args:
        url: The URL to health check endpoint
        interval_hours: Time between pings in hours
    """
    check_url = f"{url}/health" if not url.endswith('/health') else url
    interval_seconds = interval_hours * 3600
    
    logging.info(f"Starting keep-alive monitor for {check_url}")
    logging.info(f"Ping interval: {interval_hours} hours")
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"Initiating ping at {current_time}")
            
            response = requests.get(check_url, timeout=30)
            
            if response.status_code == 200:
                logging.info(f"Success: Server is active. Status: {response.status_code}")
                logging.info(f"Response: {response.json()}")
            else:
                logging.warning(f"Warning: Server returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error pinging server: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            
        logging.info(f"Sleeping for {interval_hours} hours...")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # Default URL - change this to your deployed URL
    APP_URL = "https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME"
    
    print("Stock Analysis Keep-Alive Script")
    print("--------------------------------")
    
    if "YOUR_USERNAME" in APP_URL:
        user_url = input("Enter your deployed application URL (e.g., https://your-app.hf.space): ").strip()
        if user_url:
            APP_URL = user_url
            
    ping_server(APP_URL)
