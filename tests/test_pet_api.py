import requests
import allure
from conftest import BASE_URL, HEADERS, API_KEY


@allure.feature("Pet API")
@allure.story("Create Pet")
@allure.title("Positive Test: Create a new pet")
def test_create_pet(pet_data):
    """Test to create a new pet with valid data"""
    allure.attach(str(pet_data), name="Pet Data for Creation", attachment_type=allure.attachment_type.JSON)
    response = requests.post(BASE_URL, json=pet_data, headers=HEADERS)
    allure.attach(response.text, name="Creation Response", attachment_type=allure.attachment_type.TEXT)

    # Verify pet creation was successful and data matches
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == pet_data["name"]
    assert response_data["status"] == pet_data["status"]
    assert response_data["photoUrls"] == pet_data["photoUrls"]


@allure.feature("Pet API")
@allure.story("Retrieve Pet")
@allure.title("Positive Test: Get pet by ID")
def test_get_pet(pet_data):
    """Test to retrieve an existing pet by ID with full data validation"""
    pet_id = pet_data["id"]
    # Create the pet first
    requests.post(BASE_URL, json=pet_data, headers=HEADERS)

    # Retrieve the pet by ID
    response = requests.get(f"{BASE_URL}/{pet_id}", headers=HEADERS)
    allure.attach(f"Requesting pet with ID: {pet_id}", name="Request ID", attachment_type=allure.attachment_type.TEXT)
    allure.attach(response.text, name="Get Response", attachment_type=allure.attachment_type.TEXT)

    # Full data validation
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == pet_id
    assert response_data["name"] == pet_data["name"]
    assert response_data["status"] == pet_data["status"]
    assert response_data["category"] == pet_data["category"]
    assert response_data["photoUrls"] == pet_data["photoUrls"]
    assert response_data["tags"] == pet_data["tags"]


# Separate tests for each status in the findByStatus endpoint
@allure.feature("Pet API")
@allure.story("Retrieve Pets by Status")
@allure.title("Positive Test: Find pets by status 'available'")
def test_find_pets_by_status_available(create_pet_with_status):
    """Test to find pets with status 'available' and verify correct retrieval."""
    pet_available = create_pet_with_status("available")
    response = requests.get(f"{BASE_URL}/findByStatus?status=available", headers=HEADERS)
    allure.attach(response.text, name="Find by Status 'available' Response",
                  attachment_type=allure.attachment_type.TEXT)

    assert response.status_code == 200
    available_pets = response.json()
    assert any(pet["id"] == pet_available["id"] for pet in available_pets)
    assert all(pet["status"] == "available" for pet in available_pets)


@allure.feature("Pet API")
@allure.story("Retrieve Pets by Status")
@allure.title("Positive Test: Find pets by status 'pending'")
def test_find_pets_by_status_pending(create_pet_with_status):
    """Test to find pets with status 'pending' and verify correct retrieval."""
    pet_pending = create_pet_with_status("pending")
    response = requests.get(f"{BASE_URL}/findByStatus?status=pending", headers=HEADERS)
    allure.attach(response.text, name="Find by Status 'pending' Response", attachment_type=allure.attachment_type.TEXT)

    assert response.status_code == 200
    pending_pets = response.json()
    assert any(pet["id"] == pet_pending["id"] for pet in pending_pets)
    assert all(pet["status"] == "pending" for pet in pending_pets)


@allure.feature("Pet API")
@allure.story("Retrieve Pets by Status")
@allure.title("Positive Test: Find pets by status 'sold'")
def test_find_pets_by_status_sold(create_pet_with_status):
    """Test to find pets with status 'sold' and verify correct retrieval."""
    pet_sold = create_pet_with_status("sold")
    response = requests.get(f"{BASE_URL}/findByStatus?status=sold", headers=HEADERS)
    allure.attach(response.text, name="Find by Status 'sold' Response", attachment_type=allure.attachment_type.TEXT)

    assert response.status_code == 200
    sold_pets = response.json()
    assert any(pet["id"] == pet_sold["id"] for pet in sold_pets)
    assert all(pet["status"] == "sold" for pet in sold_pets)


