import cv2
import numpy as np
from tf_keras.models import load_model
from mediapipe.python.solutions.hands import Hands

hands = Hands()
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']


def analyze(img, model):
    """
    Takes a preprocessed image and a pretrained model and returns the prediction and confidence

    Parameters
    ----------
    img: np.ndarray
        The preprocessed image (returned by `analysis_frame`)
    model: tf.keras.Model
        The pretrained model
    
    Returns
    -------
    (pred, conf): tuple
        The predicted letter and the confidence value of the prediction
    
    
    """
    pred = model(img)

    guess = np.argmax(pred)
    confidence = pred[0][guess]
    
    return letters[guess], confidence



def analysis_frame(frame):
    """
    Takes a frame and returns a preprocessed image

    Parameters
    ----------
    frame: np.ndarray
        The frame to be analyzed (from `cv2.VideoCapture.read`)

    Returns
    -------
    (bool, img): tuple
        A boolean indicating if a hand was detected and the preprocessed image

    """
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        x_min = int(min([landmark.x for landmark in hand_landmarks.landmark]) * w)
        x_max = int(max([landmark.x for landmark in hand_landmarks.landmark]) * w)
        y_min = int(min([landmark.y for landmark in hand_landmarks.landmark]) * h)
        y_max = int(max([landmark.y for landmark in hand_landmarks.landmark]) * h)

        max_diff = max(x_max - x_min, y_max - y_min)

        k = 1.25

        center = ((x_min + x_max) // 2, (y_min + y_max) // 2)

        x_min = max(0, center[0] - int(max_diff/2 * k))
        x_max = min(w, center[0] + int(max_diff/2 * k))

        y_min = max(0, center[1] - int(max_diff/2 * k))
        y_max = min(h, center[1] + int(max_diff/2 * k))

        img = frame[y_min:y_max, x_min:x_max]
        img = cv2.resize(img, (28, 28))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img / 255.0
        img = img.reshape(1, 28, 28, 1)
        
        return True, img

    return False, None

