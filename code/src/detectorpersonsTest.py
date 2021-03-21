import unittest
import cv2
from PersonsEntering import PersonsEntering
from Personsleaving import Personsleaving

class TestDetectorPersons(unittest.TestCase):



    def test_DetectorEntrada(self):
        vídeos = cv2.imread("dataset_2/EnterExitCrossingPaths1front.mpg")
        detectorentranda = PersonsEntering()
        result = detectorentranda.detectors(vídeos)
        self.assertEqual(result, "Personas que entraron en la tienda")  # El método assertEqual compara que el resultado obtenido y el esperado es el mismo


    def test_DetectorNoentran(self):
        vídeos = cv2.imread("dataset_2/OneLeaveShopReenter1front.mpg")
        detectorsalida= Personsleaving()
        result = detectorsalida.detectors1(vídeos)
        self.assertEqual(result, "Personas que pasan por la tienda")  # El método assertEqual compara que el resultado obtenido y el esperado es el mismo

 def test_RecuentoPers(self):
        vídeos = cv2.imread("dataset_2/OneLeaveShopReenter1front.mpg")
        detectorsalida= Personsleaving()
        result = detectorsalida.detectors1(vídeos)
        self.assertEqual(result, "Personas que pasan por la tienda")  # El método assertEqual compara que el resultado obtenido y el esperado es el mismo


if __name__ == "__main__":
    unittest.main()  # llama a la clase unittest y ejecuta los test que se tienen definidos
