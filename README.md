# Threat Intelligence Service Documentation

This documentation provides an overview of the Threat Intelligence Service, a small FastAPI application designed for reporting and querying suspicious IP addresses.

## Table of Contents

1. [Introduction](#introduction)
2. [Setup](#setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
3. [Endpoints](#endpoints)
   - [POST /report-ip](#post-report-ip)
   - [GET /query-ip](#get-query-ip)
4. [Security Measures](#security-measures)
   - [JWT Authentication](#Authentication)
5. [Testing](#testing)
6. [Future Enhancements](#future-enhancements)

## Introduction

The Threat Intelligence Service is a FastAPI application designed to allow users to report and query suspicious IP addresses. It utilizes a PostgreSQL database for data storage, employs basic authentication for security, and handles requests concurrently using asynchronous programming concepts.

## Setup

### Prerequisites

Ensure you have the following installed before setting up the project:

- Python (>= 3.8)
- PostgreSQL
- Pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mahmoodiian/ThreatIntelligenceReportingService.git
   cd ThreatIntelligenceReportingService
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your PostgreSQL database and configure the `DATABASE_URL` in `settings/database.py` with your credentials.

### Running the Application

Run the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## Endpoints

### POST /report-ip

This endpoint accepts an IP address and updates the `suspicious_ip` table. If the IP is already reported, it increments the `report_count` and updates the `last_reported` timestamp.

#### Request:
- Method: POST
- Endpoint: `/report-ip`
- Body: JSON with the following structure:
  ```json
  {
    "ip_address": "192.168.1.1"
  }
  ```

#### Response:
- Status Code: 200 OK
- Body: JSON with the id and success message.

### GET /query-ip

This endpoint takes an IP address and returns its details if present in the database.

#### Request:
- Method: GET
- Endpoint: `/query-ip`
- Query Parameters: `ip_address` (e.g., `/query-ip/?ip_address=192.168.1.1`)

#### Response:
- Status Code: 200 OK
- Body: JSON with the details of the IP address.

## Security Measures

### Authentication Endpoint

- **POST /token/**: Generate an access token by providing a valid username and password.

## Authentication

The application uses JWT for token-based authentication. The `login_for_access_token` endpoint handles user authentication and returns a JWT token upon successful login.

### Request Example:

```bash
curl -X POST "http://127.0.0.1:8000/token/" -d "username=admin&password=admin"
```

Replace `admin` with your actual username and password.

### Response Example:

```json
{
  "access_token": "your_generated_access_token",
  "token_type": "bearer"
}
```

Use the obtained access token for authenticated requests.

## Testing

The test cases cover basic functionality for both reporting and querying IP addresses. To run the tests:

```bash
pytest
```

## Future Enhancements

- Enhance IP validation using additional libraries or custom logic.
- Implement asynchronous database operations for improved performance.
- Include additional security measures such as HTTPS.