# ml-api-rate-limiter

## Protecting the Performance of Production Machine Learning APIs with Effective Rate Limiting


### Summary
- The code sends multiple HTTP GET requests to a specified API endpoint.
- It checks the status code of each response and handles cases for successful requests (200 OK) and rate-limiting responses (429 Too Many Requests).
- If not rate-limited, it mentions how many more requests the client can send, followed by the timing left to send those requests.
- If rate-limited, it extracts the Retry-After header to determine how long to wait before making another request.
- It also handles exceptions that might occur during the HTTP request process.

#### API rate limiter with Redis as in-memory CACHE
  ![Design_rate_limiter](https://github.com/user-attachments/assets/39a90050-5de8-413b-8038-0e11f48b1f79)



### Introduction
Deploying machine learning (ML) models, including large language models (LLMs), to production is a crucial step in making them accessible and useful in real-world scenarios. However, deploying a model isn't just about making it available; it also involves ensuring it operates efficiently, remains available, and is protected from misuse or overloading. 

Once your machine learning model is trained and ready to go, you need to decide how to deploy it. There are several common approaches, each with its own advantages:
1.	Real-time APIs: Perfect for applications that need instant feedback, like chatbots or real-time recommendations. This approach allows users to interact with your model on-the-fly.
2.	Batch Processing: Ideal for scenarios where you need to process large volumes of data all at once. This is often used for offline analysis or generating reports.
3.	Edge Deployment: Deploying models directly on devices or local servers can reduce latency and address data privacy concerns, as the data doesn’t need to be sent to a central server.
4.	Serverless Functions: Cloud-based serverless platforms can execute model inference without the need to manage infrastructure, automatically scaling based on demand.
5.	Containerisation: Using containers like Docker helps manage and deploy your model consistently across different environments. Tools like Kubernetes can help scale and orchestrate these containers.

In this project, we'll focus on the first approach, ML models that have been productionised and available as an API. This project explains how to design and develop a rate limiter to protect any API-based system, including those that serve machine learning models. We'll use a sample project to illustrate this process, including code for rate limiting, API setup, and unit testing.


### What is API Rate Limiter?
An API rate limiter is a mechanism to control the number of requests a client can make to an API within a specific time period (e.g., 100 requests per minute). It ensures that all clients receive a fair share of resources and prevents any single client from overwhelming the system. Also, it protects backend systems from being overloaded and maintains performance stability. Rate limiting is especially important in high-traffic environments and helps maintain the performance and reliability of the system.


### Three Approaches to Design API Rate Limiter
Three common approaches to design the rate limiter are explained in below table and presented in below image. Among them, the third approach (API Gateway Rate Limiter) is generally preferred due to its centralised control, low latency impact, and efficient use of caching for data storage. This method simplifies scaling and provides consistent rate limiting, while minimising added complexity and latency. In addition, there is no extra call to API gateway since anyway we hit the API gateway for checking security of request. 

![Rate_limiter_approaches](https://github.com/user-attachments/assets/ad08830d-c1c4-4b68-8395-4f32c05cc594)

#### Comparing three designs of Rate Limiter
![Rate_limiter_approaches_Comparison](https://github.com/user-attachments/assets/f7332970-c767-468c-a2e0-533ceb48de67)

In order to implement the rate limiter logic, we need (1) client’s user ID or IP address to be able to identify them, (2) number of allowed requests in a specific period of time, and (3) timestamp of latest request per client. Ideally, we need (1) temporary storage for recent data only and (2) very fast access. This makes sure that your memory usage is very low and you are not retaining indefinite unnecessary data. There are two common options as storage, including a database such as MySQL database, and CACHE. MySQL database is not memory efficient since it stores one record for every request, which data size will be extremely big as client sends more requests to API. It causes storing unnecessary data that we may not need to use them after sometime. Also, accessing this data stored in disk, followed by computations and aggregation queries on this big data will be time taking that causes latency. On the other hand, CACHE stores data temporarily and provides very quick access to data because CACHE resides in memory not disk, whereas SQL DB stores data in disk.
Redis is a common caching client that (1) stores data in memory, (2) provides quick access to data, (3) uses time to leave (TTL) to retain data for specific period of time only, and (4) minimises computation time since it includes functions like increment, decrement, and counters, that we can easily use to do very quick math, which is all we need to rate limiter.

API Gateway Rate Limiter with Data Storage (Redis as in-Memory CACHE)
When the client makes the request, the rate limiter gets the request, does some calculation based on data in cache whether the user should be rate limited or not. If the user should be rate limited, it sends http status code of 429 to the user. So, user know that they are rate limited, otherwise it forwards the request to API server and API server sends back the response to the client.

![Design_rate_limiter](https://github.com/user-attachments/assets/96293ab2-3b3f-4500-8b55-db1a6d762a35)

Rate Limiter needs to provide enough feedback to the client about why they have been rate limited and when they can send the request. In this work, we use appropriate status code (status code of 429 that represents too many requests) to notify the client that they exceeded sending requests to the API, the time that they can try to send a new request (e.g. ‘Client exceeded sending requests. Please try again after 10 seconds’). Also, when their request is successful, we provide them information about how many more requests they can send in a specific period of time that we mention them too (e.g. ‘Request was successful. They can send 5 more requests in the next 20 seconds’).


### Python Implementation
The code has been developed in Python; I have used Visual Studio Code for this demo. Code structure is as below:

![Code_structure](https://github.com/user-attachments/assets/32087172-71fe-43c8-84a7-eac2d57482f9)

- rate_limiter.py: Implements the core rate limiting logic.
- api_gateway.py: Sets up the API endpoint that utilises the rate limiter.
- test_rate_limiter.py: Writes tests to validate the functionality of the rate limiter.
- requirements.txt: Specify dependencies and Python packages used in this work.


## Outputs:

#### Redis Serve is up and running
![Redis_server](https://github.com/user-attachments/assets/708a8257-ed26-459f-b591-9d4bff1e6717)

#### A demanding API has been created using Flask, which is up and running
![API_call_flask](https://github.com/user-attachments/assets/d5a91361-304f-4c78-ba77-5dd587331297)

#### Output of unit test
![Unit_test_output](https://github.com/user-attachments/assets/5786f08b-8ac0-4b94-b132-b34a4e51dd31)
