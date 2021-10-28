import unittest
import video_call_background
import cv2
import numpy as np
import pyautogui
from threading import Timer


class TestVideoCallBackground(unittest.TestCase):
    def test_webcam_sizes(self):
        webcam = cv2.VideoCapture(0)
        answer = (480, 640, 3)
        arr1, arr2 = video_call_background.set_defaults_sizes(webcam)

        self.assertTrue((arr1.shape == answer))
        self.assertTrue((arr2.shape == answer))
        webcam.release()

    def test_blur_cv2(self):
        face = cv2.imread('Test-images/Face.png')
        output = video_call_background.blur_cv2(face)

        self.assertTrue(np.any(np.not_equal(face, output)))

    def test_no_blur_cv2(self):
        red = cv2.imread('Test-images/Red.png')
        output = video_call_background.blur_cv2(red)

        self.assertTrue((red == output).all())

    def test_mask(self):
        red = cv2.imread('Test-images/Red.png')
        mask, _ = video_call_background.calculate_mask(red, red)

        self.assertTrue(mask.all())

    def test_no_mask(self):
        red = cv2.imread('Test-images/Red.png')
        blue = cv2.imread('Test-images/Blue.png')
        mask, _ = video_call_background.calculate_mask(red, blue)

        self.assertTrue((~mask).all())

    def test_replace_self(self):
        r = Timer(5.0, pyautogui.press, ('q'))
        r.start()
        video_call_background.replace_background_with_blur_self()

        self.assertTrue(True)

    def test_replace_cv2(self):
        r = Timer(5.0, pyautogui.press, ('q'))
        r.start()
        video_call_background.replace_background_with_blur_cv2()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
