# ml-api-rate-limiter

## Protecting the Performance of Production Machine Learning APIs with Effective Rate Limiting

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

![Rate_limiter_approaches](https://github.com/user-attachments/assets/052b0764-f80b-403b-9227-c4504247b2b1)

![Rate_limiter_approaches_Comparison](https://github.com/user-attachments/assets/f7332970-c767-468c-a2e0-533ceb48de67)

In order to implement the rate limiter logic, we need (1) client’s user ID or IP address to be able to identify them, (2) number of allowed requests in a specific period of time, and (3) timestamp of latest request per client. Ideally, we need (1) temporary storage for recent data only and (2) very fast access. This makes sure that your memory usage is very low and you are not retaining indefinite unnecessary data. There are two common options as storage, including a database such as MySQL database, and CACHE. MySQL database is not memory efficient since it stores one record for every request, which data size will be extremely big as client sends more requests to API. It causes storing unnecessary data that we may not need to use them after sometime. Also, accessing this data stored in disk, followed by computations and aggregation queries on this big data will be time taking that causes latency. On the other hand, CACHE stores data temporarily and provides very quick access to data because CACHE resides in memory not disk, whereas SQL DB stores data in disk.
Redis is a common caching client that (1) stores data in memory, (2) provides quick access to data, (3) uses time to leave (TTL) to retain data for specific period of time only, and (4) minimises computation time since it includes functions like increment, decrement, and counters, that we can easily use to do very quick math, which is all we need to rate limiter.

API Gateway Rate Limiter with Data Storage (Redis as in-Memory CACHE)
When the client makes the request, the rate limiter gets the request, does some calculation based on data in cache whether the user should be rate limited or not. If the user should be rate limited, it sends http status code of 429 to the user. So, user know that they are rate limited, otherwise it forwards the request to API server and API server sends back the response to the client.

![Design_rate_limiter](https://github.com/user-attachments/assets/96293ab2-3b3f-4500-8b55-db1a6d762a35)

Rate Limiter needs to provide enough feedback to the client about why they have been rate limited and when they can send the request. In this work, we use appropriate status code (status code of 429 that represents too many requests) to notify the client that they exceeded sending requests to the API, the time that they can try to send a new request (e.g. ‘Client exceeded sending requests. Please try again after 10 seconds’). Also, when their request is successful, we provide them information about how many more requests they can send in a specific period of time that we mention them too (e.g. ‘Request was successful. They can send 5 more requests in the next 20 seconds’).

### Python Implementation
The code has been developed in Python; I have used Visual Studio Code for this demo. Code structure is as below:

/rate_limiter_project
    ├── rate_limiter.py
    ├── api_gateway.py
    ├── test_rate_limiter.py
    ├── requirements.txt

•	rate_limiter.py: Implements the core rate limiting logic.
•	api_gateway.py: Sets up the API endpoint that utilises the rate limiter.
•	test_rate_limiter.py: Writes tests to validate the functionality of the rate limiter.
•	requirements.txt: Specify dependencies and Python packages used in this work.

To run and test the initial code using VS Code, follow these steps:

1.	Install Dependencies
1.1.	Create a Virtual Environment (optional but recommended)
        		Navigate to your project directory (/rate_limiter_project) in the terminal.
cd C:\Users\Amir\Desktop\Jobs\2025\Atlassian_Sen_ML_Eng\rate_limiter_project
        		
Create a virtual environment:
            			python -m venv venv
        		
Activate the virtual environment:
            			.\vnev\Scripts\Activate.ps1
		
1.2.	Install Required Packages
With the virtual environment activated, install the dependencies listed in requirements.txt:
        			pip install -r requirements.txt

2.	Run the API Gateway
2.1.	Start the Redis Server
        		Make sure your Redis server is running. You can start it with the following command (run this in a separate terminal):
            			redis-server

2.1.1.	Challenge 1- Your system can't find the redis-server command
This error usually means that Redis isn't installed correctly or its executable isn't in your system's PATH. Let's go through the steps to resolve this issue.

Installing Redis
•	Download Redis: Redis isn't natively supported on Windows, so you'll need to use a precompiled binary or use Windows Subsystem for Linux (WSL) or Docker. The easiest way is to use a precompiled Redis binary. Download Redis from the Microsoft Open Tech GitHub page. Look for a .msi installer or a .zip archive (I did .msi).
•	Install Redis: If you downloaded an installer (.msi), run it and follow the installation instructions. If you downloaded a .zip file, extract it to a directory of your choice.
•	Add Redis to PATH: After installing or extracting Redis, add its directory to your system's PATH environment variable.
        			To add Redis to PATH:
•	Open the Start Menu and search for "Environment Variables".
•	Click on "Edit the system environment variables".
•	In the System Properties window, click on the "Environment Variables" button.
•	In the Environment Variables window, under "System variables", find the Path variable, select it, and click "Edit".
•	Click "New" and add the path to the Redis bin directory (e.g., C:\Program Files\Redis\ if you used the installer).
•	Click "OK" to close all dialog boxes.
 

•	Verify Installation: Open a new Command Prompt or PowerShell window and type:
            					redis-server --version

2.1.2.	Challenge 2- Redis is unable to bind to the TCP port 6379, which is the default port for Redis
This can happen for a few reasons:
•	Port Already in Use: Another application might already be using port 6379.
•	Configuration Issues: There might be issues with your Redis configuration.
•	Permissions: The process might not have the necessary permissions to bind to the port.

Here’s how to troubleshoot and resolve these issues:
1.	Check if Port is Already in Use: 
•	Open Command Prompt or PowerShell as Administrator.
•	Run the following command to check if port 6379 is in use:
            					netstat -ano | findstr :6379
•	If another process is using port 6379, you’ll see output with the PID (Process ID). You might need to stop or change that process.
•	Kill the Process Using the Port (if needed):
taskkill /PID <PID> /F

Example of Running Redis with Default Settings
•	Open Command Prompt or PowerShell as Administrator.
•	Navigate to the Redis Installation Directory (if needed):
cd C:\Program Files\Redis
•	Run Redis Server:
redis-server
•	Verifying Redis is Running: After starting Redis, you should be able to connect to it using the Redis CLI (redis-cli). Open a new Command Prompt or PowerShell window and run:
        				redis-cli
•	You can then test the connection by running a command like:
        				ping
    				Redis should respond with PONG.

If The output of the netstat -ano | findstr :6379 command indicates that port 6379 is currently being used by a process. Here’s a breakdown of the output:
TCP    0.0.0.0:6379           0.0.0.0:0              LISTENING       19056
TCP    [::]:6379                  [::]:0                      LISTENING       19056

Breakdown of the Output
•	TCP: The protocol being used (Transmission Control Protocol).
•	0.0.0.0:6379: This indicates that the port 6379 is bound to all network interfaces (0.0.0.0) for IPv4 connections.
•	[::]:6379: This indicates that the port 6379 is bound to all network interfaces ([::]) for IPv6 connections.
•	LISTENING: The state of the port. It means the port is open and actively waiting for incoming connections.
•	19056: The Process ID (PID) of the application that is using port 6379.

which application is using the port 6379?
•	In Command Prompt or PowerShell, run:
tasklist /FI "PID eq 19056"
This command will list the name of the process that has PID 19056.

Stop or Restart the Process: If you want to stop the process, you can use:
taskkill /PID 19056 /F
This command forcibly terminates the process with PID 19056.

If you need to restart Redis after stopping the conflicting process, try running:
    					redis-server

Check for Redis Instances: If you find that Redis is already running, you don’t need to start it again. You can connect to the existing instance using the Redis CLI:
redis-cli
Test the connection by typing:
ping
    			Redis should respond with PONG.

Change Port for Redis (if needed): 
•	If stopping the existing process is not an option, you can configure Redis to use a different port.
•	Create or edit the Redis configuration file (redis.conf) in a note pad and save it anywhere, and change the port number:
port 6380
Start Redis with the new configuration:
redis-server /path/to/redis.conf

What I did:
-	Located redis.conf in cd C:\Users\Amir\Desktop\Jobs\2025\Atlassian_Sen_ML_Eng\rate_limiter_project
-	cd C:\Users\Amir\Desktop\Jobs\2025\Atlassian_Sen_ML_Eng\rate_limiter_project
-	redis-server ./redis.conf
 
•	Redis 3.0.504: This is the version of Redis you are running.
•	64 bit: Indicates that Redis is running in 64-bit mode.
•	This banner is an ASCII art representation of Redis. It also includes a note that Redis is running in standalone mode.
•	[11092]: This is the process ID (PID) of the Redis server process.
•	11 Aug 14:09:19.538: The date and time when the server started.
•	Server started: Indicates that the Redis server has successfully started.
•	Redis version 3.0.504: Confirms the version of Redis that is running.
•	The server is now ready to accept connections on port 6380: Indicates that Redis is up and running and is listening for connections on port 6380.

About Redis:
Redis is an in-memory data structure store, commonly used as a database, cache, and message broker. Here's a detailed explanation of what redis-server does:
Overview of Redis
1.	In-Memory Data Store: Redis stores data in RAM, which allows for extremely fast read and write operations. This makes it suitable for caching and real-time analytics.
2.	Data Structures: Redis supports various data structures, including strings, lists, sets, sorted sets, hashes, bitmaps, hyperloglogs, and geospatial indexes.
3.	Persistence: Redis offers options for data persistence to disk, allowing data to be saved between restarts. It supports two main persistence methods:
o	Snapshotting (RDB): Periodically saves snapshots of the dataset.
o	Append-Only File (AOF): Logs every write operation received by the server, allowing for a more complete recovery of data.
4.	Replication: Redis supports master-slave replication, which enables data to be replicated across multiple Redis instances for high availability and load balancing.
5.	Pub/Sub Messaging: Redis provides a publish/subscribe messaging paradigm, allowing messages to be sent between clients in real-time.
6.	High Availability: Redis Sentinel provides monitoring, notification, and failover mechanisms to ensure high availability and automated failover.

What redis-server Does
1.	Starts Redis Server: When you run redis-server, it starts the Redis server process. This process listens for incoming connections from clients on a specified port (default is 6379).
2.	Configuration: Redis can be configured using a configuration file (e.g., redis.conf). The redis-server command can optionally take a path to this configuration file to customize its behavior. If no configuration file is provided, Redis uses default settings.
3.	Handles Commands: Once running, the Redis server handles commands from clients, such as GET, SET, HSET, LPUSH, and many more. It processes these commands and returns responses accordingly.
4.	Data Management: It manages data in memory according to the commands it receives, and it handles data persistence if configured to do so.
5.	Client Connections: The server manages multiple client connections simultaneously, allowing various clients to interact with Redis concurrently.
Common Usage
•	Development and Testing: Developers use Redis in local development environments to simulate caching, session storage, or other use cases.
•	Production Systems: In production, Redis is used for high-performance caching, real-time analytics, message brokering, and more.
•	Testing and Debugging: Running redis-server locally can be useful for testing Redis-based applications or debugging issues.

2.2.	Run the API Gateway
In the terminal, navigate to your project directory if not already there.
cd C:\Users\Amir\Desktop\Jobs\2025\Atlassian_Sen_ML_Eng\rate_limiter_project

Active VENV
            			.\vnev\Scripts\Activate.ps1

    		Run the API gateway script:
        			python api_gateway_2.py
   		This will start a Flask server that listens for HTTP requests.
 

More info about API Gateway:
The api_gateway.py file in your project simulates an API gateway that interacts with a rate limiter to handle incoming requests

How api_gateway.py Works
1.	Imports and Initialization
o	Flask: Used to create the web application.
o	RateLimiter: This is a custom class imported from rate_limiter.py which handles the rate limiting logic.
o	time: Imported but not used in this snippet. (You might have used it for rate limiting logic or for other purposes.)

3.	Test the Rate Limiter

    Run Unit Tests:
•	Open a new terminal window (or tab) in VS Code.
•	Make sure your virtual environment is activated.
•	Navigate to the project directory if not already there.
•	Run the unit tests:
cd C:\Users\Amir\Desktop\Jobs\2025\Atlassian_Sen_ML_Eng\rate_limiter_project

.\vnev\Scripts\Activate.ps1

python test_rate_limiting_4.py

