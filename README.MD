# Project EndOfLife

## Overview

This project consists of two main components:

1. **k8s-scanner**: A Python-based application for scanning Kubernetes namespaces and listing container images and versions.
2. **public-repo-scanner**: A Flask application that aggregates and displays version data from various public repositories and APIs.

## Project Structure

- `k8s_scanner/`
  - `k8s_scanner.py`
  - `Dockerfile`
- `public_repo_scanner/`
  - `public_repo_scanner.py`
  - `Dockerfile`
- `dashboard/`
  - `dashboard.py`
  - `templates/`
    - `dashboard.html`
- `endpoints.py`

## Requirements

- **Python 3.x**
- **Flask** for the web application
- **requests** for making HTTP requests

## Setup

### 1. Setting Up the Environment

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>

## Install Python Dependencies:
```bash
pip install -r requirements.txt
```

### 2. Docker Setup
Build Docker Images:
```bash
cd k8s_scanner
docker build -t kiryanovi/k8s-scanner:latest .

cd ../public_repo_scanner
docker build -t kiryanovi/public-repo-scanner:latest .

```

 ## Run Docker Containers:
```bash
docker run -d -p 5001:5001 kiryanovi/public-repo-scanner:latest
docker run -d -p 5002:5002 kiryanovi/k8s-scanner:latest
```

### Running Locally

Start k8s-scanner:
```bash
python3 k8s_scanner/k8s_scanner.py
```
Start public-repo-scanner:
```bash
python3 public_repo_scanner/public_repo_scanner.py
```
Start the Dashboard:
```bash
python3 dashboard/dashboard.py
```

### Troubleshooting
## Common Errors:

404 Not Found: Ensure the correct URL is being used and that the server is running.
Error fetching data: Check the logs for specific error messages and verify the external API URLs.
Public Repo Scanner Errors:

"No public available version data": This may occur if the data from an API endpoint is not available or the endpoint URL is incorrect. Verify the endpoint URLs in endpoints.py and check API responses manually.
Docker Issues:

Port Conflicts: Ensure that the ports used by Docker containers are not occupied by other services. Change the ports if necessary.
Python Script Issues:

Import Errors: Make sure all required libraries are installed. Check requirements.txt for dependencies.
Dashboard Data Formatting Issues:

Incorrect Version Display: Verify that version and cycle data are correctly parsed and formatted in public_repo_scanner.py and adjust the dashboard template if needed.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

### Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure that all changes are well-documented and tested.