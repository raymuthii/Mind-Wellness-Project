import requests
import json
from typing import Dict, Any, Optional

class TestDonationFlow:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.test_amount = 10.00
        self.auth_token = None
    
    def login(self, email: str = "test@example.com", password: str = "test123") -> Optional[str]:
        """Get authentication token"""
        print("\nGetting authentication token...")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data['access_token']
                self.headers["Authorization"] = f"Bearer {self.auth_token}"
                print("✅ Successfully got auth token")
                return self.auth_token
            else:
                print(f"❌ Failed to get auth token: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting auth token: {str(e)}")
            return None
    
    def create_donation(self) -> Dict[str, Any]:
        """Test creating a new donation"""
        print("\nTesting donation creation...")
        
        payload = {
            "amount": self.test_amount,
            "is_recurring": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/donations/",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Successfully created donation")
                print(f"Donation ID: {data['id']}")
                print(f"Checkout URL: {data['checkout_url']}")
                return data
            else:
                print(f"❌ Failed to create donation: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating donation: {str(e)}")
            return None
    
    def get_donation(self, donation_id: str) -> Dict[str, Any]:
        """Test retrieving a specific donation"""
        print(f"\nRetrieving donation {donation_id}...")
        
        try:
            response = requests.get(
                f"{self.base_url}/donations/{donation_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Successfully retrieved donation")
                print(f"Status: {data['status']}")
                return data
            else:
                print(f"❌ Failed to retrieve donation: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving donation: {str(e)}")
            return None

def main():
    # Initialize test flow
    test = TestDonationFlow()
    
    # Get authentication token
    if not test.login():
        print("❌ Test failed: Could not get authentication token")
        return
    
    # Create a donation
    donation_data = test.create_donation()
    if not donation_data:
        print("❌ Test failed: Could not create donation")
        return
    
    # Get the donation details
    donation = test.get_donation(donation_data['id'])
    if not donation:
        print("❌ Test failed: Could not retrieve donation")
        return
    
    print("\n✅ Test completed successfully!")
    print("\nTo complete the payment flow:")
    print(f"1. Open this URL in your browser: {donation_data['checkout_url']}")
    print("2. Use test card number: 4242 4242 4242 4242")
    print("3. Use any future date for expiry")
    print("4. Use any 3 digits for CVC")
    print("5. Use any value for other fields")

if __name__ == "__main__":
    main() 