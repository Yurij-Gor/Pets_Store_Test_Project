import pytest
import requests
import random
import string
import allure

# Base URL and headers for the API
BASE_URL = "https://petstore.swagger.io/v2/pet"
HEADERS = {"Content-Type": "application/json"}
API_KEY = "special-key"  # API key for authentication


def generate_unique_id():
    """Generates a unique integer ID for pet testing purposes"""
    return random.randint(100000, 999999)


def generate_unique_name():
    """Generates a unique name for the pet by appending random letters"""
    return "Pet_" + ''.join(random.choices(string.ascii_letters, k=5))


@pytest.fixture(scope="session", autouse=True)
def cleanup_pets():
    """Fixture to clean up all pets created during the test session."""
    created_pet_ids = []  # List to store pet IDs

    # Yielding the list to allow tests to append pet IDs
    yield created_pet_ids

    # Cleanup: Attempt to delete each pet using its ID and check status
    cleanup_results = []  # Collect messages for Allure attachment

    for pet_id in created_pet_ids:
        response = requests.delete(f"{BASE_URL}/{pet_id}", headers={"api_key": API_KEY})

        # Check if the pet was successfully deleted or was already deleted
        if response.status_code == 200:
            message = f"Pet with ID {pet_id} successfully deleted."
        elif response.status_code == 404:
            message = f"Pet with ID {pet_id} was already deleted or does not exist."
        else:
            message = f"Unexpected status code {response.status_code} when deleting pet with ID {pet_id}"

        # Append message to results for Allure
        cleanup_results.append(message)

    # Attach cleanup summary to Allure report
    allure.attach("\n".join(cleanup_results), name="Cleanup Results", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture
def pet_data(cleanup_pets):
    """Fixture to provide unique pet data for testing CRUD operations."""
    # Generate unique data for the pet
    pet = {
        "id": generate_unique_id(),
        "category": {"id": 1, "name": "dog"},
        "name": generate_unique_name(),
        "photoUrls": ["https://cdn.britannica.com/92/212692-050-D53981F5/labradoodle-dog-stick-running-grass.jpg"],
        "tags": [{"id": 0, "name": "tag1"}],
        "status": "available"
    }

    # Append the pet ID to the cleanup list
    cleanup_pets.append(pet["id"])
    return pet


@pytest.fixture
def create_pet_with_status(cleanup_pets):
    """Fixture to create a pet with a specified status."""
    def _create_pet(status):
        pet = {
            "id": generate_unique_id(),
            "category": {"id": 1, "name": "dog"},
            "name": generate_unique_name(),
            "photoUrls": ["https://cdn.britannica.com/92/212692-050-D53981F5/labradoodle-dog-stick-running-grass.jpg"],
            "tags": [{"id": 1, "name": "tag1"}],
            "status": status
        }
        response = requests.post(BASE_URL, json=pet, headers=HEADERS)
        assert response.status_code == 200
        cleanup_pets.append(pet["id"])  # Register pet ID for cleanup
        allure.attach(str(pet), name="Created Pet Data", attachment_type=allure.attachment_type.JSON)
        return pet
    return _create_pet
