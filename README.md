# Sorting Hat

## Overview
**Sorting Hat** is a modern tool designed to efficiently assign students to projects based on specific constraints such as student preferences and project availability. At its core, Sorting Hat leverages the powerful SCIP solver from Google OR-Tools to solve constrained integer programs, ensuring optimal assignment solutions.

This tool integrates a MongoDB database to maintain student and project data, and features a user-friendly Streamlit frontend for seamless data entry and assignment visualization. The entire application is containerized with Docker, making setup and deployment straightforward and consistent across different environments.

## Features
- **Student and Project Management**: Easily input and manage student and project data through a Streamlit-based interface.
- **Optimized Assignment**: Uses SCIP solver to ensure that students are assigned to projects based on predefined constraints effectively.
- **Dockerized Environment**: Includes complete Docker and Docker Compose configurations for easy deployment and scalability.
- **Interactive Notebooks**: Jupyter Notebook integration for advanced data analysis and manual adjustments.

## Prerequisites
Before you can run Sorting Hat, you need to have Docker and Docker Compose installed on your machine. These tools will handle the installation of all necessary software components.

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### Clone the Repository
First, clone the repository to your local machine:

```
git clone https://github.com/jbackofe/sorting-hat.git
cd sorting-hat
```

### Start the Project
To start all services defined in the Docker Compose file, run the following command from the root of your cloned repository:

`docker-compose up -d`

This command builds and starts the following services:
- **MongoDB**: NoSQL database service for storing student and project data.
- **Jupyter**: A Jupyter Notebook server pre-configured with all required dependencies.
- **Streamlit**: A Streamlit server hosting the frontend application.

### Accessing the Services
- **Streamlit Interface**: Open your web browser and navigate to `http://localhost:8501` to access the Streamlit application.
- **Jupyter Notebooks**: Access Jupyter at `http://localhost:10000`. The server runs without a token for simplicity, but consider securing it for public or production environments.

### Shutting Down
To stop and remove the containers, use the following Docker Compose command:

`docker-compose down`

## Customizing Your Setup
Feel free to modify the Docker Compose configurations and Dockerfiles to match your specific requirements, such as changing exposed ports, adding new services, or tweaking environment variables.

## Contributing
Contributions to Sorting Hat are welcome! Please read our contributing guidelines and submit pull requests to our repository.

## License
Sorting Hat is released under the MIT License. See the LICENSE file in the repository for more details.
