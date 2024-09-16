# Getting Started

## Cloning the Repository

To begin, please clone the repository to your local machine. This will provide you with all the necessary files to run and deploy the server:

```bash
git clone https://github.com/LambdaLightSource/diamond-image-service
```

## Running Locally

Navigate to the thumbor_ directory and execute server.py to start the server locally:

```bash
pip install -e .[dev]
python server.py
```
You can access the local server at: http://localhost:8888/unsafe/<image_name>

This will allow you to test image processing directly in your browser.

# Testing Locally with Dev Containers in VSCode.

Please ensure the latest version of the dev containers app is installed. Click the blue icon in the bottom left corner of your editor to open the menu and select "Rebuild in Container" to set up your development environment.