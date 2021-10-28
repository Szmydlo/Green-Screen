from typing import Callable
import numpy as np
import cv2
import sys


COLOR_BOUNDARIES = {
    'LOWER_GREEN_HSV': np.array([36, 0, 0]),
    'UPPER_GREEN_HSV': np.array([86, 255, 255]),
    'LOWER_GREEN_BGR': np.array([0, 135, 0]),
    'UPPER_GREEN_BGR': np.array([110, 255, 110])
}


def check_dimensions_compability(video_object: cv2.VideoCapture, image_array: np.ndarray) -> None:
    '''Function to check if sizes of both inputs match

    Args:
        video_object (cv2.VideoCapture): video stream of cv2 library
        image_array (np.ndarray): image stream as numpy array

    Raises:
        Exception: If dimensions mismatch, then exception raises
    '''
    video_width = video_object.get(cv2.CAP_PROP_FRAME_WIDTH)
    video_height = video_object.get(cv2.CAP_PROP_FRAME_HEIGHT)
    image_width = image_array.shape[1]
    image_height = image_array.shape[0]

    if video_width != image_width or video_height != image_height:
        raise Exception("File dimensions mismatch")


def replace_background_cv2(
        frame: np.ndarray, image: np.ndarray, lower_boundary: np.ndarray, upper_boundary: np.ndarray) -> np.ndarray:
    '''Cv2-based implementation of background replacement

    Args:
        frame (np.ndarray): Single frame to adjust
        image (np.ndarray): New background
        lower_boundary (np.ndarray): Lower boundary of HSL colour to remove
        upper_boundary (np.ndarray): Upper boundary of HSL colour to remove

    Returns:
        np.ndarray: Adjusted frame
    '''
    # Represent frame as hsv array
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get mask of points between given range
    mask = cv2.inRange(hsv_frame, lower_boundary, upper_boundary)

    # Apply background on mask pixels
    image_background = cv2.bitwise_and(image, image, mask=mask)

    # Convert mask to hsv representation
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Remove and add new background
    result = cv2.subtract(frame, mask)
    result = cv2.add(result, image_background)

    return result


def replace_background_self(
        frame: np.ndarray, image: np.ndarray, lower_boundary: np.ndarray, upper_boundary: np.ndarray) -> np.ndarray:
    '''Self-implemented background replacement

    Args:
        frame (np.ndarray): Single frame to adjust
        image (np.ndarray): New background
        lower_boundary (np.ndarray): Lower boundary of BGR colour to remove
        upper_boundary (np.ndarray): Upper boundary of BGR colour to remove

    Returns:
        np.ndarray: Adjusted frame
    '''
    # Vectorization > iteration
    mask = (frame[:, :, 0] <= upper_boundary[0]) & (
        frame[:, :, 1] >= lower_boundary[1]) & (
            frame[:, :, 2] <= upper_boundary[2])

    # Replace only masked pixels
    frame[mask] = image[mask]

    return frame


def replace_background_with_image(video: str, image: str, removal_function: Callable,
                                  lower_boundary: np.ndarray = COLOR_BOUNDARIES['LOWER_GREEN_HSV'],
                                  upper_boundary: np.ndarray = COLOR_BOUNDARIES['UPPER_GREEN_HSV']) -> None:
    '''Function which replaces green background with given image. Uncomment lines for visual output

    Args:
        video (str): File name of video with green background
        image (str): File name of new background
        removal_function (Callable): Chosen function for replacing the background
        lower_boundary (np.ndarray, optional): Lower boundary of chosen colour model to remove. \
            Defaults to COLOR_BOUNDARIES['LOWER_GREEN_HSV'].
        upper_boundary (np.ndarray, optional): Upper boundary of chosen colour model to remove. \
            Defaults to COLOR_BOUNDARIES['UPPER_GREEN_HSV'].
    '''
    video_stream = cv2.VideoCapture(video)
    image_stream = cv2.imread(image)  # numpy array

    check_dimensions_compability(video_stream, image_stream)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    output = cv2.VideoWriter('output.mp4', fourcc, 30.0, (image_stream.shape[1], image_stream.shape[0]))

    while(video_stream.isOpened()):
        stream_read, frame = video_stream.read()
        if stream_read is True:
            adjusted_frame = removal_function(frame, image_stream, lower_boundary, upper_boundary)
            output.write(adjusted_frame)
            # Uncomment for visible output (press q to quit)
            # cv2.imshow('frame', adjusted_frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        else:
            break
    video_stream.release()
    output.release()
    cv2.destroyAllWindows()
    return True


def main():  # pragma: no cover
    '''Main function to run the script
    '''
    video_name = sys.argv[1]
    image_name = sys.argv[2]

    # CV2
    replace_background_with_image(video_name, image_name, replace_background_cv2)

    # Self
    # replace_background_with_image(video_name, image_name, replace_background_self,
    #                               COLOR_BOUNDARIES['LOWER_GREEN_BGR'], COLOR_BOUNDARIES['UPPER_GREEN_BGR'])


if __name__ == '__main__':  # pragma: no cover
    main()
