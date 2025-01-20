import cv2
import face_recognition
import os
import datetime

def choose_folder():
    path = input("Enter the folder if in another directory (es ../ or /another/) or press Enter to skip: ")
    if path == '':
        path = './'
    elif not os.path.isdir(path):
        print("The specified path is not valid or reachable.")
        exit()
    return path

def choose_video( path ):
    files = os.listdir( path )
    videos = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    if len(videos) == 0:
        print("No video files found in the specified folder.")
        exit()
    elif (len(videos) == 1):
        input("Only one video available here, Enter to proceed: " + videos[0])
        video = videos[0]
    else:
        print("The following video files were found in the specified folder:")
        print("\n".join(videos))
        video = input("Enter the choosen video name: ")
        while video not in videos:
            video = ("The specified video file does not exist, insert video name again:")
    print(f"Selected video: {video}")
    return video

def format_video_path_for_cv2( path, video ):
    if path in [ './', '.' ]: #fix needed for locals
        video_path = video
    else:
        video_path = os.path.join(path, video)
        if video_path[0] != '/':
            video_path = '/' + video_path #test
    print(f"Video path: {video_path}")
    return video_path

def create_output_folder( path, video ):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = 'faces_' + video + current_time
    output_folder = os.path.join(path, folder_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Output folder created: '{output_folder}'")
    return output_folder

def saving_faces(video_path, output_folder):
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
            print("New Face Saved")

        frame_number += 1

    # Release the video capture object
    video_capture.release()
    cv2.destroyAllWindows()

    print(f"Faces extracted and saved in '{output_folder}'")

def run():
    path = choose_folder()
    video = choose_video( path )
    output_folder = create_output_folder( path, video )
    video_path = format_video_path_for_cv2( path, video )
    print("Running...")
    #video_path = 'file_name_in_folder.mp4'
    #video_path = 'Captured David hb 3.mp4'
    saving_faces(video_path, output_folder)

run()