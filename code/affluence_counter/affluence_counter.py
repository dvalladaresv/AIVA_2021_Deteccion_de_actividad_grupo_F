import os

import cv2
import time
import argparse
import wget
from detector import Detector
from tracker import Tracker
import imutils


def parse_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", help="input video path", required=False, type=str)
    parser.add_argument("--output_video_path",
                        help="output video path (if not filled so output will be printed to screen)",
                        default="", type=str)
    args = parser.parse_args()
    return args


class AffluenceCounter:
    def __init__(self, path_video):
        self.path_video = path_video

    def draw_gridlines(self, img):
        (height, width) = img.shape[:2]
        for h in range(0, height):
            h = h * 20
            cv2.line(img, (0, h), (width, h), (70, 70, 70), 1);
            cv2.putText(img, str(h), (0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        for w in range(0, width):
            w = w * 20
            cv2.line(img, (w, 0), (w, height), (70, 70, 70), 1);
            cv2.putText(img, str(w), (w - 20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    def process_video(self):

        if not os.path.exists("../assets/model/yolov3.weights"):
            print("downloading checkpoint yolov3.weights... wait please.")
            wget.download("https://pjreddie.com/media/files/yolov3.weights")
        det_inst = Detector("../assets/model/yolov3.weights", "../assets/model/yolov3.cfg")

        cap = cv2.VideoCapture(self.path_video)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

        tracker_inst = Tracker()
        frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            self.draw_gridlines(frame)
            res, bboxes, _ = det_inst.detect_image(frame)
            tracker_inst.update_trackers_by_dets(frame, bboxes)
            tracker_inst.track(frame)
            tracker_inst.check_trackers()
            # show the output frame

            # cv2.rectangle(frame, (20, 140), (120, 200), (250, 0, 0), 2)  # Left
            # cv2.rectangle(frame, (320, 120), (400, 200), (250, 0, 0), 2)  # Right
            # cv2.rectangle(frame, (220, 60), (320, 120), (0, 250, 0), 2)  # Door
            # cv2.imshow("Output", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            frames += 1
            # print("Frame: {0}, time: {1}".format(frames, time.time() - start))

        return tracker_inst.get_counter_enter(), tracker_inst.get_counter_pass()


if __name__ == '__main__':
    args = parse_parameters()
    app = AffluenceCounter(args.video_path)
    print(app.process_video())
