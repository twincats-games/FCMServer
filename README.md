# File Checkout Manager (FCM) Server

The **File Checkout Manager (FCM)** is a backend service that allows users to check out, release, and manage files in a version-controlled environment. It exposes REST APIs for checking the status of files, checking out multiple files, and managing file checkouts with a secure and rate-limited approach.

This service is implemented using **FastAPI**, **SQLAlchemy** for database interaction, and **Docker** for deployment.

## Table of Contents

- [File Checkout Manager (FCM) Server](#file-checkout-manager-fcm-server)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Setup \& Installation](#setup--installation)
  - [Environment Variables](#environment-variables)
  - [API Endpoints](#api-endpoints)
    - [1. **Checkout File**](#1-checkout-file)
    - [2. **Checkout Multiple Files**](#2-checkout-multiple-files)
    - [3. **Release File**](#3-release-file)
    - [4. **Release Multiple Files**](#4-release-multiple-files)
    - [5. **Get File Status**](#5-get-file-status)
    - [6. **Get Multiple File Status**](#6-get-multiple-file-status)
  - [Security \& Rate Limiting](#security--rate-limiting)
  - [Logging](#logging)
  - [Docker Setup](#docker-setup)
  - [Testing \& Swagger UI](#testing--swagger-ui)
  - [Contributing](#contributing)
  - [License](#license)
    - [**Key Sections:**](#key-sections)

## Features

- **File Checkout System**: Users can check out individual or multiple files.
- **File Status**: Retrieve the checkout status of a file, including the user who has it checked out.
- **Release Files**: Allows users to release files they have checked out.
- **Rate Limiting**: Protects the server from potential DDoS attacks by limiting the number of requests within a time window.
- **Security**: Utilizes JWT authentication and CORS protection to ensure secure and authorized access.

## Requirements

- Python 3.13+
- PostgreSQL (or compatible) database
- Docker (for containerized deployment)

## Setup & Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/twincats-games/FCMServer.git
   cd fcm-server
   ```

2. **Install dependencies**:

   It is recommended to use a virtual environment.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure the environment variables**:

   You need to set environment variables for the application to work. Create a `.env` file at the root of the project and add the following:

   ```env
   DATABASE_URL=postgresql://user:password@db:5432/fcm_db
   SECRET_KEY=your-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   RATE_LIMIT_MAX_REQUESTS=100
   RATE_LIMIT_WINDOW_SECONDS=60
   ALLOWED_HOSTS=https://services-twincats.ddns.net
   ```

4. **Run the application**:

   You can start the server using `uvicorn` for local development:

   ```bash
   uvicorn app.main:app --reload
   ```

   This will start the server at `http://127.0.0.1:8000`.

## Environment Variables

| Variable                        | Description                                                                                       | Default Value                  |
|----------------------------------|---------------------------------------------------------------------------------------------------|--------------------------------|
| `DATABASE_URL`                   | The database connection URL for PostgreSQL.                                                       | `sqlite:///./test.db`          |
| `SECRET_KEY`                     | The secret key for JWT authentication.                                                            | `"super-secret-key"`           |
| `ACCESS_TOKEN_EXPIRE_MINUTES`    | The expiration time for access tokens in minutes.                                                  | `60`                           |
| `RATE_LIMIT_MAX_REQUESTS`        | The maximum number of requests allowed within the time window.                                     | `100`                          |
| `RATE_LIMIT_WINDOW_SECONDS`      | The time window in seconds for rate limiting.                                                     | `60`                           |
| `ALLOWED_HOSTS`                  | A comma-separated list of allowed origins for CORS requests.                                      | `"https://your-host.com"` |

## API Endpoints

### 1. **Checkout File**

- **POST** `/api/v1/checkout`
- **Body**: 
   ```json
   {
     "file_path": ["path/to/file.txt"],
     "user_id": 123
   }
   ```

### 2. **Checkout Multiple Files**

- **POST** `/api/v1/checkout`
- **Body**:
   ```json
   {
     "file_paths": ["path/to/file1.txt", "path/to/file2.txt"],
     "user_id": 123
   }
   ```

### 3. **Release File**

- **POST** `/api/v1/release`
- **Body**:
   ```json
   {
     "file_path": ["path/to/file.txt"],
     "user_id": 123
   }
   ```

### 4. **Release Multiple Files**

- **POST** `/api/v1/release`
- **Body**:
   ```json
   {
     "file_paths": ["path/to/file1.txt", "path/to/file2.txt"],
     "user_id": 123
   }
   ```

### 5. **Get File Status**

- **GET** `/api/v1/status`
- **Query Parameters**: `file_path`
- **Response**:
   ```json
   {
     "file_path": ["path/to/file.txt"],
     "user_id": 123,
     "status": "CHECKED_OUT"
   }
   ```

### 6. **Get Multiple File Status**

- **GET** `/api/v1/status`
- **Query Parameters**: `file_paths=path/to/file1.txt,path/to/file2.txt`
- **Response**:
   ```json
   {
     "path/to/file1.txt": {
       "user_id": 123,
       "status": "CHECKED_OUT"
     },
     "path/to/file2.txt": {
       "user_id": null,
       "status": "AVAILABLE"
     }
   }
   ```

## Security & Rate Limiting

The application implements **rate limiting** to prevent DDoS attacks by limiting the number of requests a client can make in a defined time window. If the client exceeds the limit, a `429 Too Many Requests` error will be returned.

Additionally, **CORS** is used to restrict cross-origin requests, and **JWT Authentication** ensures that only authorized users can perform actions like file checkout and release.

## Logging

Logs are stored in the `logs/` directory and are configured to rotate every 7 days, with a maximum size of 100MB per log file. This ensures that the logs remain manageable while retaining recent history.

## Docker Setup

To run the server in a **Docker** container, follow these steps:

1. **Build the Docker image**:

   ```bash
   docker-compose build
   ```

2. **Start the application**:

   ```bash
   docker-compose up
   ```

This will start the server and make it available at `http://127.0.0.1:8000`.

## Testing & Swagger UI

Once the application is running, you can test the endpoints and interact with the API using **Swagger UI** at:

```
http://127.0.0.1:8000/docs
```

Alternatively, you can view the raw OpenAPI schema at:

```
http://127.0.0.1:8000/openapi.json
```

## Contributing

Feel free to open issues or create pull requests for improvements or bug fixes!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### **Key Sections:**
- **Setup & Installation**: Guides users through cloning, installing dependencies, and running the app.
- **Environment Variables**: Lists all the necessary environment variables with their default values.
- **API Endpoints**: Provides details on the available endpoints, the request format, and responses.
- **Security & Rate Limiting**: Explains the implemented safety measures, such as JWT authentication and rate limiting.
- **Logging**: Describes the logging configuration for rotating logs and keeping logs within a manageable size.
- **Docker Setup**: Instructions for building and running the app in a Docker container.
- **Testing & Swagger UI**: Explains how to access the Swagger UI to test the API.

Let me know if you'd like to add anything else to the README!