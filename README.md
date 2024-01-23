# Face Recognition Attendance System

## Project Overview
This project involves the development of a Face Recognition Attendance System. The system is implemented in Python and utilizes Firebase for database management. The code is organized into several components:

### Folder Structure
- **main.py:** This file contains the code responsible for capturing faces through the camera.

- **EncodeGen.py:** This script generates an `EncodeGen.py` file which stores the facial encodings of students available in the database.

- **AddDatabase.py:** This script facilitates the connection with the database and uploads essential information about students.

- **.gitignore:** A Gitignore file to specify intentionally untracked files that Git should ignore.

### Tech Stack
- **Python:** The primary programming language used for implementing the Face Recognition Attendance System.

- **Firebase:** The chosen database management system for storing relevant information about students.

### Libraries Used
- **Cmake:** A cross-platform family of tools designed to build, test, and package software.

- **dlib:** A toolkit for machine learning and computer vision tasks.

- **Face Recognition:** A face recognition library that simplifies face recognition implementation.

- **OpenCV:** An open-source computer vision and machine learning software library.

## How to Use
1. Run `main.py` to capture faces through the camera.
2. Execute `EncodeGen.py` to generate facial encodings and store them in `EncodeGen.py`.
3. Ensure you use your Firebase credentials by adding them to the appropriate configuration file.
4. Utilize `AddDatabase.py` to connect with the database and upload essential student information.

## Firebase Credentials
To use Firebase with this system, make sure to replace the placeholder credentials in the configuration files with your own Firebase credentials. You can obtain these credentials by creating a Firebase project on the [Firebase Console](https://console.firebase.google.com/) and following the instructions to set up your project.

