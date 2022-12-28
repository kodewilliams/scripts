import os
import subprocess
import sys

def get_aspect_ratio(filename):
    # Use ffprobe to get the width and height of the video
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,sample_aspect_ratio,display_aspect_ratio', '-of', 'csv=p=0', filename]
    output = subprocess.check_output(command).decode().strip()
    width, height = map(float, output.split(',')[:2])

    # Calculate the aspect ratio
    aspect_ratio = width / height
    return aspect_ratio

def main():
    # Check if a directory was specified as a command line argument
    if len(sys.argv) < 2:
        print('Usage: python sort_videos.py <directory>')
        sys.exit(1)

    # Get the specified directory from the command line arguments
    directory = sys.argv[1]

    # Change the current working directory to the specified directory
    os.chdir(directory)

    # Create the landscape and portrait subfolders if they don't already exist
    if not os.path.exists('Landscape'):
        os.mkdir('Landscape')
    if not os.path.exists('Portrait'):
        os.mkdir('Portrait')

    # Iterate through all files in the specified directory
    for filename in os.listdir():
        try:
            # Skip hidden files
            if filename.startswith('.'):
                continue

            extension = filename.split('.')[-1].lower()
            # Skip files that don't have the desired extensions
            if extension not in ("mp4", "mov", "avi"):
                continue

            # Get the aspect ratio of the video
            aspect_ratio = get_aspect_ratio(filename)

            # Determine whether the video is landscape or portrait
            if aspect_ratio >= 1:
                subfolder = 'Landscape'
            else:
                subfolder = 'Portrait'

            # Move the file to the appropriate subfolder
            os.rename(filename, f'{subfolder}/{filename}')
        except Exception as e:
            print(f"Error occurred: {e}. Continuing.")
            continue
    
    print(f"Done. Exiting.")
    sys.exit(0)

if __name__ == '__main__':
    main()
