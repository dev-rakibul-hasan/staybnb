import requests
import os

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/accounts/login/"
ADD_LISTING_URL = f"{BASE_URL}/listing/add/"

# Credentials
EMAIL = "host_browser@test.com"
PASSWORD = "password123"

def run_test():
    s = requests.Session()
    
    # 1. Get Login Page (to get CSRF cookie)
    print("Fetching login page...")
    r = s.get(LOGIN_URL)
    csrf_token = s.cookies.get('csrftoken')
    if notHOwever, in Django, the CSRF token for POST is usually required in the form data 'csrfmiddlewaretoken'.
    # We can perform a naive extraction or just use the cookie if 'django.middleware.csrf.CsrfViewMiddleware' is used,
    # but usually the form needs the hidden field.
    # Let's try to pass it in headers 'X-CSRFToken' which works for AJAX, might work here if view supports it.
    
    headers = {
        'Referer': LOGIN_URL,
        'X-CSRFToken': csrf_token
    }

    # 2. Login
    print("Logging in...")
    login_data = {
        'identifier': EMAIL,
        'password': PASSWORD,
        'csrfmiddlewaretoken': csrf_token # Attempting to use cookie value as token
    }
    r = s.post(LOGIN_URL, data=login_data, headers=headers)
    
    if "Host Dashboard" in r.text or "Welcome back" in r.text or r.url.endswith("dashboard/"):
        print("Login Successful")
    else:
        print("Login Failed")
        print(r.text[:500])
        # Proceeding anyway? No, login needed.
        return

    # 3. Create Listing
    print("Creating Listing...")
    listing_data = {
        'title': 'Scripted Cozy Cottage',
        'description': 'Created by python script',
        'address': 'Script Lane',
        'city': 'Scriptville',
        'country': 'Codeland',
        'price': '99',
        'guests': '2',
        'csrfmiddlewaretoken': s.cookies.get('csrftoken')
    }
    
    # files = {'image': open('test_image.png', 'rb')} # skipping image for simplicity or use generated one
    
    headers['Referer'] = ADD_LISTING_URL
    r = s.post(ADD_LISTING_URL, data=listing_data, headers=headers)
    
    if "Listing added successfully" in r.text:
        print("Listing Creation Successful")
    else:
        print("Listing Creation Failed")
        print(r.status_code)
        print(r.text[:500])

if __name__ == "__main__":
    run_test()
