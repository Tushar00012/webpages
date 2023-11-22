# app.py
from flask import Flask, render_template, redirect, request
import cv2
import face_recognition
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        # Trigger the face registration code here
        person_name = request.form['person_name']
        register_faces(person_name)
        return redirect('/result')
    return render_template('login2.html')

# @app.route('/register', methods=['GET', 'POST'])
# def page3():
#     if request.method == 'POST':
#         person_name = request.form['person_name']
#         return render_template('/final')#, person_name=person_name
#     return render_template('register.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        person_name = request.form['person_name']
        # Perform any registration logic here

        # Redirect to the final page or any other appropriate page
        return redirect('/final', person_name=person_name)  # You can adjust the URL as needed

    return render_template('register.html')

@app.route('/final')
def final():
    # You can include any logic needed for the 'final' page here
    return render_template('final.html')

@app.route('/result')
def result():
    return render_template('result.html')

def register_faces(person_name, output_dir='faces'):
    # Your face registration logic (similar to the provided code)
    # ...
    if not os.path.exists(person_name):
        os.makedirs(person_name)

    # Open a connection to the camera (0 is the default camera)
    video_capture = cv2.VideoCapture(0)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    count = 0

    print("Press 'q' to stop capturing and register the face.")

    while True:
        # Capture each frame
        ret, frame = video_capture.read()

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Draw a rectangle around the face
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Capture a frame every 100 milliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            # Save the captured face to the person's directory
            face_image = os.path.join(person_name, f"face_{count}.jpg")
            cv2.imwrite(face_image, frame)
            count += 1

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)
