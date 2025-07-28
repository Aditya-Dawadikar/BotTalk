import requests

BASE_URL = "http://localhost:8001"  # Change this to your API server URL


def create_job(job_data: dict):
    """
    Call the /jobs/create API endpoint to create a job.
    
    :param job_data: Dictionary containing job details (e.g., {"title": "My Job", "status": "pending"})
    :return: JSON response from the API
    """
    url = f"{BASE_URL}/jobs/create"
    response = requests.post(url, json=job_data)

    if response.status_code != 200:
        raise Exception(f"Failed to create job: {response.status_code} - {response.text}")

    return response.json()


def update_job(job_id: str, update_fields: dict):
    """
    Call the /jobs/update/{job_id} API endpoint to update a job.
    
    :param job_id: Document ID of the job to update
    :param update_fields: Dictionary of fields to update (e.g., {"status": "completed"})
    :return: JSON response from the API
    """
    url = f"{BASE_URL}/jobs/update/{job_id}"
    response = requests.put(url, json=update_fields)

    if response.status_code != 200:
        raise Exception(f"Failed to update job: {response.status_code} - {response.text}")

    return response.json()
