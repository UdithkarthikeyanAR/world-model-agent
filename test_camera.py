import cv2

from vision.video_loader import VideoLoader


camera = VideoLoader()

while True:

    success, frame = camera.read()

    if not success:
        break

    cv2.imshow("World Model Camera", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()