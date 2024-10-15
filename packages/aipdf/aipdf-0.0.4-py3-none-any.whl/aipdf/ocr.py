import io
import base64
import logging
import concurrent.futures

from pdf2image import convert_from_bytes
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_PROMPT = """
Extract the full markdown text from the given image, following these guidelines:
- Respond only with markdown, no additional commentary.  
- Capture all the text, respecting titles, headers, subheaders, equations, etc.
- If there are tables in this page, convert each one into markdown table format and include it in the response.
- If there are images, provide a brief description of what is shown in each image, and include it in the response.
- if there are charts, for each chart include a markdown table with the data represents the chart, a column for each of the variables of the cart and the relevant estimated values
          
"""

def process_image_to_markdown(file_object, client, model="gpt-4o",  prompt = DEFAULT_PROMPT):
    """
    Process a single image file and convert its content to markdown using OpenAI's API.

    Args:
        file_object (io.BytesIO): The image file object.
        client (OpenAI): The OpenAI client instance.
        model (str, optional): by default is gpt-4o
        prompt (str, optional): The prompt to send to the API. Defaults to DEFAULT_PROMPT.

    Returns:
        str: The markdown representation of the image content, or None if an error occurs.
    """
    # Log that we're about to process a page
    logging.info("About to process a page")

    base64_image = base64.b64encode(file_object.read()).decode('utf-8')
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
        
        # Extract the markdown content from the response
        markdown_content = response.choices[0].message.content
        logging.info("Page processed successfully")
        return markdown_content
    
    except Exception as e:
        logging.error(f"An error occurred while processing the image: {e}")
        return None

    
def pdf_to_image_files(pdf_file):
    """
    Convert a PDF file to a list of image file objects.

    Args:
        pdf_file (io.BytesIO): The PDF file object.

    Returns:
        list: A list of io.BytesIO objects, each containing a page of the PDF as a PNG image.
    """
    # Read the PDF file content
    pdf_content = pdf_file.read()
    
    # Convert PDF pages to images
    images = convert_from_bytes(pdf_content)
    
    # List to store image file objects
    image_files = []
    
    # Process each image
    for i, image in enumerate(images):
        # Create a byte stream to store the image
        img_byte_arr = io.BytesIO()
        
        # Save the image as PNG to the byte stream
        image.save(img_byte_arr, format='PNG')
        
        # Seek to the beginning of the stream
        img_byte_arr.seek(0)
        
        # Create a file-like object and add it to the list
        image_file = io.BytesIO(img_byte_arr.getvalue())
        image_file.name = f"page_{i+1}.png"
        image_files.append(image_file)
        
    
    return image_files


def ocr(pdf_file, api_key, model="gpt-4o", base_url= 'https://api.openai.com/v1', prompt=DEFAULT_PROMPT, pages_list = None):
    """
    Convert a PDF file to a list of markdown-formatted pages using OpenAI's API.

    Args:
        pdf_file (io.BytesIO): The PDF file object.
        api_key (str): The OpenAI API key.
        model (str, optional): by default is gpt-4o
        base_url (str): You can use this one to point the client whereever you need it like Ollama
        prompt (str, optional): The prompt to send to the API. Defaults to DEFAULT_PROMPT.
        pages_list (list, optional): A list of page numbers to process. If provided, only these pages will be converted. Defaults to None, which processes all pages.
    Returns:
        list: A list of strings, each containing the markdown representation of a PDF page.
    """
    client = OpenAI(api_key=api_key, base_url = base_url)  # Create OpenAI client
    # Convert PDF to image files
    image_files = pdf_to_image_files(pdf_file)

    if pages_list:
        # Filter image_files to only include pages in page_list
        image_files = [img for i, img in enumerate(image_files) if i + 1 in pages_list]
    
    # List to store markdown content for each page
    markdown_pages = [None] * len(image_files)

    # Process each image file in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks for each image file
        future_to_page = {executor.submit(process_image_to_markdown, img_file, client, model, prompt): i 
                          for i, img_file in enumerate(image_files)}
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_page):
            page_num = future_to_page[future]
            try:
                markdown_content = future.result()
                if markdown_content:
                    markdown_pages[page_num] = markdown_content
                else:
                    markdown_pages[page_num] = f"Error processing page {page_num + 1}."
            except Exception as e:
                logging.error(f"Error processing page {page_num + 1}: {e}")
                markdown_pages[page_num] = f"Error processing page {page_num + 1}: {str(e)}"

    return markdown_pages


