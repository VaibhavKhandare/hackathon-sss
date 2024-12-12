import os

import re
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)


def extract_page_content(url):
    """
    Fetch the webpage content and extract the main text.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse and extract the text content
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        return f"Error fetching the page: {str(e)}"


def analyze_with_openai(page_content):
    """
    Use OpenAI API to analyze the context of the webpage using the Chat API.
    """
    try:
        # Prepare a query for GPT using ChatCompletion (for GPT-4 or GPT-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" for better results
            messages=[
                {"role": "system",
                 "content": "You are an assistant that finds relevant brands based on website content."},
                {"role": "user",
                 "content": f"The webpage content: {page_content} \n\nCan you suggest a list of relevant brands and product categories matching the context? Respond as a list."}
            ]
        )

        # Extract the content from the assistant's reply
        output = response['choices'][0]['message']['content'].strip().split("\n")
        return False, output
    except Exception as e:
        return True, [f"Error analyzing content with OpenAI: {str(e)}"]


def obtain_banner_assets_url(suggested_brand, content):
    try:
        prompt = f'Create a banner advertisement image for "{suggested_brand}"'
        banner_image_response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
        return banner_image_response['data'][0]['url']
    except Exception as e:
        return [f"Error obtaining banner: {str(e)}"]


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to analyze a webpage and suggest related brands using OpenAI.
    """
    data = request.json
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'Please provide a valid website URL'}), 400

    # Extract webpage content
    content = extract_page_content(url)
    if content.startswith("Error"):
        return jsonify({'error': content}), 500  # Return error from webpage fetching

    # Analyze the content using OpenAI
    err, brands_response = analyze_with_openai(content)

    if err:
        return jsonify({'error': brands_response}), 500

    # Select a "suggested brand" (e.g., the first one from the returned list) if the list is non-empty
    suggested_brand = brands_response[2] if brands_response else "No suitable brand found"

    suggested_brand = re.sub(r'[^a-zA-Z\s]', '', suggested_brand)
    suggested_brand = suggested_brand.strip()

    banner_ad_url = obtain_banner_assets_url(suggested_brand, content) if brands_response else None

    # Return both the list of brands and the suggested brand in the response
    return jsonify({
        'url': url,
        'suggested_brands': brands_response,
        'suggested_brand': suggested_brand,
        'banner_ad_url': banner_ad_url
    })


if __name__ == '__main__':
    app.run(debug=True)
