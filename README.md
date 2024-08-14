# ml-api-rate-limiter

## Protecting the Performance of Production Machine Learning APIs with Effective Rate Limiting

### Overview of ML Model Deployment and Rate Limiting Solutions
The importance of deploying machine learning models in production as APIs, real-world examples of ML models utilised as APIs, concept of rate limiting, and key solution designs have been explained here: 

### Summary
- The code sends multiple HTTP GET requests to a specified API endpoint.
- It checks the status code of each response and handles cases for successful requests (200 OK) and rate-limiting responses (429 Too Many Requests).
- If not rate-limited, it mentions how many more requests the client can send, followed by the timing left to send those requests.
- If rate-limited, it extracts the Retry-After header to determine how long to wait before making another request.
- It also handles exceptions that might occur during the HTTP request process.


### Python Implementation
The code has been developed in Python; I have used Visual Studio Code for this demo. Code structure is as below:

![Code_structure](https://github.com/user-attachments/assets/32087172-71fe-43c8-84a7-eac2d57482f9)

- rate_limiter.py: Implements the core rate limiting logic.
- api_gateway.py: Sets up the API endpoint that utilises the rate limiter.
- test_rate_limiter.py: Writes tests to validate the functionality of the rate limiter.
- requirements.txt: Specify dependencies and Python packages used in this work.


## Outputs:

#### Redis Serve is up and running
Redis is used to store the CACHE and perform computations regarding rate limiter decisioning
![Redis_server](https://github.com/user-attachments/assets/708a8257-ed26-459f-b591-9d4bff1e6717)

#### A demanding API has been created using Flask, which is up and running
This App serves as an API gateway with rate limiting functionality
![API_call_flask](https://github.com/user-attachments/assets/d5a91361-304f-4c78-ba77-5dd587331297)

#### Output of unit test
- If client request to the API is allowed, client can see how many more requests they can send to API followed by the time period.
- If client exceeded number of requests to API, they will be informed when they are allowed to send the next request to the API.
![Unit_test_output](https://github.com/user-attachments/assets/87e79913-8053-4d66-a312-23b1d40909b0)

