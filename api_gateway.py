# Flask: This is the main class from the Flask web framework used to create the web application.
# request: A module from Flask that allows access to request data such as query parameters, form data, etc.
# jsonify: A function from Flask to convert Python dictionaries to JSON responses.
# RateLimiter: This is a custom class imported from rate_limiter_2.py which presumably contains the logic for rate limiting.
# time: Imported but not used in this snippet. It might be used in the RateLimiter class or could be intended for other functionalities such as delays.

from flask import Flask, request, jsonify
from rate_limiter import RateLimiter
import time

# Flask Application Initialization: Creates an instance of the Flask web application. 
# __name__ is a special Python variable that represents the name of the module. 
# Flask uses this to know where to look for resources.
app = Flask(__name__)

# Rate Limiter Initialization: Creates an instance of the RateLimiter class. 
# This object will be used to check whether a user’s requests are within the allowed limits.
rate_limiter = RateLimiter()

# API Endpoint (Route) Definition: Defines a route for the endpoint /api/resource that responds to GET requests. 
# When a request is made to this endpoint, the resource function is called.
@app.route('/api/resource', methods=['GET'])
def resource():
    # Extracting Query Parameter: Retrieves the user_id parameter from the query string of the request URL. 
    # This user_id is used to identify which user's requests need to be rate-limited.
    user_id = request.args.get('user_id')  # Assume client sends user_id to identify rate limits
    
    # Rate Limiting Check:
    # Calls the is_allowed method of the RateLimiter instance, passing the user_id. This method checks if the user has exceeded their request limit and returns a tuple (allowed, retry_after):
    #     allowed: A boolean indicating if the request is allowed or not.
    #     retry_after: A string or integer indicating how many seconds the client should wait before making another request if the rate limit has been exceeded.
    allowed, retry_after = rate_limiter.is_allowed(user_id)
    
    # Number of remaining requests in that specific timeframe and amount of time left for that specific time window
    remaining_requests, time_left = rate_limiter.get_rate_limit_status(user_id)
    
    # Handling Allowed Requests:
    # If the request is allowed (allowed is True), it returns a JSON response with a success message ("Request successful"). The status code defaults to 200 OK.
    if allowed:
        return jsonify({
            "message": "Request successful",
            "remaining_requests": remaining_requests,
            "time_left": time_left
        })
    
    # Handling Rate-Limited Requests:
    # If the request is not allowed (allowed is False):
    #     Creates a JSON response with a message indicating the rate limit has been exceeded ("Rate limit exceeded").
    #     Sets the HTTP status code to 429 to indicate the rate limit error.
    #     Adds a Retry-After header to the response, specifying how long the client should wait before making another request. This header value is obtained from the retry_after variable returned by the is_allowed method.
    #     Returns the response.
    else:
        response = jsonify({
            "message": "Rate limit exceeded",
            "remaining_requests": 0,
            "time_left": retry_after
        })
        response.status_code = 429
        response.headers['Retry-After'] = retry_after
        return response

# Starting the Server: Checks if the script is being run directly (not imported as a module in another script). 
# If so, it starts the Flask development server on port 5000.
if __name__ == '__main__':
    app.run(port=5000) # default port for API applications
    # Using a default port like 5000 helps avoid port conflicts and provides a consistent environment for development
