import cv2
import time
import datetime

# Cameras

cap = cv2.VideoCapture("Your RSTP/IP Camera HERE")


# Instances
detection = False
detection_stopped_time = None
timer_started = False

SECONDS_TO_RECORD_AFTER_DETECTION = 5


# methods

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def element(frame):
    face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # body = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # person = body.detectMultiScale(gray, 1.8, 2)
    faces = face.detectMultiScale(gray, 1.8, 5)

    return faces


def record():
    current_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    frame_size = (int(cap.get(3)), int(cap.get(4)))

    film = cv2.VideoWriter(
        f"{current_time}.mp4", fourcc, 20, frame_size)
    return film


class Cctv:
    while True:
        _, frame = cap.read()

        scale = rescale_frame(frame, 75)
        element(frame)

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

        x = cv2.waitKey(1)

        if x == ord("q"):
            break

    recording.release()
    cap.release()
    cap.destroyAllWindows()


if __name__ == "__main__":
    Cctv()
