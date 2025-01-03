import requests
import json
import os
import time

def get_activities(limit=100):
    activities = []
    base_url = "http://www.boredapi.com/api/activity/"
    
    print(f"Searching for {limit} activities...")
    
    for i in range(limit):
        max_retries = 3
        retries = 0
        
        while retries < max_retries:
            try:
                response = requests.get(base_url, timeout=5)
                
                if response.status_code == 200:
                    activity = response.json()
                    activities.append(activity)
                    print(f"Activity {i+1}/{limit} added successfully")
                    time.sleep(1)
                    break
                elif response.status_code == 503:
                    print(f"API temporarily unavailable (503). Attempt {retries + 1} of {max_retries}")
                    retries += 1
                    if retries == max_retries:
                        print("API still unavailable. Will try again later...")
                        return activities
                    time.sleep(5)
                else:
                    print(f"Unexpected error: Status {response.status_code}")
                    retries += 1
                    time.sleep(2)
                    
            except requests.RequestException as e:
                print(f"Request error: {e}")
                retries += 1
                if retries == max_retries:
                    print("Maximum number of attempts reached")
                    return activities
                time.sleep(2)
    
    return activities