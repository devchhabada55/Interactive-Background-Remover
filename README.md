
# Interactive Image Background Removal

Hi,  
This project provides an interactive web-based tool that allows users to remove the background of an image using a bounding box selection. The web application consists of a frontend interface to upload an image and draw a bounding box, and a backend that processes the image, removes the background, and returns the processed image for download.  
Additionally, the project integrates Google Vision for object detection within the bounding box. This functionality can help improve the accuracy of background removal by identifying objects, although it has not yet been deployed. It will be deployed soon in the next update! 😊

Website: [Interactive Image Background Removal](https://flask-app-400049391293.asia-south1.run.app)

## Features

- **Image URL Upload**: Input an image URL to load the image.
- **Bounding Box Selection**: Draw a bounding box over the area of the image to retain.
- **Manual Co-ordinates**: Also you can enter the manual co-ordinates i.e X_min,X_max,Y_min,Y_max. 
- **Background Removal**: Process the image and remove the background using AI-based algorithms.
- **Object Detection with Google Vision**: Detect objects in the selected bounding box (will update soon on the website).
- **Download Processed Image**: Get the processed image with a transparent background and download it.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup](#setup)
4. [How It Works](#how-it-works)
5. [Endpoints](#endpoints)
6. [License](#license)

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Background Removal**: [rembg](https://github.com/danielgatis/rembg)
- **Google Vision API**: For object detection within the bounding box.
- **AI Algorithms**: Used for removing image backgrounds.
- **Image Processing**: Pillow for image manipulation.

## Setup

### Frontend

1. Clone or download the project files from the repository.
2. Open the `Homepage.html` file in a browser to run the frontend application.

### Backend

1. Install the required dependencies:
   
   ```bash
   pip install Flask rembg Pillow requests flask-cors google-cloud-vision
   ```

2. Save the Python backend code in a file, such as `app.py`.
3. Run the Flask app:

   ```bash
   python app.py
   ```

4. The app will be available at [http://localhost:8080](http://localhost:8080).

## How It Works

1. **Load Image**: Input a public image URL into the frontend form to load the image.
2. **Draw Bounding Box**: Use the frontend canvas to draw a bounding box around the area of the image that should remain.
3. **Background Removal**: Once the bounding box is drawn, the backend processes the image, removes the background using the rembg AI model, and generates a transparent background.
4. **Object Detection**: The system will use Google Vision API to detect objects within the bounding box, enhancing background removal accuracy.
5. **Download Processed Image**: The processed image with the removed background is returned, and the user can download the result.

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
```

### Example Response:

The response would return a JSON with the base64-encoded image or a URL to download the processed image. For example:

```json
{
  "original_image_url": "<original_image_url>",
  "processed_image_url": "http://example.com/processed_image.png"
}
```

## Endpoints

### `/remove-background`
- **Method**: `POST`
- **Description**: Accepts an image URL and optional bounding box coordinates to remove the background from the specified area of the image.
- **Request Body**: JSON containing the image URL and bounding box coordinates.
- **Response**: The processed image with the background removed.

#### Example:

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
```

### `/download/<filename>`
- **Method**: `GET`
- **Description**: Allows the user to download the processed image after background removal.

### `/object-detection`
- **Method**: `GET`
- **Description**: This endpoint will return detected objects within the bounding box selected by the user, using the Google Vision API.

## Screenshot of the Application

Here’s a screenshot showing the interactive background removal in action. This demonstrates how users can upload an image, draw a bounding box, and remove the background.

![Screenshot](./Screenshot%20(1).png) 

### Theoretical Overview
The image background removal tool uses an AI-powered algorithm to detect the foreground object and remove the background seamlessly. The bounding box allows users to define the area for processing, ensuring more accurate results.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Major Contributor : Dev Chhabada


Feel free to fork this project and submit pull requests! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new pull request.

