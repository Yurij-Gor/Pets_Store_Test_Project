# Pets Store Test Project

## Description
This project is designed for automated API testing. The tests are written in Python using the `pytest` framework and use `Allure` for test reporting. The project is containerized with Docker to ensure compatibility and ease of deployment. Additionally, the project is integrated with GitHub Actions for continuous integration, which automatically runs tests and generates reports on each push or pull request to the main branch.

The API documentation used for testing can be found here:  
[Pet Store API Documentation](https://petstore.swagger.io/)

## Test Results
View the Allure Test Report:  
[Allure Report](https://yurij-gor.github.io/Pets_Store_Test_Project/)

## Technologies
This project utilizes the following technologies:

- **Python 3.x**: The programming language for writing tests.
- **Requests**: HTTP client for making API calls.
- **Pytest**: A framework for writing and executing tests.
- **Allure**: A reporting tool for generating detailed test reports.
- **Docker**: Used for containerization to isolate the testing environment.
- **GitHub Actions**: CI/CD for automatically running tests and generating reports, with the results published to GitHub Pages.

## Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/Yurij-Gor/Pets_Store_Test_Project
cd Pets_Store_Test_Project
pip install -r requirements.txt
```

## Running Tests

To run the tests and generate a report, execute the following command:

```bash
pytest --alluredir=test_results/ tests/
```

After running the tests, create a report by running:

```bash
allure serve test_results
```

### Running Tests with Docker
To run the tests in a Docker container, use the following commands:

```bash
# Stop and remove any running containers
docker-compose down

# Build and start the project using docker-compose
docker-compose up --build
```

To copy the Allure report from the Docker container to your local machine and open it:

```bash
# Replace <LocalPathToStoreResults> with the local path where you want to store the test results
docker cp pytest_runner_container:/tests_project/test_results <LocalPathToStoreResults>

# To serve the Allure report, navigate to the directory where the results are stored and run:
allure serve <LocalPathToStoreResults>/test_results
```
Remember to clean up after your Docker environment once you're done:
```bash
docker-compose down
```
Ensure to replace &lt;LocalPathToStoreResults&gt; with the actual paths and names relevant to your project.

## GitHub Actions Workflow
The CI/CD pipeline is defined in `.github/workflows/ci.yml`

## Project Structure

The project has the following structure:

```
Pets_Store_Test_Project/
├── .github/workflows/      # CI/CD files for GitHub Actions
│   └── ci.yml              # CI/CD configuration
├── tests/                  # Directory with test files
│   ├── __init__.py         
│   └── test_pet_api.py     # Tests for the Pets API
├── test_results/           # Directory for test results
├── .gitignore              # Files and folders ignored by Git
├── Dockerfile              # Dockerfile for containerizing the project
├── docker-compose.yml      # Docker Compose file for managing containers
├── conftest.py             # Pytest configuration file
└── requirements.txt        # Project dependencies
```

## Additional Notes

The repository is configured to automatically generate reports using GitHub Actions, which are published on GitHub Pages in the `gh-pages` branch.

Refer to the [Pet Store API Documentation](https://petstore.swagger.io/) for more details on the API endpoints and expected request/response formats.