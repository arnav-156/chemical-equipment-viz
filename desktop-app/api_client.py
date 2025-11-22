"""
API Client for Chemical Equipment Visualizer Desktop App
"""
import requests
import json


class APIClient:
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
    
    def set_token(self, token):
        """Set authentication token"""
        self.token = token
        self.session.headers.update({'Authorization': f'Token {token}'})
    
    def clear_token(self):
        """Clear authentication token"""
        self.token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def login(self, username, password):
        """Login user and get token"""
        url = f'{self.base_url}/auth/login/'
        response = requests.post(url, json={'username': username, 'password': password})
        response.raise_for_status()
        data = response.json()
        self.set_token(data['token'])
        return data
    
    def register(self, username, password, email=''):
        """Register new user"""
        url = f'{self.base_url}/auth/register/'
        response = requests.post(url, json={'username': username, 'password': password, 'email': email})
        response.raise_for_status()
        data = response.json()
        self.set_token(data['token'])
        return data
    
    def logout(self):
        """Logout user"""
        url = f'{self.base_url}/auth/logout/'
        try:
            self.session.post(url)
        except:
            pass
        finally:
            self.clear_token()
    
    def get_datasets(self):
        """Get list of datasets"""
        url = f'{self.base_url}/datasets/'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id):
        """Get specific dataset with equipment"""
        url = f'{self.base_url}/datasets/{dataset_id}/'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, dataset_id):
        """Get dataset summary statistics"""
        url = f'{self.base_url}/datasets/{dataset_id}/summary/'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def upload_csv(self, file_path, progress_callback=None):
        """Upload CSV file"""
        url = f'{self.base_url}/datasets/upload/'
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files)
        
        response.raise_for_status()
        return response.json()
    
    def download_report(self, dataset_id, save_path):
        """Download PDF report"""
        url = f'{self.base_url}/datasets/{dataset_id}/report/'
        response = self.session.get(url)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return save_path
