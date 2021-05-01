import unittest
import sys
import cv2

sys.path.append("../app")
from detector import Detector


class TestDetectorPerson(unittest.TestCase):

    def test_detector_two_person(self):
        path_img = "img/detector_test.png"
        img = cv2.imread(path_img)
        det_inst = Detector("../assets/model/yolov3.weights", "../assets/model/yolov3.cfg")
        bboxes = det_inst.detect_image(img)
        self.assertEqual(2, len(bboxes))


if __name__ == "__main__":
    unittest.main()  # llama a la clase unittest y ejecuta los test que se tienen definidos
