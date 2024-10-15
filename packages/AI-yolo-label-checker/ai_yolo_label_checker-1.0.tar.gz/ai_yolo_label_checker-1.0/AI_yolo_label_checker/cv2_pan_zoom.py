RUN=1

from matplotlib import pyplot as plt

plt.plot()

if RUN==2:
    # Import dependancies
    import cv2

    maxScaleUp = 100
    scaleFactor = 1
    windowName = "Resize Image"
    trackbarValue = "Scale"

    # read the image
    image = cv2.imread("img1.jpg")

    # Create a window to display results and  set the flag to Autosize
    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)


    # Callback functions
    def scaleImage(*args):
        # Get the scale factor from the trackbar
        scaleFactor = 1 + args[0] / 100.0
        # Resize the image
        scaledImage = cv2.resize(image, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv2.INTER_LINEAR)
        cv2.imshow(windowName, scaledImage)


    # Create trackbar and associate a callback function
    cv2.createTrackbar(trackbarValue, windowName, scaleFactor, maxScaleUp, scaleImage)

    # Display the image
    cv2.imshow(windowName, image)
    c = cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass
if RUN==1:
    # Import packages
    import cv2

    # Lists to store the bounding box coordinates
    top_left_corner = []
    bottom_right_corner = []


    # function which will be called on mouse input
    def drawRectangle(action, x, y, flags, *userdata):
        # Referencing global variables
        global top_left_corner, bottom_right_corner
        # Mark the top left corner when left mouse button is pressed
        # print(action, x, y, flags, *userdata)
        if action == cv2.EVENT_LBUTTONDOWN:
            top_left_corner = [(x, y)]
            # When left mouse button is released, mark bottom right corner
        elif action == cv2.EVENT_LBUTTONUP:
            bottom_right_corner = [(x, y)]
            # Draw the rectangle
            cv2.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0, 255, 0), 2, 8)
            cv2.imshow("Window", image)
        elif action == cv2.EVENT_MOUSEWHEEL:
            if flags>0: print('Scroll Up')
            if flags<0: print('Scroll Down')




    # Read Images
    image = cv2.imread("img1.jpg")
    # Make a temporary image, will be useful to clear the drawing
    temp = image.copy()
    # Create a named window
    cv2.namedWindow("Window")
    # highgui function called when mouse events occur
    cv2.setMouseCallback("Window", drawRectangle)

    k = 0
    # Close the window when key q is pressed
    while k != 113:
        # Display the image
        cv2.imshow("Window", image)
        k = cv2.waitKey(0)
        # If c is pressed, clear the window, using the dummy image
        if (k == 99):
            image = temp.copy()
            cv2.imshow("Window", image)

    cv2.destroyAllWindows()

