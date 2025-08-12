# Book-Alchemy: A Flask Digital Library

This project is a simple digital library web application built with Python, Flask, and SQLAlchemy. It was created as part of a [Masterschool.com](https://masterschool.com/) course to demonstrate foundational web development concepts with the Flask micro-framework.

## Project Status & Disclaimer

This project is intended primarily for **educational purposes**. It serves as a practical exercise in understanding routing, database interactions with an ORM, and basic templating in Flask.

-   **Steep Learning Curve:** The project can be challenging, especially for those new to Flask, SQLAlchemy, or web development concepts.
-   **Not Production-Ready:** This application is not designed for a production environment. It lacks scalability, advanced security features, and the robustness required for a public-facing application.
-   **Efficiency:** For a real-world, efficient, and scalable digital library, it would be more practical to use existing, mature tools and frameworks. However, for learning the fundamentals from the ground up, this project is a valuable exercise.

## Setup and Running the Application

To get the application running on your local machine, follow these steps:

1.  **Create and Activate a Virtual Environment:** It is highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    # Create a virtual environment named .venv
    python3 -m venv .venv

    # Activate it (on macOS/Linux)
    source .venv/bin/activate
    ```

2.  **Install Dependencies:** All required Python packages are listed in the `requirements.txt` file.

    ```bash
    # Install the packages
    pip install -r requirements.txt
    ```

3.  **Run the Server:** A simple shell script is provided to start the Flask development server. This derives from the exercise: 

    ```bash
    # Run the server
    python3 -m flask app
    ```

Once the server is running, you can access the application in your web browser at the address provided in the terminal (usually `http://127.0.0.1:5000`).
