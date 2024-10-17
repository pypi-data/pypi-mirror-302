import os
import cv2
import json
import shutil

def print_tabular(data):
    keys_to_print = ['dataset_name', 'id']
    print('\t '.join(keys_to_print))
    # Print rows
    for item in data['dataSets']:
        print('\t '.join(str(item[key]) for key in keys_to_print if key in item))

def format_time(seconds):
    time_str = ""
    hours, remainder = divmod(seconds, 3600)
    if hours:
        time_str += f"{int(hours)}h "
    minutes, seconds = divmod(remainder, 60)
    if minutes or time_str:
        time_str += f"{int(minutes)}m "
    if not time_str:  # if time_str is empty, it means the duration is less than a minute
        time_str = f"{seconds:.2f}s"
    return time_str.strip()


def validate_coco_format(file_path):
        print('Validating coco format...')
        try:
            with open(file_path, 'r') as file:
                coco_data = json.load(file)

            # Check for the essential keys in COCO format
            essential_keys = ['images', 'annotations', 'categories']
            if not all(key in coco_data for key in essential_keys):
                print("Missing one or more essential COCO format keys.")
                return False

            # Validate the structure of 'images', 'annotations', and 'categories'
            for image in coco_data['images']:
                if not all(key in image for key in ['id', 'file_name']): #include width & height
                    print("Invalid structure in 'images'.")
                    return False

            for annotation in coco_data['annotations']:
                if not all(key in annotation for key in ['id', 'image_id', 'category_id']): #include for object detection bbox
                    print("Invalid structure in 'annotations'.")
                    return False

            for category in coco_data['categories']:
                if not all(key in category for key in ['id', 'name']):
                    print("Invalid structure in 'categories'.")
                    return False

            print("Metadata file is in valid COCO format.")
            return True

        except Exception as e:
            print(f"Error validating COCO format: {e}")
            return False

def flatten_directory(directory_path):
    """
    Copy all files from subdirectories to the main directory
    """
    try:
        # First, copy all files from subdirectories to the main directory
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Skip the main directory itself
                if root == directory_path:
                    continue
                # Copy file to the main directory
                source = os.path.join(root, file)
                destination = os.path.join(directory_path, file)
                shutil.move(source, destination)
    except Exception as e:
        print(e)


def subsample_video_to_frames(input_video, output_folder='video_output', sub_sample_rate=15, image_format='png'):

    output_folder = os.path.abspath(output_folder)

    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(input_video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_idx = 0
    saved_frame_idx = 0

    # Read through the video frame by frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame if it's at the subsample rate
        if frame_idx % sub_sample_rate == 0:
            filename = os.path.join(output_folder, f"frame_{saved_frame_idx:04d}.{image_format}")
            cv2.imwrite(filename, frame)
            saved_frame_idx += 1

        frame_idx += 1

    cap.release()
    print(f'Successfully extracted {frame_idx} frames to {output_folder}')
