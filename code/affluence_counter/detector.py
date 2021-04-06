import cv2
import numpy as np

class Detector:
    """
        Detectar personas en la imagen
    """
    SCALE = 1 / 255.0
    CONF_THRESHOLD = 0.9
    NMS_THRESHOLD = 0.4

    def __init__(self, yolo_weights_path, yolo_config_path):

        self._net = cv2.dnn.readNet(yolo_weights_path, yolo_config_path)
        self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL_FP16)
        self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._frame_width = 0
        self._frame_height = 0

    def detect_image(self, frame):
        """
            Detectar personas en una imagen

        :param frame -> Imagen
        :return bboxes -> Lista con los bboxes detectados
        """
        bboxes = []

        self._frame_width = frame.shape[1]
        self._frame_height = frame.shape[0]

        blob = cv2.dnn.blobFromImage(frame, self.SCALE, (416, 416), (0, 0, 0), True, crop=False)
        self._net.setInput(blob)
        outs = self._net.forward(self.get_output_layers())

        class_ids = []
        confidences = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if class_id == 0 and confidence > self.CONF_THRESHOLD:
                    center_x = int(detection[0] * self._frame_width)
                    center_y = int(detection[1] * self._frame_height)
                    w = int(detection[2] * self._frame_width)
                    h = int(detection[3] * self._frame_height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    bboxes.append((int(x), int(y), int(w), int(h)))

        cv2.dnn.NMSBoxes(bboxes, confidences, self.CONF_THRESHOLD, self.NMS_THRESHOLD)

        return bboxes

    def get_output_layers(self):
        """
            Obtener capas de la red

        :return:  output_layers -> Lista con las capas de la red
        """
        layer_names = self._net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]
        return output_layers
