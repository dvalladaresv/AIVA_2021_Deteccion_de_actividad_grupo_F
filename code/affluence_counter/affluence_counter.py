import os
import cv2
import argparse
import wget
import time
from detector import Detector
from tracker import Tracker


def parse_parameters():
    """
    Parametros necesarion para lanzar el programa

    :return args -> Argumentos pasados por la línea de comandos
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", help="input video path", required=True, type=str)
    args = parser.parse_args()
    return args


class AffluenceCounter:
    """
        Encargada de procesar el vídeo que se le pasa como entrada y obtener la contabilizacion
    """
    PATH_WEIGHTS = "../assets/model/yolov3.weights"
    PATH_CFG = "../assets/model/yolov3.cfg"

    def __init__(self, path_video):
        self.path_video = path_video

    def process_video(self):
        """
            Encargada de procesar el video

        :return: nº de personas que entran y nº de personas que pasan de largo
        """

        if not os.path.exists(self.PATH_WEIGHTS):
            print("downloading checkpoint yolov3.weights... wait please.")
            wget.download("https://pjreddie.com/media/files/yolov3.weights", "../assets/model/")

        det_inst = Detector(self.PATH_WEIGHTS, self.PATH_CFG)
        tracker_inst = Tracker()
        cap = cv2.VideoCapture(self.path_video)
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            start = time.time()
            bboxes = det_inst.detect_image(frame)  # Detectar personas en el frame
            tracker_inst.update_trackers_by_dets(frame, bboxes)  # Actualizar los bbox de los tracker
            tracker_inst.track(frame)  # Actualizar el seguimiento de las personas
            tracker_inst.check_trackers()  # Comprobar el estado de las personas
            frame_count += 1
            print("Frame: {0}, time: {1}".format(frame_count, time.time() - start))
        return tracker_inst.get_counter_enter(), tracker_inst.get_counter_pass()


if __name__ == '__main__':
    args = parse_parameters()
    app = AffluenceCounter(args.video_path)
    count_enter, count_not = app.process_video()
    print("Personas que han entrado en la tienda: " + str(count_enter))
    print("Personas que han pasado de largo: " + str(count_not))
