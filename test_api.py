"""
Simple script to test the API endpoints
Run the Django server first: python manage.py runserver
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_login():
    """Test login endpoint"""
    print("\n=== Testing Login ===")
    response = requests.post(f'{BASE_URL}/auth/login/', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('token')

def test_upload(token):
    """Test CSV upload"""
    print("\n=== Testing CSV Upload ===")
    headers = {'Authorization': f'Token {token}'}
    
    with open('sample_equipment_data.csv', 'rb') as f:
        files = {'file': f}
        response = requests.post(f'{BASE_URL}/datasets/upload/', 
                                headers=headers, 
                                files=files)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json().get('id')

def test_list_datasets(token):
    """Test list datasets"""
    print("\n=== Testing List Datasets ===")
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/datasets/', headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_dataset(token, dataset_id):
    """Test get specific dataset"""
    print(f"\n=== Testing Get Dataset {dataset_id} ===")
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/datasets/{dataset_id}/', headers=headers)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Dataset: {data['file_name']}")
    print(f"Equipment count: {len(data['equipment_items'])}")
    print(f"Summary: {json.dumps(data['summary'], indent=2)}")

def test_get_summary(token, dataset_id):
    """Test get summary"""
    print(f"\n=== Testing Get Summary {dataset_id} ===")
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/datasets/{dataset_id}/summary/', headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_download_report(token, dataset_id):
    """Test PDF report generation"""
    print(f"\n=== Testing PDF Report {dataset_id} ===")
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/datasets/{dataset_id}/report/', headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        with open('test_report.pdf', 'wb') as f:
            f.write(response.content)
        print("PDF saved as test_report.pdf")

if __name__ == '__main__':
    try:
        # Test login
        token = test_login()
        
        if token:
            # Test upload
            dataset_id = test_upload(token)
            
            # Test list
            test_list_datasets(token)
            
            if dataset_id:
                # Test get dataset
                test_get_dataset(token, dataset_id)
                
                # Test summary
                test_get_summary(token, dataset_id)
                
                # Test PDF report
                test_download_report(token, dataset_id)
        
        print("\n=== All tests completed ===")
    
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server.")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\nError: {e}")
