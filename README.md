# Flickr Unfollow Bot  
*Easily remove those who don't follow you back.*

This Python script automates the process of unfollowing users on Flickr who don't follow you back. Using Selenium and Flickr's API, it logs into your account, checks your following list, and removes users who aren't following you in return.

---

### Features:
- Automatically identifies non-mutual followers on your Flickr account.
- Uses browser automation (Selenium with Chromium) to unfollow users.
- Simple to use—just configure your API keys and run the script.

---

### Prerequisites
Before running the script, make sure you have the following installed:

- **Python** (preferably Python 3.x)
- **Selenium**: For browser automation
- **Chromium/Chrome**: Selenium requires a web browser to automate actions.
- **Flickr API Key & Secret**: You can obtain these from [Flickr API Keys](https://www.flickr.com/services/api/misc.api_keys.html).

---

### Setup

1. **Obtain your Flickr API key and secret**  
   Visit [Flickr API Key Registration](https://www.flickr.com/services/api/misc.api_keys.html) and get your API key and secret.

2. **Configure the script**  
   Open the `flickr-unfollow.py` file and insert your Flickr API key and secret in the respective fields at the top of the script.  
   Additionally, input your **Flickr username (email)** and **password**.

3. **Run the script**  
   Open your terminal and navigate to the folder where you've saved the script. Then, run it with the following command:
   ```bash
   python -u flickr-unfollow.py

---

### How it Works

1. **Authenticate and Sign In**
The script uses the Flickr API to sign in to your account using the provided API key and secret.

2. **Gather Following List**
It fetches your following list—these are the people you are following.

3. **Identify Non-Mutual Followers**
The script checks who you follow, but who isn’t following you back.

4. **Browser Automation (Selenium)**
Once non-mutual followers are identified, the script opens a Chromium browser (via Selenium) and logs into your Flickr account.

5. **Unfollow Non-Mutual Followers**
The script automatically unfollows those who don’t follow you back.


---

### Notes

- Flickr API Limitations: Unfortunately, Flickr doesn't allow direct unfollowing through their API. Therefore, browser automation is used to handle this process.

- Browser Automation: This may not be the most elegant solution, but it gets the job done!

---

### Troubleshooting

If you encounter issues with browser automation, ensure that you have the correct version of Chromium or Chrome installed and that it's compatible with the version of Selenium you're using.

---

### Contact

For any questions or issues, feel free to reach out: eric56379@gmail.com
