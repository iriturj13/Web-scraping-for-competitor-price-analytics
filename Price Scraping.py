import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os

# Function to log in to the website
# Function to log in to the website
def login(driver):
    driver.get('https://www.build.com/account/login')

    # Find the parent div for email directly
    email_parent_div = driver.find_element(By.CLASS_NAME, "border-box.db.w-100.b")

    if email_parent_div:
        # Find the email input within the email parent div
        email_input = email_parent_div.find_element(By.CLASS_NAME, "input-reset.input.br2.f5.ph3.ba.w-100.truncate.input.f5.theme-grey-dark.b--theme-grey")

        if email_input:
            # Enter email
            email_input.send_keys("")
            print("Email input found and value entered.")
        else:
            print("Email input not found.")

    # Find the parent div for password directly
    password_parent_div = driver.find_element(By.CLASS_NAME, "border-box.db.w-100.b.mt2")

    if password_parent_div:
        # Find the password input within the password parent div
        password_input = password_parent_div.find_element(By.ID, "password")

        if password_input:
            # Enter the password
            password_input.send_keys("")  # replace with actual password
            print("Password input found and value entered.")
        else:
            print("Password input not found.")

        # Find the login button by its class name and click it
        login_button = driver.find_element(By.CLASS_NAME, "pointer.ba.br2.w-inherit.fw4.bg-theme-primary.theme-white.b--theme-primary.hover-bg-theme-primary-dark.hover-theme-white.hover-b--theme-primary-dark.active-bg-theme-primary-darker.active-b--theme-primary-darker.input.f5.ph4")

        if login_button:
            login_button.click()
            print("Login button found and clicked.")
            time.sleep(30)  # Wait for login to complete
        else:
            print("Login button not found.")
    else:
        print("Password parent div not found.")


# Function to scrape titles and prices
def scrape_titles_and_prices(driver, input_file):
    # Read the Excel file containing product links
    df = pd.read_excel(input_file)

    # Function to scrape title and price for a given link
    def scrape_title_and_price(link):
        try:
            # Go to the provided link
            driver.get(link)
            # Allow the page to load completely
            time.sleep(5)

            # Get the page source
            page_source = driver.page_source
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find the title element
            title_element = soup.find('h1', class_='ma0 fw6 lh-title di f5 f3-ns')
            title = title_element.text.strip() if title_element else "Title not found"

            # Find the price element
            price_element = soup.find('div', class_='lh-title b theme-emphasis f4 f3-ns mr2', attrs={'data-automation': 'price'})
            if not price_element:
                price_element = soup.find('span', class_='lh-title b theme-emphasis f4 f3-ns mr2', attrs={'data-automation': 'price'})

            price = price_element.text.strip() if price_element else "Price not found"

            return title, price
        except Exception as e:
            print(f"An error occurred while scraping {link}: {e}")
            return "Error", "Error"

    # Scraping titles and prices
    results = []
    for index, row in df.iterrows():
        link = row['Link']
        title, price = scrape_title_and_price(link)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results.append([link, title, price, timestamp])

    # Create a DataFrame from the results
    output_df = pd.DataFrame(results, columns=['Link', 'Title', 'Price', 'Timestamp'])

    # Output file name with unique timestamp
    output_file = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    # Write the DataFrame to Excel
    output_df.to_excel(output_file, index=False)

    # Provide the link to download the Excel file
    print(f"Scraped data has been saved to the Excel file: {output_file}")

def main():
    # Initialize the undetected Chrome driver
    options = uc.ChromeOptions()
    chrome_version = 125
    driver = uc.Chrome(options=options,version_main=chrome_version)

     # Get input file path from user input
    input_file = input("Enter the path to the Excel file containing product links: ")

    # Perform login
    login(driver)

   
    # Scrape titles and prices
    scrape_titles_and_prices(driver, input_file)

if __name__ == '__main__':
    main()
