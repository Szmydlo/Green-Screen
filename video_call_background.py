from typing import Tuple
import time
import cv2
import numpy as np


COLOR_BOUNDARIES = {
    # CV2 HSV hue 0-179
    'LOWER_HSV': np.array([0, 0, 0]),
    'UPPER_HSV': np.array([179, 150, 150])
}

ADJUSTMENT_FREQUENCY = 30
BLUR_STRENGTH = 35
DELTA = 6


def show_frame(frame: np.ndarray, last_time: float) -> None:
    '''Function to show last generated frame with FPS

    Args:
        frame (np.ndarray): Frame to show
        last_time (float): Last measured time for FPS calculations
    '''
    text = f"FPS: {int(1 / (time.time() - last_time))}"
    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow('Webcam', frame)


def blur_cv2(frame: np.ndarray) -> np.ndarray:
    '''CV2-based function from blurring background (color-dependent)

    Args:
        frame (np.ndarray): Single frame to be blurred

    Returns:
        np.ndarray: Adjusted frame
    '''
    # Convertion to the HSV color model for easier masking
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask for low saturation ~ skin colour
    mask = cv2.inRange(hsv_frame,  COLOR_BOUNDARIES['LOWER_HSV'], COLOR_BOUNDARIES['UPPER_HSV'])

    # To prevent shape mismatch, mask needs to be stacked
    mask_3d = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    blurred_frame = cv2.GaussianBlur(frame, (BLUR_STRENGTH, BLUR_STRENGTH), 0)
    adjusted_frame = np.where(mask_3d == (255, 255, 255), frame, blurred_frame)

    return adjusted_frame


def set_defaults_sizes(webcam: cv2.VideoCapture) -> Tuple[np.ndarray, np.ndarray]:
    '''Function for setting right size of frame and mask

    Args:
        webcam (cv2.VideoCapture): Webcam object

    Returns:
        [np.ndarray, np.ndarray]: New array for old_frame and one_second_mask
    '''
    width = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return [np.zeros(shape=(height, width, 3)), np.zeros(shape=(height, width, 3))]


def calculate_mask(old_frame: np.ndarray, new_frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    '''Calculates new mask and sets new old_frame if needed

    Args:
        old_frame (np.ndarray): 1 second old frame
        new_frame (np.ndarray): Current frame

    Returns:
        Tuple[np.ndarray, np.ndarray]: New mask and new old_frame
    '''
    # DELTA is margin of change for a value. Even with "stable" image there are some "fluctuations"
    one_second_mask = np.isclose(old_frame, new_frame, atol=DELTA)
    old_frame = np.copy(new_frame)
    return [one_second_mask, old_frame]


def replace_background_with_blur_self() -> None:
    '''Function which blurs background of webcam video
    '''
    # Get the webcam (index: 0)
    webcam = cv2.VideoCapture(0)

    # Timer for FPS
    last_time = time.time()

    # Set default values
    frame_count = 0
    old_frame, one_second_mask = set_defaults_sizes(webcam)

    while True:
        stream_read, frame = webcam.read()

        if stream_read is True:
            # Every ADJUSTMENT_FREQUENCY frames perform blur adjustment
            if frame_count % ADJUSTMENT_FREQUENCY == 0:
                one_second_mask, old_frame = calculate_mask(old_frame, frame)
                frame_count = frame_count - 30

            # for equivalent blurring results between approaches
            blurred_frame = cv2.GaussianBlur(frame, (BLUR_STRENGTH, BLUR_STRENGTH), 0)

            # Mask final values
            adjusted_frame = np.where(one_second_mask, blurred_frame, frame)

            show_frame(adjusted_frame, last_time)
            # Press q to quit
            if cv2.waitKey(1) == ord('q'):
                break

            # Update counter and timer
            frame_count = frame_count + 1
            last_time = time.time()

    # Clean up
    webcam.release()
    cv2.destroyAllWindows()


def replace_background_with_blur_cv2() -> None:
    '''Function which blurs background of webcam video
    '''
    # Get the webcam (index: 0)
    webcam = cv2.VideoCapture(0)

    # Timer for FPS
    last_time = time.time()

    while True:
        stream_read, frame = webcam.read()

        if stream_read is True:
            adjusted_frame = blur_cv2(frame)

            show_frame(adjusted_frame, last_time)
            # Press q to quit
            if cv2.waitKey(1) == ord('q'):
                break

            # Update timer
            last_time = time.time()

    # Clean up
    webcam.release()
    cv2.destroyAllWindows()


def main():  # pragma: no cover
    '''Main function to run the script
    '''
    replace_background_with_blur_self()


if __name__ == '__main__':  # pragma: no cover
    main()
