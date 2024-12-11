import os
import io
import logging
import requests
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
from google.cloud import vision, storage

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
GOOGLE_CREDENTIALS = "onlinesalesdev-2a3972a88a4b.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS

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

def check_object_presence(image_data):
    """Use Google Vision API to check if any objects are present in the image."""
    try:
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_data)

        response = client.object_localization(image=image)
        if response.error.message:
            raise ImageProcessingError(f"Vision API error: {response.error.message}")

        objects = response.localized_object_annotations
        if objects:
            detected_objects = [
                {
                    "name": obj.name,
                    "score": obj.score,
                    "bounding_poly": {
                        "normalized_vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in obj.bounding_poly.normalized_vertices
                        ]
                    }
                }
                for obj in objects
            ]
            logging.info(f"Detected objects: {[obj['name'] for obj in detected_objects]}")
            return detected_objects
        else:
            logging.info("No objects detected.")
            return []

    except Exception as e:
        raise ImageProcessingError(f"Error checking object presence: {str(e)}")

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
            return image_data

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

def download_json_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """Download a JSON file from Google Cloud Storage"""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        logging.info(f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}.")
    except Exception as e:
        raise ValueError(f"Failed to download JSON file from GCS: {e}")

@app.route("/")
def home():
    return render_template("homepage.html")  # Ensure this matches your HTML template

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

        # Check for object presence using Google Vision API
        image_bytes = image_data.getvalue()
        detected_objects = check_object_presence(image_bytes)

        # Crop the image if bounding box is provided
        cropped_image_data = crop_image(io.BytesIO(image_bytes), bounding_box)

        # Remove the background
        processed_image_data = remove(cropped_image_data.getvalue())

        # Save the processed image
        output_filename = "processed_image.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, "wb") as f:
            f.write(processed_image_data)

        return jsonify({
            "processed_image_url": f"/download/{output_filename}",
            "detected_objects": detected_objects
        })

    except Exception as e:
        logging.error(f"Error in /remove-background: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    """Download the processed image"""
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        return send_file(file_path, mimetype="image/png")
    except Exception as e:
        logging.error(f"Error in /download/{filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.before_request
def log_request_info():
    logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
