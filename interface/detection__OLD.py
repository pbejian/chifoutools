#import matplotlib.pyplot as plt
import streamlit as st
import mediapipe as mp
import pandas as pd
#from PIL import Image
import numpy as np
#import random
#import os
import cv2
#from PIL import Image
from chifoutools.interface.utils import create_key
from chifoutools.ml_logic.registry import load_pipeline
from chifoutools.ml_logic.preprocessor import preprocess_features


def take_a_picture(key):
    """
    Take a picture with streamlit.camera_input.
    """
    picture = st.camera_input(label="", disabled=False, key=key)
    return picture


def picture_to_df(picture):
    """
    This function take a picture of an hand as argument (created with
    streamlit.camera_input) and return a DataFrame which contains
    the mediapipe data of this hand.
    """
    hand_list = []
    mp_hands = mp.solutions.hands
    with mp_hands.Hands(static_image_mode=True,
                        max_num_hands=1,
                        min_detection_confidence=0.5) as hands:
        image = np.array(picture)
        print("✅ Image accquise")
        image_flip = cv2.flip(image, 1) ### BUUGGGG
        print("✅ CV2 OK")
        result_flip = hands.process(cv2.cvtColor(image_flip, cv2.COLOR_BGR2RGB))
        if not result_flip.multi_hand_landmarks:
            return "Pas de main sur cette photo !"

        for hand_landmarks in result_flip.multi_hand_landmarks:
            fingers = {}
            for i, finger in enumerate(hand_landmarks.landmark, start=1):
                fingers[f'{i}x'] = (finger.x)
                fingers[f'{i}y'] = (finger.y)
                fingers[f'{i}z'] = (finger.z)
            hand_list.append(fingers)
        paper_df = pd.DataFrame(hand_list)
        return paper_df


def picture_to_target(picture):
    """
    Docstring
    """
    df = picture_to_df(picture)
    # Load Pipeline from pickle file
    my_pipeline = load_pipeline()
    result = my_pipeline.predict(df)
    return result
