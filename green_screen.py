import numpy as np
import cv2
import sys


COLOR_BOUNDARIES = {
    'LOWER_GREEN': [36, 0, 0],
    'UPPER_GREEN': [86, 255, 255]
}


def check_dimensions_compability(video_object: cv2.VideoCapture,
                                 image_array: np.ndarray) -> None:
    '''Function to check if sizes of both inputs match'''
    video_width = video_object.get(cv2.CAP_PROP_FRAME_WIDTH)
    video_height = video_object.get(cv2.CAP_PROP_FRAME_HEIGHT)
    image_width = image_array.shape[1]
    image_height = image_array.shape[0]

    if video_width != image_width or video_height != image_height:
        raise Exception("File dimensions mismatch")


def replace_background_cv2(frame: np.ndarray, image: np.ndarray,
                           lower_boundary: np.ndarray,
                           upper_boundary: np.ndarray) -> np.ndarray:
    '''Cv2-based implementation of background replacement'''
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


def replace_background_with_image(video: str, image: str) -> None:
    '''Function which replaces green background with given image_stream'''
    video_stream = cv2.VideoCapture(video)
    image_stream = cv2.imread(image)  # numpy array

    check_dimensions_compability(video_stream, image_stream)

    # Define boundaries for colour
    lower_boundary = np.array(COLOR_BOUNDARIES['LOWER_GREEN'])
    upper_boundary = np.array(COLOR_BOUNDARIES['UPPER_GREEN'])

    while(video_stream.isOpened()):
        stream_read, frame = video_stream.read()
        if stream_read is True:
            adjusted_frame = replace_background_cv2(
                frame, image_stream, lower_boundary, upper_boundary)
            cv2.imshow('frame', adjusted_frame)

            # Press q to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    video_stream.release()
    cv2.destroyAllWindows()


def main():
    video_name = sys.argv[1]
    image_name = sys.argv[2]

    replace_background_with_image(video_name, image_name)


if __name__ == "__main__":
    main()
