import unittest
import green_screen
import time
import cv2
import numpy as np

RUNS = 1


class TestGreenScreen(unittest.TestCase):
    def test_green_screen_cv2(self):
        result = True
        t0 = time.perf_counter()
        for _ in range(RUNS):
            video_result = green_screen.replace_background_with_image(
                'Squirrels.mp4', 'Waterfall.jpg', green_screen.replace_background_cv2)
            result = result and video_result
        t1 = time.perf_counter()
        time_elapsed = t1 - t0
        average_time = time_elapsed / RUNS
        print(
            f'Time elapsed: {round(time_elapsed, 4)}s, \
            average time: {round(average_time, 4)}s')

        self.assertTrue(result)

    def test_green_screen_self(self):
        result = True
        t0 = time.perf_counter()
        for _ in range(RUNS):
            video_result = green_screen.replace_background_with_image(
                'Squirrels.mp4', 'Waterfall.jpg', green_screen.replace_background_self,
                green_screen.COLOR_BOUNDARIES['LOWER_GREEN_BGR'],
                green_screen.COLOR_BOUNDARIES['UPPER_GREEN_BGR'])
            result = result and video_result
        t1 = time.perf_counter()
        time_elapsed = t1 - t0
        average_time = time_elapsed / RUNS
        print(
            f'Time elapsed: {round(time_elapsed, 4)}s, \
            average time: {round(average_time, 4)}s')

        self.assertTrue(result)

    def test_check_dimensions_compability_should_not_raise(self):
        video_stream = cv2.VideoCapture('Squirrels.mp4')
        image_stream = cv2.imread('Waterfall.jpg')

        try:
            green_screen.check_dimensions_compability(video_stream, image_stream)
        except Exception:
            self.fail("check_dimensions_compability() raised unexpected Exception")

    def test_check_dimensions_compability_should_raise(self):
        video_stream = cv2.VideoCapture('Squirrels.mp4')
        image_stream = cv2.imread('Test-images/Sunflower.jpg')
        self.assertRaises(Exception, green_screen.check_dimensions_compability, video_stream, image_stream)

    def test_replace_cv2(self):
        green = cv2.imread('Test-images/Green.png')
        red = cv2.imread('Test-images/Red.png')
        output = green_screen.replace_background_cv2(green, red, np.array([36, 0, 0]), np.array([86, 255, 255]))

        self.assertTrue((output == red).all())

    def test_no_replace_cv2(self):
        blue = cv2.imread('Test-images/Blue.png')
        red = cv2.imread('Test-images/Red.png')
        output = green_screen.replace_background_cv2(blue, red, np.array([25, 0, 0]), np.array([75, 255, 255]))

        self.assertTrue((output == blue).all())

    def test_replace_self(self):
        green = cv2.imread('Test-images/Green.png')
        red = cv2.imread('Test-images/Red.png')
        output = green_screen.replace_background_self(red, green, np.array([128, 0, 0]), np.array([240, 240, 240]))

        self.assertTrue((output == green).all())

    def test_no_replace_self(self):
        blue = cv2.imread('Test-images/Blue.png')
        red = cv2.imread('Test-images/Red.png')
        output = green_screen.replace_background_self(red, blue, np.array([128, 0, 0]), np.array([240, 240, 240]))

        self.assertTrue((output == blue).all())


if __name__ == '__main__':
    unittest.main()
