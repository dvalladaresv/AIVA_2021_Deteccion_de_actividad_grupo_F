import csv
import cv2
from PersonsEntering import PersonsEntering
from Personsleaving import Personsleaving

class MakeTests():
    def __init__(self):
        self.detector = PersonsEntering()
        self.detector1 = Personsleaving()
        self.sucess = 0
        self.test = 0
        with open('groundtruh/via_project_2Mar2021_18h59m.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_counter = 0
            for row in csv_reader:
                if line_counter > 0:
                    file_name = row[0]
                    x = int(row[4])
                    y = int(row[5])
                    width = int(row[6])
                    height = int(row[7])
                    result = row[8]
                    self._procesar(file_name, x, y, width, height, result)
                line_counter += 1

    def _procesar(self, file_name, x, y, width, height, groundtruth):
        img = cv2.imread(file_name)
        result = self.detector(img)
        self.test += 1
        if result == groundtruth:
            self.sucess +=1


if __name__ == "__main__":
    m = MakeTests()