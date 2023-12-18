import cv2
import numpy as np
import tensorflow as tf


# Function to load the Keras model
def load_keras_model(model_path):
    return tf.keras.models.load_model(model_path)


# Function to preprocess the face image before passing it to the model
def preprocess_face_image(face_image):
    gray_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    preprocessed_image = gray_face / 255.0  # Example normalization
    return np.expand_dims(np.expand_dims(preprocessed_image, axis=-1), axis=0)


# Function to detect faces in a frame
def detect_face(frame, cv_classifier_path):
    face_cascade = cv2.CascadeClassifier(cv_classifier_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    return faces


# Function to print frames with face information
def process_frames(video_path, model_path, cv_classifier_path):
    # Load the Keras model
    model = load_keras_model(model_path)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Couldn't open the video file.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    first_frame = 0
    mid_frame = total_frames // 2

    def display_frame_with_face(frame_index, frame_label):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if ret:
            faces = detect_face(frame, cv_classifier_path)
            if len(faces) > 0:
                for x, y, w, h in faces:
                    # Crop and resize the face region to 48x48
                    face_roi = frame[y : y + h, x : x + w]
                    face_resized = cv2.resize(face_roi, (48, 48))

                    print(
                        f"Frame {frame_index}, Time: {frame_index / fps:.2f} seconds (Contains a face)"
                    )

                    # Preprocess the face image and make predictions
                    preprocessed_face = preprocess_face_image(face_resized)
                    prediction = model.predict(preprocessed_face)
                    confidence = (
                        prediction[0, 0] * 100
                    )  # Assuming binary classification
                    print("Model Prediction:", prediction)
                    print("Confidence:", confidence)

                    if confidence > 50:
                        print("Confident")
                        return 1
                    else:
                        print("Unconfident")
                        return 0

            else:
                print("Face not found")
                return -1

    result_first_frame = display_frame_with_face(first_frame, "First Frame")
    result_mid_frame = display_frame_with_face(mid_frame, "Second Frame (Mid)")

    cap.release()
    cv2.destroyAllWindows()

    return result_first_frame, result_mid_frame


if __name__ == "__main__":
    # Example usage:
    video_path = "video_1.mp4"
    model_path = "conf_unconf.h5"
    result_first, result_mid = process_frames(video_path, model_path)
    print("Result First Frame:", result_first)
    print("Result Mid Frame:", result_mid)
