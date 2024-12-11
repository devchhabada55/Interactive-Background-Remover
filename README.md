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

