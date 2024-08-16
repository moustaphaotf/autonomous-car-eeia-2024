
# import the opencv library
import cv2
  
  
# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    
    grayscale_image  = cv2.cvtColor(frame , cv2.COLOR_RGB2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image,(5,5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)
    # Display the resulting frame
    cv2.imshow('frame', edges)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()