import cv2
import face_recognition
import os

# Load the video
video_path = 'file_name_in_folder.mp4'
output_folder = 'extracted_faces'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

video_capture = cv2.VideoCapture(video_path)
frame_number = 0

while video_capture.isOpened():
    # Read a frame from the video
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert the frame from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Iterate through each face found in the frame
    for i, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        # Extract the face from the frame
        face_image = frame[top:bottom, left:right]

        # Save the extracted face
        face_filename = os.path.join(output_folder, f'face_{frame_number}_{i}.jpg')
        cv2.imwrite(face_filename, face_image)

    frame_number += 1

# Release the video capture object
video_capture.release()
cv2.destroyAllWindows()

print(f"Faces extracted and saved in '{output_folder}'")