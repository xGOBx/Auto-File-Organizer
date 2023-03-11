import os 
import shutil
from win10toast import ToastNotifier
from time import sleep
import subprocess
import ctypes
import sys
import json
import getpass




# Get the directory of this script
script_dir = os.path.dirname(os.path.realpath(__file__))


def create_Resources():


        
    username = getpass.getuser()


    # Get the path to the resources folder
    resources_dir = os.path.join(script_dir, "resources")

    # Check if files already exist in the resources folder
    file_organiser_bat_path = os.path.join(resources_dir, "fileOrganizer.bat")
    set_reg_bat_path = os.path.join(resources_dir, "setReg.bat")
    file_organiser_vbs_path = os.path.join(resources_dir, "fileOrganizer.vbs")


    if(os.path.exists(file_organiser_bat_path) and
            os.path.exists(set_reg_bat_path) and
            os.path.exists(file_organiser_vbs_path)):
        print("Files already exist in the resources folder.")

    else:

            # JSON file doesn't exist, prompt user for input values
        with open(os.path.join(script_dir, 'helpers', 'RunAsAdmin.py')) as f:
            exec(f.read())
        partition_letter = input("Enter the partition letter (e.g., C, D, E): ")

        # Create the fileOrganizer.bat file
        file_organiser_bat = f"""
        @echo off

        python {partition_letter}:\\Users\\{username}\\Desktop\\FileService\\app.py

        @pause"""
        with open(file_organiser_bat_path, "w") as f:
            f.write(file_organiser_bat)

        # Create the setReg.bat file
        set_reg_bat = f"""
        @echo off

        set "valueName=fileOrganizer"
        set "valueData={partition_letter}:\\Users\\{username}\\Desktop\\FileService\\resources\\fileOrganizer.vbs"

        echo Adding new String Value...
        reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "%valueName%" /d "%valueData%" /f

        echo String Value "%valueName%" created with value data "%valueData%"!

        exit
        """
        with open(set_reg_bat_path, "w") as f:
            f.write(set_reg_bat)

        # Create the fileOrganizer.vbs file
        file_organiser_vbs = f"""CreateObject("Wscript.shell").Run "{partition_letter}:\\Users\\{username}\\Desktop\\FileService\\resources\\fileOrganizer.bat", 0 , True"""
        with open(file_organiser_vbs_path, "w") as f:
            f.write(file_organiser_vbs)

        print("All files created successfully in the resources folder.")



create_Resources()
    
    

# Check if JSON file exists
config_file = os.path.join(script_dir, 'config.json')
if os.path.isfile(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        landing_folder = config['landing_folder']
        main_storage_folder = config['main_storage_folder']
else:
    
    script_dir = os.path.dirname(__file__)
    bat_file_path = os.path.join(script_dir, 'resources', 'setReg.bat')
    subprocess.run([bat_file_path])
    
    landing_folder = input("Enter the path of the landing folder: ")
    main_storage_folder = input("Enter the path of the main storage folder: ")
    print("Restart PC and enjoy!")
    # Save input values to JSON file
    with open(config_file, 'w') as f:
        config = {
            'landing_folder': landing_folder,
            'main_storage_folder': main_storage_folder,
        }
        json.dump(config, f)

# Change working directory
os.chdir(script_dir)


# Create paths using the main storage folder relative to this script
images_folder = os.path.join(main_storage_folder, "images")
audio_folder = os.path.join(main_storage_folder, "audio")
videos_folder = os.path.join(main_storage_folder, "videos")
docs_folder = os.path.join(main_storage_folder, "docs")
exe_folder = os.path.join(main_storage_folder, "exe")
others_folder = os.path.join(main_storage_folder, "others")

# You can add more file formats here
image_formats = ["jpg", "png", "jpeg", "gif", "webp", "tiff"]
audio_formats = ["mp3", "wav", "wma"]
video_formats = ["mp4", "avi", "webm"]
docs_formats = ["ai", "ait", "txt", "rtf", "doc", "docx", "pdf", "txt"]
exe_formats = ["exe"]
    
def init():
    # Create the main storage folder and subfolders if they don't exist
    if not os.path.isdir(main_storage_folder):
        os.mkdir(main_storage_folder)
    if not os.path.isdir(images_folder):
        os.mkdir(images_folder)
    if not os.path.isdir(audio_folder):
        os.mkdir(audio_folder)
    if not os.path.isdir(videos_folder):
        os.mkdir(videos_folder)
    if not os.path.isdir(docs_folder):
        os.mkdir(docs_folder)
    if not os.path.isdir(exe_folder):
        os.mkdir(exe_folder)
    if not os.path.isdir(others_folder):
        os.mkdir(others_folder)

toast = ToastNotifier()

try:
    toast.show_toast("File Organiser", "The process has been started", duration=30)
except TypeError:
    pass


init()



while True:
    files = os.listdir(landing_folder)

    for file in files:
        if os.path.isfile(os.path.join(landing_folder, file)):
            ext = (file.split(".")[-1]).lower()
            if ext in image_formats:
                shutil.move(os.path.join(landing_folder, file), os.path.join(images_folder, file))
            elif ext in audio_formats:
                shutil.move(os.path.join(landing_folder, file), os.path.join(audio_folder, file))
            elif ext in video_formats:
                shutil.move(os.path.join(landing_folder, file), os.path.join(videos_folder, file))
            elif ext in docs_formats:
                shutil.move(os.path.join(landing_folder, file), os.path.join(docs_folder, file))
            elif ext in exe_formats:
                shutil.move(os.path.join(landing_folder, file), os.path.join(exe_folder, file))
            else:
                shutil.move(os.path.join(landing_folder, file), os.path.join(others_folder, file))

    del files
    sleep(2) #if program is using too much memory increase the value of sleep function# Close the command prompt window


