import cv2
import os
import csv
from datetime import datetime

# Directory to save captured images
save_dir = 'captured_images'
os.makedirs(save_dir, exist_ok=True)

# CSV file to save image paths and class labels
csv_file = os.path.join(save_dir, 'image_data.csv')

# Define a video capture object
vid = cv2.VideoCapture(0)

# Function to save image and log data
def save_image_and_log(frame, img_class, img_count):
    # Generate image filename with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    img_name = f'image_{img_count}_{timestamp}.jpg'
    img_path = os.path.join(save_dir, img_name)
    
    # Save the image
    cv2.imwrite(img_path, frame)
    
    # Log image path and class to CSV
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([img_path, img_class])

# Initialize image counter
img_count = 0

while(True):
    # Capture the video frame by frame
    ret, frame = vid.read()
    
    # Process the frame: Convert to grayscale, blur, and detect edges
    grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)
    
    # Display the resulting frame
    cv2.imshow('frame', edges)
      
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        # Quit the loop if 'q' is pressed
        break
    elif key == 13:  # Enter key (ASCII code 13)
        # Capture image when Enter key is pressed
        img_count += 1
        img_class = '0'  # Replace with actual class label if needed
        save_image_and_log(frame, img_class, img_count)
        print(f"Captured image {img_count}")

# Release the capture object and close all windows
vid.release()
cv2.destroyAllWindows()
