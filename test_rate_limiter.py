import requests # used to make HTTP requests.
import time # handles time-related functions, such as sleeping.

# API endpoint
# Defines the URL of the API endpoint to which requests will be sent. 
# This points to a local server running on port 5000.
url = "http://127.0.0.1:5000/api/resource"

# Number of requests to make to the API endpoint
num_requests = 20

for i in range(1, num_requests + 1): # run the loop 70 times, each time sending a request to the API.
    try:
        # Make the HTTP GET request
        response = requests.get(url) # Sends an HTTP GET request to the API endpoint specified by url and stores the response in the response variable.
        
        if response.status_code == 200:
            data = response.json()
            remaining_requests = data.get("remaining_requests")
            time_left = data.get("time_left")
            print(f"Request {i}: Status Code = 200 OK, Remaining Requests = {remaining_requests}, Time Left = {time_left} seconds")
        elif response.status_code == 429:
            # Extract the Retry-After header if present
            retry_after = response.headers.get("Retry-After", "unknown") # If the header is not present, it defaults to "unknown".
            print(f"Request {i}: Rate limit exceeded. Retry after {retry_after} seconds.")
            # Wait for the retry-after period plus a little extra time to ensure we respect the limit
            time.sleep(int(retry_after) + 1)  # Sleep longer than the Retry-After time
        else:
            print(f"Request {i}: Status Code = {response.status_code}")
    
    except requests.RequestException as e: # Catches and handles exceptions that may occur during the HTTP request.
        # Handle exceptions
        print(f"Request {i}: Exception occurred - {e}") # Prints a message indicating that an exception occurred, along with the exception details.
