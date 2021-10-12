# Green Screen Replacement Script
The idea behind this project is to develop a script, which will replace uniform green background of a video with an image and blur background as in video calls and compare it to predefined functions of [OpenCV](https://opencv.org/) package

TODO:  
- :white_check_mark: Replace green background with image
  - :white_check_mark: Find a film sample of a green/blue screen video  
  - :white_check_mark: Import the frames of the video  
  - :white_check_mark: Find the pixels that are approximately green/blue  
  - :white_check_mark: Set the opacity of those pixel to zero  
  - :white_check_mark: Add a different background  
- :white_large_square: Blur constant-over-time background (like video calls)
  - :white_large_square: Real time computation

<br />
<br />

## Green Background
Located in [green_screen.py](https://github.com/Szmydlo/Green-Screen/blob/main/green_screen.py). To run pass two parameters:
- Video with green background
- Image to replace green pixels

They both should have the same dimensions, otherwise error will be thrown. Edited video is stored in  `output.mp4` file. To see how algorithm performs frame by frame uncomment block in `replace_background_with_image` function.
<br />
<br />
### Testing
CV2-based function first represents colours in HSV model. Then it computes mask for both video frame and image. Unwanted green background is substracted and replaced with masked image. For 5 runs it takes:  

![Timings of CV2 method](/Screenshots/GreenScreenReplacementCV2.png?raw=true "Timings of CV2 method")
<br />
<br />
Self implementation tries to compete with predefined functions. It makes cuts using numpy advanced indexing: green pixels are replaced right away with image pixels. Also colour model is not changed (BGR - Blue, Green, Red). For 5 runs it takes:  

![Timings of self-implemented method](/Screenshots/GreenScreenReplacementSelf.png?raw=true "Timings of self-implemented method")  

<br />
For a 30 fps video it takes around the length of video to replace background with self-implemented method. On the other hand CV2 method needs 1/3 of duration of the video to replace green pixels.

Even with optimized, vectorized code (iterated approach is around 100 times slower) CV2 predefined methods are much faster in replacing green screen.

Quality-wise it is also harder to define "green" in BGR colour model. Therefore self-implemented method performs slightly worse in terms of quality too:

![Quality comparison of green screen removal](/Screenshots/Squirrels.png?raw=true "Quality comparison of green screen removal")  