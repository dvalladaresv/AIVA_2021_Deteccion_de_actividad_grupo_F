import unittest
import sys
import cv2

sys.path.append("../affluence_counter")
from detector import Detector
from tracker import Tracker

class TestTracker(unittest.TestCase):

    def test_tracker_two_person(self):
        path_img = "img/detector_test.png"
        img = cv2.imread(path_img)
        det_inst = Detector("../assets/model/yolov3.weights", "../assets/model/yolov3.cfg")
        tracker_inst = Tracker()
        res, bboxes, _ = det_inst.detect_image(img)
        tracker_inst.update_trackers_by_dets(img, bboxes)
        tracker_inst.track(img)
        self.assertEqual(2, tracker_inst._track_id)


class TestTrack(unittest.TestCase):

    def test_track_person_inside_ref_right(self):
        path_img = "img/track_left.png"
        img = cv2.imread(path_img)
        det_inst = Detector("../assets/model/yolov3.weights", "../assets/model/yolov3.cfg")
        tracker_inst = Tracker()
        res, bboxes, _ = det_inst.detect_image(img)
        tracker_inst.update_trackers_by_dets(img, bboxes)
        tracker_inst.track(img)
        tracker_inst.check_trackers()
        self.assertEqual("L", tracker_inst._trackers[0].get_status())



if __name__ == "__main__":
    unittest.main()  # llama a la clase unittest y ejecuta los test que se tienen definidos
