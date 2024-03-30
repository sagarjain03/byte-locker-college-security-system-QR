import cv2
import numpy as np
from pyzbar.pyzbar import decode
import datetime
import csv

# Load the list of authorized data
with open('myDataFile.text') as f:
    authorized_names = f.read().splitlines()

# CSV file name for logging
csv_file = 'entry_log.csv'

# Initialize the CSV file with headers if it doesn't exist
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Entry Time"])

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Decode QR codes from the frame
    decoded_objects = decode(frame)

    # Iterate over all detected QR codes
    for obj in decoded_objects:
        # Extract data from the QR code
        name = obj.data.decode('utf-8')

        # Get the current time
        entry_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if the decoded data is in the list of authorized data
        if name in authorized_names:
            # Write the entry data to the CSV file
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, entry_time])

            # Display authorization status on the frame
            cv2.putText(frame, f"{name} - Authorized", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # Display authorization status on the frame
            cv2.putText(frame, "Unauthorized", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('QR Code Scanner', frame)

    # Check for key press
    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' key to exit
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
