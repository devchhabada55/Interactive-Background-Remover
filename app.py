import os
import io
import logging
import requests
import base64
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from rembg import remove
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Directory setup
OUTPUT_DIR = os.path.join(os.getcwd(), 'static')
os.makedirs(OUTPUT_DIR, exist_ok=True)

class ImageProcessingError(Exception):
    """Custom exception for image processing errors"""
    pass

def download_image(url):
    """Download an image from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to download image: {e}")

def crop_image(image_data, bounding_box=None):
    """Crop the image based on the bounding box"""
    try:
        image = Image.open(image_data)

        if not bounding_box:
            # Return raw image bytes if no cropping is needed
            cropped_bytes = io.BytesIO()
            image.save(cropped_bytes, format="PNG")
            cropped_bytes.seek(0)
            return cropped_bytes

        x_min = bounding_box.get("x_min", 0)
        y_min = bounding_box.get("y_min", 0)
        x_max = bounding_box.get("x_max", image.width)
        y_max = bounding_box.get("y_max", image.height)

        cropped_image = image.crop((x_min, y_min, x_max, y_max))
        cropped_bytes = io.BytesIO()
        cropped_image.save(cropped_bytes, format="PNG")
        cropped_bytes.seek(0)
        return cropped_bytes
    except Exception as e:
        raise ValueError(f"Failed to crop image: {e}")

@app.route("/")
def home():
    return render_template("Homepage.html")  # Ensure this matches your HTML template

@app.route("/remove-background", methods=["POST"])
def remove_background_from_image():
    """Handle background removal from an image"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        image_url = data.get("image_url")
        bounding_box = data.get("bounding_box")

        if not image_url:
            return jsonify({"error": "Missing image URL"}), 400

        # Download the image
        image_data = download_image(image_url)

        # Crop the image if bounding box is provided
        cropped_image_data = crop_image(image_data, bounding_box)

        # Remove the background
        cropped_image_data.seek(0)  # Ensure the pointer is at the start
        processed_image_data = remove(cropped_image_data.read())

        # Save the processed image to the server
        processed_image_path = os.path.join(OUTPUT_DIR, "processed_image.png")
        with open(processed_image_path, "wb") as f:
            f.write(processed_image_data)

        # Encode the processed image to Base64 for display
        encoded_image_data = base64.b64encode(processed_image_data).decode('utf-8')

        # Return the Base64-encoded image and download link in the JSON response
        return jsonify({
            "processed_image_base64": encoded_image_data,
            "download_link": f"/download/processed_image.png"
        })

    except Exception as e:
        logging.error(f"Error in /remove-background: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    """Endpoint to download the processed image"""
    try:
        return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.before_request
def log_request_info():
    logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
