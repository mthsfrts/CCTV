import cv2
import time
import datetime

# Cameras

cap = cv2.VideoCapture("Your RSTP Link HERE")

# Instances
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5


# methods

def rescale_frame(frame, percent=75):
    """Method responsible for scale the frame"""

    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def element(frame):
    """Method responsible for analyse the frame"""

    body = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    person = body.detectMultiScale(gray, 1.8, 3)

    return person


def record():
    """Method responsible for automate the recording of the footage"""

    current_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame_size = (int(cap.get(3)), int(cap.get(4)))

    film = cv2.VideoWriter(
        f"{current_time}.mp4", fourcc, 20, frame_size)
    return film


class Cctv:
    """Class responsible for generate and record the CCTV footage"""

    while True:
        _, frame = cap.read()

        # Image Analysis
        scale = rescale_frame(frame, percent=145)
        element(frame)

        # Time Stamp Configuration
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(scale, str(datetime.datetime.now()), (1, 530),
                    font, 1, (255, 255, 230), 2, cv2.LINE_AA)

        # Main Object
        if len(element(frame)) > 0:
            if detection:
                timer_started = False

            else:
                detection = True
                recording = record()
                print("Started Recording!")

        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    recording.release()
                    print('Stop Recording!')
            else:
                timer_started = True
                detection_stopped_time = time.time()

        if detection:
            recording.write(frame)

        cv2.imshow("cam_entrance", scale)

        x = cv2.waitKey(1) & 0xFF

        if x == ord("q"):
            break

    recording.release()
    cap.release()
    cap.destroyAllWindows()


if __name__ == "__main__":
    Cctv()
