import unittest
import green_screen
import time


class TestGreenScreen(unittest.TestCase):
    def test_green_screen_cv2(self):
        result = True
        t0 = time.perf_counter()
        for _ in range(5):
            video_result = green_screen.replace_background_with_image(
                'Squirrels.mp4', 'Waterfall.jpg', green_screen.replace_background_cv2)
            result = result and video_result
        t1 = time.perf_counter()
        time_elapsed = t1 - t0
        average_time = time_elapsed / 5
        print(
            f'Time elapsed: {round(time_elapsed, 4)}s, \
            average time: {round(average_time, 4)}s')
        self.assertTrue(result)

    def test_green_screen_self(self):
        result = True
        t0 = time.perf_counter()
        for _ in range(5):
            video_result = green_screen.replace_background_with_image(
                'Squirrels.mp4', 'Waterfall.jpg', green_screen.replace_background_self,
                green_screen.COLOR_BOUNDARIES['LOWER_GREEN_BGR'],
                green_screen.COLOR_BOUNDARIES['UPPER_GREEN_BGR'])
            result = result and video_result
        t1 = time.perf_counter()
        time_elapsed = t1 - t0
        average_time = time_elapsed / 5
        print(
            f'Time elapsed: {round(time_elapsed, 4)}s, \
            average time: {round(average_time, 4)}s')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
