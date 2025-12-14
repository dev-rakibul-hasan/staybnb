import requests
import re

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/accounts/login/"
LOGOUT_URL = f"{BASE_URL}/accounts/logout/"

def check_links(html, role):
    required = []
    forbidden = []
    
    if role == "logged_out":
        required = ["Home", "Search", "Login", "Sign Up"]
        forbidden = ["My Bookings", "My Listings", "Add Listing", "Booking Requests", "Logout"]
    elif role == "guest":
        required = ["Home", "Search", "My Bookings", "Logout"]
        forbidden = ["Login", "Sign Up", "My Listings", "Add Listing", "Booking Requests"]
    elif role == "host":
        required = ["Home", "My Listings", "Add Listing", "Booking Requests", "Logout"]
        forbidden = ["Login", "Sign Up", "My Bookings"] # 'Search' removed from host menu in user req?
        # User req for Host: "Home | My Listings | Add Listing | Booking Requests | Logout"
        # Search is NOT in host menu per request.
        
    print(f"Checking {role} menu...")
    missing = [link for link in required if f">{link}<" not in html and f">{link}</a>" not in html] 
    # simple check, might need regex if attributes differ. 
    # Base html has <a href="...">Link</a>.
    
    unexpected = [link for link in forbidden if f">{link}<" in html or f">{link}</a>" in html]
    
    if missing:
        print(f"FAILED: Missing links for {role}: {missing}")
    if unexpected:
        print(f"FAILED: Unexpected links for {role}: {unexpected}")
    
    if not missing and not unexpected:
        print(f"PASSED: {role} menu looks correct.")

def run_test():
    s = requests.Session()
    
    # 1. Logged Out
    r = s.get(BASE_URL)
    check_links(r.text, "logged_out")
    
    # 2. Login Guest
    # Need a guest user. guest_browser@test.com / password123 (from previous task)
    csrftoken = s.cookies.get('csrftoken', '')
    if not csrftoken:
         r = s.get(LOGIN_URL)
         csrftoken = s.cookies.get('csrftoken')
         
    login_data = {
        'identifier': 'guest_browser@test.com',
        'password': 'password123',
        'csrfmiddlewaretoken': csrftoken
    }
    headers = {'Referer': LOGIN_URL}
    s.post(LOGIN_URL, data=login_data, headers=headers)
    
    r = s.get(BASE_URL)
    check_links(r.text, "guest")
    
    # 3. Logout
    s.get(LOGOUT_URL)
    r = s.get(BASE_URL)
    # Should be back to logged out
    check_links(r.text, "logged_out")
    
    # 4. Login Host
    # Need a host user. host_browser@test.com / password123
    r = s.get(LOGIN_URL)
    csrftoken = s.cookies.get('csrftoken')
    login_data['identifier'] = 'host_browser@test.com'
    login_data['csrfmiddlewaretoken'] = csrftoken
    s.post(LOGIN_URL, data=login_data, headers={'Referer': LOGIN_URL})
    
    r = s.get(BASE_URL)
    check_links(r.text, "host")

if __name__ == "__main__":
    run_test()
