import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to read names from text file
def read_names(filename):
    with open(filename, 'r') as file:
        names = [line.strip() for line in file]
    return names

# Function to generate a random email address
def generate_email(first_name, last_name):
    random_numbers = ''.join(random.choices(string.digits, k=5))
    email = f"{last_name}{first_name}{random_numbers}@gmail.com"
    return email

# Function to generate username
def generate_username(first_name, last_name):
    random_numbers = ''.join(random.choices(string.digits, k=5))
    username = f"{last_name}{first_name}{random_numbers}"
    return username

# Function to fill form with random names
def fill_form(first_names, last_names):
    # Set path to chromedriver.exe (adjust this path to where you have downloaded chromedriver)
    chromedriver_path = "C:/Users/meeee/Downloads/chromedriver-win64/chromedriver.exe"

    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode

    # Initialize the Chrome webdriver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    # URL of the Google account creation page
    url = "https://accounts.google.com/signup/v2/webcreateaccount?hl=en&flowName=GlifWebSignIn&flowEntry=SignUp"

    # Open the URL
    driver.get(url)

    try:
        # Explicit wait for the first name element
        wait = WebDriverWait(driver, 10)
        first_name_elem = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))

        # Find and fill first name field
        first_name = random.choice(first_names)
        first_name_elem.send_keys(first_name)
        first_name_elem.send_keys(Keys.ENTER)  # Press Enter after filling first name

        # Find and fill last name field (optional)
        last_name_elem = driver.find_element(By.ID, "lastName")
        last_name = random.choice(last_names)
        last_name_elem.send_keys(last_name)
        last_name_elem.send_keys(Keys.ENTER)  # Press Enter after filling last name

        # Generate email address
        email = generate_email(first_name, last_name)

        # Wait for the month dropdown to be clickable
        wait.until(EC.element_to_be_clickable((By.ID, "month")))
        
        # Select random month
        month_elem = driver.find_element(By.ID, "month")
        month_options = month_elem.find_elements(By.TAG_NAME, "option")
        random_month = random.choice(month_options)
        random_month.click()

        # Enter random day (1-27)
        day_elem = driver.find_element(By.ID, "day")
        day_elem.send_keys(str(random.randint(1, 27)))
        day_elem.send_keys(Keys.ENTER)  # Press Enter after filling day

        # Enter random year (18+)
        year_elem = driver.find_element(By.ID, "year")
        year_elem.send_keys(str(random.randint(1980, 2006)))  # Adjust the range for age requirement
        year_elem.send_keys(Keys.ENTER)  # Press Enter after filling year

        # Select gender (randomly choose Male or Female)
        gender_elem = driver.find_element(By.ID, "gender")
        gender_elem.click()  # Click on the gender dropdown to activate it

        # Simulate pressing down arrow keys to navigate options
        for _ in range(random.randint(1, 2)):
            gender_elem.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)  # Adjust sleep time as needed to allow dropdown options to load

        # Press Enter to select the option
        gender_elem.send_keys(Keys.ENTER)
        time.sleep(0.5)  # Wait for page to settle before proceeding

        # Click Next to proceed to email suggestion
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()

        # Wait for the email suggestions to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "t5nRo")))

        # Select the first email suggestion using JavaScript to avoid interception issues
        email_suggestion = driver.find_element(By.XPATH, '//div[@class="t5nRo Id5V1"]')
        driver.execute_script("arguments[0].click();", email_suggestion)

        # Click Next to proceed to username entry
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()

        # Wait for the username input field to be clickable
        username_elem = wait.until(EC.element_to_be_clickable((By.ID, "username")))

        # Generate username
        username = generate_username(first_name, last_name)

        # Fill username field
        username_elem.send_keys(username)
        username_elem.send_keys(Keys.ENTER)  # Press Enter after filling username

        # Click Next to proceed to password entry
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()

        # Enter password
        password_elem = driver.find_element(By.NAME, "Passwd")
        password_elem.send_keys("your_password_here")  # Replace with your desired password
        password_elem.send_keys(Keys.ENTER)  # Press Enter after filling password

        # Confirm password
        confirm_password_elem = driver.find_element(By.NAME, "PasswdAgain")
        confirm_password_elem.send_keys("your_password_here")  # Replace with your desired password again
        confirm_password_elem.send_keys(Keys.ENTER)  # Press Enter after filling confirm password

        # Click Next to complete registration
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()

        # Wait for the "confirm you are not a robot" page to appear (handle SMS verification manually)

        # Get selected details for saving
        selected_details = {
            "First Name": first_name,
            "Last Name": last_name,
            "Month": month_elem.text.strip(),
            "Day": day_elem.get_attribute("value"),
            "Year": year_elem.get_attribute("value"),
            "Gender": gender_elem.text.strip(),
            "Email": email,  # Use the generated email address
            "Username": username  # Add generated username to selected details
        }

        # Save selected details to a file (customize path and filename as needed)
        save_details(selected_details, "google_account_details.txt")

    except Exception as e:
        print(f"Error occurred: {e}")
        input("Press Enter to close the browser...")

    finally:
        pass
        #driver.quit()

def save_details(details, filename):
    with open(filename, 'a') as file:
        file.write("\n=== New Account Details ===\n")
        for key, value in details.items():
            file.write(f"{key}: {value}\n")

if __name__ == "__main__":
    # File paths for first and last names text files
    first_names_file = 'first_names.txt'
    last_names_file = 'last_names.txt'

    # Read names from text files
    first_names = read_names(first_names_file)
    last_names = read_names(last_names_file)

    # Fill the form with random names
    fill_form(first_names, last_names)
