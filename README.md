# My Python Project

This is a Python project that can be run using Docker. It exposes a web application on port 5000 and utilizes a volume for development.

## Prerequisites

Before running the project, make sure you have the following software installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-project.git
   ```

2. Change into the project directory:

   ```cd your-project```

3. Save your Python code files inside the /path/to/local/code directory on your local machine.

4. Build the Docker image:

   ```docker build -t python-dev-image .```

5. Run the Docker container:
   ```docker run -d -p 5000:5000 -v "$(pwd)":/app --name py --restart unless-stopped python-dev-image```

The application will be accessible at http://localhost:5000.

6. Start developing your Python application. Any changes made to the code files in the /path/to/local/code directory will be reflected immediately in the running container.

7. To stop the container, use the following command:
   ```docker stop py```

You can start the container again using the docker start py command.

8. To re-compile, use following command:
   ```docker restart py```