@allure.feature("Pet API")
@allure.story("Retrieve Pet")
@allure.title("Negative Test: Get pet with invalid ID")
def test_get_pet_invalid_id():
    """Test to retrieve a pet using an invalid ID"""
    invalid_id = "invalid_id"
    response = requests.get(f"{BASE_URL}/{invalid_id}", headers=HEADERS)
    allure.attach(f"Requesting pet with invalid ID: {invalid_id}", name="Invalid ID Request",
                  attachment_type=allure.attachment_type.TEXT)
    allure.attach(response.text, name="Invalid ID Get Response", attachment_type=allure.attachment_type.TEXT)
    assert response.status_code == 404


@allure.feature("Pet API")
@allure.story("Update Pet")
@allure.title("Positive Test: Update pet's name and status")
def test_update_pet(pet_data):
    """Test to update a pet's name and status with valid data"""
    # Initial data for pet creation
    allure.attach(str(pet_data), name="Original Pet Data", attachment_type=allure.attachment_type.JSON)
    response = requests.post(BASE_URL, json=pet_data, headers=HEADERS)
    assert response.status_code == 200

    # Updating data
    pet_data["name"] = "Max"
    pet_data["status"] = "sold"
    allure.attach(str(pet_data), name="Updated Pet Data", attachment_type=allure.attachment_type.JSON)

    response = requests.put(BASE_URL, json=pet_data, headers=HEADERS)
    allure.attach(response.text, name="Update Response", attachment_type=allure.attachment_type.TEXT)

    assert response.status_code == 200
    assert response.json()["name"] == "Max"
    assert response.json()["status"] == "sold"


@allure.feature("Pet API")
@allure.story("Update Pet")
@allure.title("Negative Test: Update pet with invalid data")
def test_update_pet_invalid_data(pet_data):
    """Test to update a pet with invalid data, expecting failure"""
    response = requests.post(BASE_URL, json=pet_data, headers=HEADERS)
    assert response.status_code == 200
    pet_id = response.json()["id"]

    # Invalid update data
    invalid_data = {
        "id": pet_id,
        "name": "",  # Invalid empty name
        "status": "unknown123"  # Invalid status
    }
    allure.attach(str(invalid_data), name="Invalid Update Data", attachment_type=allure.attachment_type.JSON)

    # Perform the update request
    response = requests.put(BASE_URL, json=invalid_data, headers=HEADERS)
    allure.attach(response.text, name="Invalid Update Response", attachment_type=allure.attachment_type.TEXT)

    # Expecting a validation error response
    assert response.status_code in [400, 405]


@allure.feature("Pet API")
@allure.story("Delete Pet")
@allure.title("Positive Test: Delete pet by ID")
def test_delete_pet(pet_data):
    """Test to delete an existing pet by ID"""
    pet_id = pet_data["id"]
    requests.post(BASE_URL, json=pet_data, headers=HEADERS)
    response = requests.delete(f"{BASE_URL}/{pet_id}", headers={"api_key": API_KEY})
    allure.attach(f"Deleting pet with ID: {pet_id}", name="Delete Request ID",
                  attachment_type=allure.attachment_type.TEXT)
    allure.attach(response.text, name="Delete Response", attachment_type=allure.attachment_type.TEXT)
    assert response.status_code == 200


@allure.feature("Pet API")
@allure.story("Delete Pet")
@allure.title("Negative Test: Delete pet with invalid ID")
def test_delete_pet_invalid_id():
    """Test to delete a pet using an invalid ID"""
    invalid_id = "invalid_id"
    response = requests.delete(f"{BASE_URL}/{invalid_id}", headers={"api_key": API_KEY})
    allure.attach(f"Attempting to delete pet with invalid ID: {invalid_id}", name="Invalid ID Delete Request",
                  attachment_type=allure.attachment_type.TEXT)
    allure.attach(response.text, name="Invalid ID Delete Response", attachment_type=allure.attachment_type.TEXT)
    assert response.status_code == 404
