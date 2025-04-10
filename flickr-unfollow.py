import flickrapi
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with your Flickr API key and secret.
API_KEY = 'YOUR API KEY HERE'
API_SECRET = 'YOUR SECRET KEY HERE'

# Replace with your Flickr login credentials.
FLICKR_USERNAME = "YOUR USERNAME HERE"
FLICKR_PASSWORD = "YOUR PASSWORD HERE"

# Function used for unfollowing people.
def unfollow_contact(driver, contact_nsid):
    # Creating the template URL for the user.
    profile_url = f"https://www.flickr.com/people/{contact_nsid}/"
    print(f"Accessing page for {contact_nsid}...")

    # Accessing their webpage, and waiting for the page to load.
    driver.get(profile_url)
    time.sleep(1.5)
    
    try:
        # Wait for the "Following" button to appear.
        following_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.following-flickr-user-button"))
        )
        print("Found 'Following' button, clicking it to unfollow.")
        
        # Clicking the "Following" button so that we unfollow.
        following_button.click()
        print(f"Clicked 'Following' button for {contact_nsid} (unfollowed).")
    except Exception as e:
        print(f"Error unfollowing contact {contact_nsid}: {e}")

# Getting all useres from the "Following" list on your profile.
def get_contacts_to_unfollow():
    # Using the keys here.
    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')
    flickr.authenticate_via_browser(perms='read')
    
    # Logging in using the API.
    my_info = flickr.test.login()
    my_nsid = my_info['user']['id']
    
    # Will be used to get your "contacts".
    print(f"My NSID (ID): {my_nsid}")
    
    # This gets how many people that you're following. The Flickr API calls your "Following" count
    # as your "contacts". A little name discrepancy here.
    contacts_resp = flickr.contacts.getList(user_id=my_nsid)
    contacts = contacts_resp.get('contacts', {}).get('contact', [])
    print(f"Found {len(contacts)} contacts.")
    
    # Creating an empty list of people who we will unfollow.
    contacts_to_unfollow = []
    
    # Iterating through everyone that we're following.
    for contact in contacts:
        # Getting their NSID and their username.
        contact_nsid = contact['nsid']
        username = contact.get('username', 'Unknown')
        print(f"\nChecking if {username} (NSID: {contact_nsid}) follows you back...")
        
        # Accessing their webpage and checks to see if your NSID is on their "contacts" page.
        try:
            their_contacts_resp = flickr.contacts.getPublicList(user_id=contact_nsid)
            their_contacts = their_contacts_resp.get('contacts', {}).get('contact', [])
            follows_me_back = any(c.get('nsid') == my_nsid for c in their_contacts)
        except Exception as e:
            print(f"  Error retrieving {username}'s contacts: {e}")
            # Assume not following back on error.
            follows_me_back = False  
        
        # Appending them to the list of people that are not following you back.
        if not follows_me_back:
            print(f"  -> {username} does NOT follow you back.")
            contacts_to_unfollow.append(contact_nsid)

        # Otherwise, continue to follow them.
        else:
            print(f"  -> {username} follows you back. Keeping them.")
        
        # Pause to respect API rate limits.
        time.sleep(1)
    
    return contacts_to_unfollow

# Logging into Flickr with the username and password.
def login_flickr(driver, username, password):
    # Opening the website.
    driver.get("https://www.flickr.com/signin")
    time.sleep(2)
    
    # Filling in the email which was a constant from above.
    email_input = driver.find_element(By.ID, "login-email")
    email_input.send_keys(username)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    
    # Doing the same with the password. Giving some extra sleep time so that
    # Flickr can process this request.
    password_input = driver.find_element(By.ID, "login-password")
    password_input.send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(5)


def main():
    # First, we will build a list of people that we will unfollow.
    contacts_to_unfollow = get_contacts_to_unfollow()
    print("\nContacts to unfollow:", contacts_to_unfollow)
    
    # Initialize the Selenium WebDriver (e.g., using Chrome; ensure you have chromedriver installed).
    driver = webdriver.Chrome()
    
    # Attempt to log into the page through Selenium WebDriver.
    try:
        # Log into Flickr using Selenium. This opens an application.
        login_flickr(driver, FLICKR_USERNAME, FLICKR_PASSWORD)
        
        # Unfollow each contact that doesn't follow you back.
        for nsid in contacts_to_unfollow:
            unfollow_contact(driver, nsid)
            time.sleep(2)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()