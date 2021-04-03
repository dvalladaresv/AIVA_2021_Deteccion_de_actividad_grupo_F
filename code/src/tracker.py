import cv2

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "mil": cv2.TrackerMIL_create
}

class Track():

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
        success, self._bbox = self._tracker.update(frame)

        self.update_centroid()
    def update_centroid(self):
        self.x_last = self.x
        self.y_last = self.y
        self.x = int(self._bbox[0] + (self._bbox[2])/2)
        self.y = int(self._bbox[1] + (self._bbox[3])/2)


    def draw_bbox(self, frame):
        (x, y, w, h) = [int(v) for v in self._bbox]
        cv2.circle(frame,(self.x, self.y), 3, (0,0,255), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(frame, "{0}".format(self._id), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), thickness=2)

    def is_finish_track(self):
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
        return self._bbox

    def update_bbox(self, bbox):
        self._bbox = bbox
        self.update_centroid()

    def get_id(self):
        return self._id

    def check_bb_size(self):
        if (self._bbox[2] > self._frame_width / 3) or (self._bbox[3] > self._frame_height / 3):
            return False
        return True

    def get_status(self):
        return self.status

    def update_status(self):
        self._ref_left()
        self._ref_right()
        self._ref_door()

    def _ref_left(self):
        left_ref = self.references["left"]
        if left_ref[0] < self.x < left_ref[1] and not "L" in self.status:
            self.status = self.status + "L"
            print("DENTRO DE L")

    def _ref_right(self):
        right_ref = self.references["right"]
        if right_ref[0] < self.x < right_ref[1] and not "R" in self.status:
            self.status = self.status + "R"
            print("DENTRO DE R")

    def _ref_door(self):
        door_ref = self.references["door"]
        if door_ref[0] < self.y < door_ref[1] and not "P" in self.status and self.y_last > self.y:
            self.status = self.status + "PP"
            print("DENTRO DE P")

    def is_timeout(self):
        if self.x == self.x_last and self.y == self.y_last:
            self.timeout = self.timeout + 1
        else:
            self.timeout = 0
        if self.timeout >= 5:
            return True
        else:
            return False


class Tracker():
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
        import operator
        bb1 = tuple(map(operator.mul, bboxes[better_bb_index], (.6, .6, .6, .6)))
        bb2 = tuple(map(operator.mul, bboxes[int(not better_bb_index)], (.4, .4, .4, .4)))
        return tuple(map(operator.add, bb1, bb2))


    def update_trackers_by_dets(self, frame, bboxes):
        for bbox in bboxes:
            add_new = True
            for tr in self._trackers:
                bb = [bbox, tr.get_bbox()]
                indicates = cv2.dnn.NMSBoxes(bb, [1.,.9], self.CONF_THRESHOLD, self.NMS_THRESHOLD)
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
        return self.counter_pass

    def get_counter_enter(self):
        return self.counter_enter

    def check_trackers(self):
        for tr in self._trackers:
            status = tr.get_status()
            if len(status) >= 2:
                if status == "LR" or status == "RL":
                    self.counter_pass = self.counter_pass + 1
                elif status == "LPP" or status == "RPP":
                    self.counter_enter = self.counter_enter + 1

                self.remove_track(tr)

    def remove_track(self, tr):
        index = self._trackers.index(tr)
        self._trackers.pop(index)
        del tr  # free the memory of i

    def track(self, frame):

        for track in self._trackers:
            track.update(frame)
            track.update_status()
            if track.is_timeout():
                self.remove_track(track)

        for track in self._trackers:
            track.draw_bbox(frame)

        def f(tr):
            return not tr.is_finish_track()

        self._trackers = list(filter(f, self._trackers))


        return frame