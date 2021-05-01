import unittest
import sys


sys.path.append("../app/")
from affluence_counter import AffluenceCounter


class TestCounterPerson(unittest.TestCase):

    def test_one_person_enter(self):
        path_video = "../../videos/1_EnterExitCrossingPaths1front.mpg"
        app = AffluenceCounter(path_video)
        count_enter, count_noenter, time_process = app.process_video()
        self.assertEqual(count_enter, 1)
        self.assertEqual(count_noenter, 0)


if __name__ == "__main__":
    unittest.main()  # llama a la clase unittest y ejecuta los test que se tienen definidos
