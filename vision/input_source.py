import cv2


class InputSource:

    def __init__(self):

        print("\nChoose Input Source")
        print("1. Webcam")
        print("2. Video File")

        choice = input("\nSelect (1/2): ").strip()

        if choice == "1":

            self.cap = cv2.VideoCapture(0)

        elif choice == "2":

            path = input("\nEnter video path: ").strip()

            self.cap = cv2.VideoCapture(path)

            if not self.cap.isOpened():

                raise FileNotFoundError(
                    f"Cannot open video: {path}"
                )

        else:

            raise ValueError("Invalid choice.")

    def read(self):

        return self.cap.read()

    def release(self):

        self.cap.release()