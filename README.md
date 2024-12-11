# Interactive Image Background Removal
Hi, 
This project provides an interactive web-based tool that allows users to remove the background of an image using a bounding box selection. The web application consists of a frontend interface to upload an image and draw a bounding box, and a backend that processes the image, removes the background, and returns the processed image for download.
Additionally, the project integrates Google Vision for object detection within the bounding box. This functionality can help improve the accuracy of background removal by identifying objects, although it has not yet been deployed. Will be deployed soon in next Update! 😊

Website : [Link](https://flask-app-400049391293.asia-south1.run.app)

## Features
   - Image URL Upload: Input an image URL to load the image.
   - Bounding Box Selection: Draw a bounding box over the area of the image to retain.
   - Background Removal: Process the image and remove the background using AI-based algorithms.
   - Object Detection with Google Vision: Detect objects in the selected bounding box.(will Update soon on website).
   - Download Processed Image: Get the processed image with a transparent background and download it.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup](#setup)
4. [How It Works](#how-it-works)
5. [Endpoints](#endpoints)
6. [License](#license)

## Setup

### Frontend

1. Clone or download the project files.
2. Open the `Homepage.html` file in a browser to run the frontend application.

### Backend

1. Install the required dependencies:

   ```bash
   pip install Flask rembg Pillow requests flask-cors google-cloud-vision

   Save the Python backend code in a file, such as app.py.

2. Save the Python backend code in a file, such as app.py.
3. Run the Flask app:
        python app.py
4. The app will be available at http://localhost:8080.
5. 
### 5. **Examples of Usage**
Demonstrating how your project works through examples helps users quickly grasp how to use it. You can add sample requests, command-line examples, or images to demonstrate the process.

For instance, you could include:

```markdown
### Example Request

Here’s an example of how to make a request to the `/remove-background` endpoint:

```json
{
  "image_url": "https://example.com/image.jpg",
  "bounding_box": {
    "x_min": 50,
    "y_min": 100,
    "x_max": 300,
    "y_max": 400
  }
}

### 6. **Explain How the Application Works**
This section explains the steps and flow of the application, from input to output. A breakdown helps users understand how the backend processes requests, or how the frontend interacts with the server.

```markdown
## How It Works

1. **Load Image**: Enter a public image URL to load the image onto the canvas.
2. **Draw Bounding Box**: Click and drag to select the area of the image to retain.
3. **Remove Background**: Click the submit button to remove the background.
4. **Download Processed Image**: The processed image is returned with a transparent background, and a download link is provided.

### Object Detection (Coming Soon)

- Object detection via Google Vision is integrated in the backend but not yet deployed.




