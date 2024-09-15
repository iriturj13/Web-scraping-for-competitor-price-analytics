import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to modify the image URL by removing the last part
def modify_image_url(image_url):
    if image_url:
        split_url = image_url.split('._')
        if len(split_url) > 1:
            return split_url[0] + '.jpg'
    return image_url

# Function to extract Amazon image URLs from a given URL
def get_image_urls(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Initialize list to store image URLs
    image_urls = []

    # Find the div element with id 'altImages'
    alt_images_div = soup.find("div", {"id": "altImages"})

    if alt_images_div:
        # Find all img elements within the div
        image_elements = alt_images_div.find_all("img")

        # Iterate through the image elements and modify the source URLs
        for image in image_elements:
            image_url = image.get("src")

            # Modify the image URL by removing the last part
            modified_url = modify_image_url(image_url)
            image_urls.append(modified_url)

        return image_urls
    else:
        return None


# Read URLs from Excel file
input_excel_path = "/content/Links.xlsx"
df_urls = pd.read_excel(input_excel_path, sheet_name="Amazon")  # Adjust sheet name if necessary

# Initialize the data for the output Excel file
data = []

# Iterate through each URL and scrape the image URLs
for index, row in df_urls.iterrows():
    url = row['link']
    image_urls = get_image_urls(url)
    if image_urls:
        row_data = [url] + image_urls[:10] + [''] * (10 - len(image_urls))
        data.append(row_data)
        print(f"Amazon Link: {url}")
        print(f"Image URLs: {image_urls}")
    else:
        row_data = [url] + [''] * 10
        data.append(row_data)
        print(f"Amazon Link: {url}")
        print("No images found.")

# Create a DataFrame and save to an Excel file
output_excel_path = "amazon_image_links_output.xlsx"
column_names = ["Amazon Link"] + [f"Image URL {i+1}" for i in range(10)]
df_output = pd.DataFrame(data, columns=column_names)
df_output.to_excel(output_excel_path, index=False)

print(f"Excel file has been created: {output_excel_path}")
