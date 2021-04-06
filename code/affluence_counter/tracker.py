import cv2

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "mil": cv2.TrackerMIL_create
}


class Track:
    """
        Seguimiento de una persona
    """

    def __init__(self, tracker_name, first_frame, bbox, id, references):
        self._tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()
        self._bbox = bbox
        self._tracker.init(first_frame, bbox)
        self._frame_height, self._frame_width, _ = first_frame.shape
        self._id = id
        self.status = ""
        self.references = references
        self.x = 0
        self.y = 0
        self.x_last = 0
        self.y_last = 0
        self.timeout = 0
        self.update_centroid()

    def update(self, frame):
        """
            Actualizar posiciones de seguimiento

        :param frame: Imagen
        """
        success, self._bbox = self._tracker.update(frame)
        self.update_centroid()

    def update_centroid(self):
        """
            Calcular el centro del bbox del track
        """
        self.x_last = self.x
        self.y_last = self.y
        self.x = int(self._bbox[0] + (self._bbox[2]) / 2)
        self.y = int(self._bbox[1] + (self._bbox[3]) / 2)

    def is_finish_track(self):
        """
            Comprobar si ha finalizado el seguimiento
        """
        bb_area = self._bbox[2] * self._bbox[3]

        xmin = max(0, self._bbox[0])
        ymin = max(0, self._bbox[1])
        xmax = min(self._frame_width, self._bbox[0] + self._bbox[2])
        ymax = min(self._frame_height, self._bbox[1] + self._bbox[3])

        bb_inner_area = (xmax - xmin) * (ymax - ymin)

        try:
            percent_in_area = bb_inner_area / bb_area
        except ZeroDivisionError:
            return False
        if percent_in_area < 0.8:
            return True
        return False

    def get_bbox(self):
        """
        :return: bbox de track
        """
        return self._bbox

    def update_bbox(self, bbox):
        """
            Actualizar las posiciones

        :param bbox:
        """
        self._bbox = bbox
        self.update_centroid()

    def get_id(self):
        """
        :return: identificador del track
        """
        return self._id

    def check_bb_size(self):
        """
            Comprobar si el tamaño de la bbox es aceptable

        :return: boolean
        """
        if (self._bbox[2] > self._frame_width / 3) or (self._bbox[3] > self._frame_height / 3):
            return False
        return True

    def get_status(self):
        """
        :return: Estado del track
        """
        return self.status

    def update_status(self):
        """
            Actualizar estado del track
        """
        self._ref_left()
        self._ref_right()
        self._ref_door()

    def _ref_left(self):
        """
            Comprobar si el track esta en la región de ref. izquierda
        """
        left_ref = self.references["left"]
        if left_ref[0] < self.x < left_ref[1] and not "L" in self.status:
            self.status = self.status + "L"

    def _ref_right(self):
        """
            Comprobar si el track esta en la región de ref. derecha
        """
        right_ref = self.references["right"]
        if right_ref[0] < self.x < right_ref[1] and not "R" in self.status:
            self.status = self.status + "R"

    def _ref_door(self):
        """
            Comprobar si el track esta en la región de ref. puerta
        """
        door_ref = self.references["door"]
        if door_ref[0] < self.y < door_ref[1] and not "P":
            self.status = self.status + "P"

    def is_timeout(self):
        """
            Comprobar si se ha producido un timeout del track
        """
        if self.x == self.x_last and self.y == self.y_last:
            self.timeout = self.timeout + 1
        else:
            self.timeout = 0
        if self.timeout >= 5:
            return True
        else:
            return False


class Tracker:
    """
        Controlar el seguimiento de las personas
    """
    references = {"left": (20, 120), "right": (320, 400), "door": (60, 120)}
    TRACKER_TYPE = "csrt"
    CONF_THRESHOLD = 0.82
    NMS_THRESHOLD = 0.1

    def __init__(self):
        self._trackers = []
        self._last_bboxes = None
        self._track_id = 0
        self.counter_enter = 0
        self.counter_pass = 0

    def refresh_bbox(self, bboxes, better_bb_index):
        """
            Actualizar las bbox
        :param bboxes: bboxes actuales
        :param better_bb_index: Indices de la mejor bbox propuesta
        :return: tupla com la bbox actualizada
        """
        import operator
        bb1 = tuple(map(operator.mul, bboxes[better_bb_index], (.6, .6, .6, .6)))
        bb2 = tuple(map(operator.mul, bboxes[int(not better_bb_index)], (.4, .4, .4, .4)))
        return tuple(map(operator.add, bb1, bb2))

    def update_trackers_by_dets(self, frame, bboxes):
        """
            Actualizar las bboxes de los tracks existentes o crear un nuevo track

        :param frame: Imagen
        :param bboxes: Nuevos bboxes detectadas por el detector
        """

        for bbox in bboxes:
            add_new = True
            for tr in self._trackers:
                bb = [bbox, tr.get_bbox()]
                indicates = cv2.dnn.NMSBoxes(bb, [1., .9], self.CONF_THRESHOLD, self.NMS_THRESHOLD)
                if indicates.size == 1:
                    add_new = False

                    new_bbox = self.refresh_bbox(bb, indicates[0][0])
                    tr.update_bbox(new_bbox)

            if add_new:
                new_track = Track("csrt", frame, bbox, self._track_id, references=self.references)
                if not new_track.is_finish_track() and new_track.check_bb_size():
                    self._trackers.append(new_track)
                    self._track_id += 1

    def get_counter_pass(self):
        """
            Contador de personas que no entran en la tienda

        :return: Nº de personas que pasan de largo
        """
        return self.counter_pass

    def get_counter_enter(self):
        """
            Contador de personas que entran en la tienda

        :return: Nº de personas que entran
        """
        return self.counter_enter

    def check_trackers(self):
        """
            Comprobar el estado del seguimiento de las personas para sumar contadores
        """
        for tr in self._trackers:
            status = tr.get_status()
            if len(status) >= 2:
                if status == "LR" or status == "RL":
                    self.counter_pass = self.counter_pass + 1
                elif status == "LP" or status == "RP":
                    self.counter_enter = self.counter_enter + 1

                self.remove_track(tr)

    def remove_track(self, tr):
        """
            Remover un tracker de la lista de trackers

        :param tr: Tracker a eliminar
        """
        index = self._trackers.index(tr)
        self._trackers.pop(index)
        del tr

    def track(self, frame):
        """
            Actualizar el seguimiento de las personas:
                - Actualizar estados
                - Eliminar tracker finalizados o con timeout

        :param frame: Imagen
        """

        for track in self._trackers:
            track.update(frame)
            track.update_status()
            if track.is_timeout():
                self.remove_track(track)

        def f(tr):
            return not tr.is_finish_track()
        self._trackers = list(filter(f, self._trackers))

        return frame
