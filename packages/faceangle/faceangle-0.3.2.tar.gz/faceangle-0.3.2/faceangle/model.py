"""Модели детектирования лиц, ключевых точек лица и оценки поворота головы"""

import cv2
from insightface.app import FaceAnalysis
import numpy as np
import onnxruntime as ort
from tqdm import tqdm
import warnings
import os

from .math import toSpheric
from .preprocessing import estimateNorm
from .visualization import drawBoundingBox, drawLandmarks, writeAngles, drawAxes

NOSE_2D_POS        = 86  # Порядковый номер кончика носа в наборе двумерных ключевых точек
NOSE_3D_POS        = 34  # Порядковый номер кончика носа в наборе трёхмерных ключевых точек
LANDMARKS_2D_NUM   = 106 # Количество двумерных ключевых точек
LANDMARKS_3D_NUM   = 68  # Количество трёхмерных ключевых точек
SELECTED_2D_LANDMARKS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                         10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                         20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                         30, 31, 32, 72, 73, 74, 75, 76, 77, 78, 79,
                         80, 81, 82, 83, 84, 85]     # Индексы двумерных ключевых точек овала лица и носа
SELECTED_3D_LANDMARKS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
                         27, 28, 29, 30, 31, 32, 33, 34] # Индексы трёхмерных ключевых точек овала лица и носа


class RepNet360:
    """
    Модель оценки положения головы в пространстве.
    Источник: https://github.com/thohemp/6DRepNet360
    """
    def __init__(self, angle_model_path):
        self.model = ort.InferenceSession(angle_model_path,
                                          providers=['CUDAExecutionProvider'])
    
    def run(self, image, face):
        box = face.bbox.astype(int)
        netInput = image[box[1]:box[3], box[0]:box[2]]
        if netInput.shape[0] * netInput.shape[1] == 0:
            return None
        
        netInput = cv2.resize(netInput, (224, 224))
        netInput = cv2.cvtColor(netInput, cv2.COLOR_BGR2RGB)
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        netInput = netInput / 255
        netInput = (netInput - mean) / std
        netInput = np.rollaxis(netInput, -1, 0)
        pitch, yaw, roll = self.model.run(output_names=None,
                             input_feed={'face': [netInput]})[0]
        
        return np.round(-yaw, 2)[0], np.round(-pitch, 2)[0], np.round(roll, 2)[0]


class WHENet:
    """
    Модель оценки положения головы в пространстве.
    Источник: https://github.com/Ascend-Research/HeadPoseEstimation-WHENet 
    """
    def __init__(self, angle_model_path):
        self.model = ort.InferenceSession(angle_model_path,
                                          providers=['CPUExecutionProvider'])
    
    def run(self, image, face):
        box = face.bbox.astype(int)
        netInput = image
        if netInput.shape[0] * netInput.shape[1] == 0:
            return None
        
        netInput = cv2.resize(netInput, (224, 224))
        netInput = cv2.cvtColor(netInput, cv2.COLOR_BGR2RGB)

        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        netInput = netInput / 255
        netInput = (netInput - mean) / std
        yaw, pitch, roll = self.model.run(output_names=None,
                                          input_feed={'face': [netInput]})
        return np.round(-yaw, 2)[0], np.round(-pitch, 2)[0], np.round(roll, 2)[0]

class Model:
    """
    Объект, предназначенный для обработки изображения лица человека.
    Включает детектирование лица на изображении, оценку двумерных
    и трёхмерных ключевых точек лица, извлечение биометрического вектора,
    а также оценку углов поворота головы.

    Члены данных
    ------------
    detector : insightface.app.FaceAnalysis
               Модель детектирования лица, оценки ключевых точек и извлечения
               биометрического вектора.

               По умолчанию используется совокупность моделей buffalo_l.
               Подробнее об используемых моделях:
               https://github.com/deepinsight/insightface/tree/master/model_zoo

               Ключевой метод объекта - get - возвращает список с информацией
               о каждом детектированном лице.
    
    angle_model : Object
                Модель оценки положения головы.
                Метод run возвращает углы наклона вдоль каждой плоскости 
                трёхмерного пространства.

    det_size :  tuple[int]
                Входной размер изображения для модели детектирования
    """
    def __init__(self, angle_model_name: str, angle_model_path: str=None,
                 det_size: tuple[int] = (448, 448), use_gpu: bool = True):
        """
        Аргументы
        ---------
        angle_model_name : str
                          Название модели оценки положения головы в пространстве.

        angle_model_path : str
                          Путь к onnx-файлу модели.
        
        det_size : tuple[int]
                   Размер входного слоя модели детектирования
        
        use_gpu : bool
                  Указатель на использование GPU.
        """
        warnings.filterwarnings("ignore")
        if use_gpu:
            self.providers = ["CUDAExecutionProvider"]
        else:
            self.providers = ["CPUExecutionProvider"]


        self.detector = FaceAnalysis(allowed_modules=['detection',
                                                      'landmark_2d_106',
                                                      'landmark_3d_68',
                                                      'recognition'],
                                     providers=self.providers)
        self.detector.prepare(ctx_id=0, det_size=det_size)
        self.det_size = det_size

        if angle_model_name == 'whenet':
            if angle_model_path == None:
                angle_model_path = os.path.join(os.path.dirname(__file__), 'models', 'WHENet.onnx')
            self.angle_model = WHENet(angle_model_path)

        elif angle_model_name == 'repnet360':
            if angle_model_path == None:
                angle_model_path = os.path.join(os.path.dirname(__file__), 'models', '6DRepNet360.onnx')
            self.angle_model = RepNet360(angle_model_path)

        elif angle_model_name == 'faceangle':
            if angle_model_path == None:
                angle_model_path = 'models/FaceAngle.onnx'
        
        else:
            raise ValueError('Unknown model name: ', angle_model_name)
    
    def process(self, image):
        """
        Получение информации о лицах на изображении.

        Аргументы
        ---------
        image : np.ndarray
                Изображение для обработки
        
        Возвращает
        ----------
        faces : list[dict]
                Список с информацией о каждом лице на изображении
        """
        faces = self.detector.get(image)
        for face in faces:
            face.landmarks2d = None
            face.landmarks3dProjection = None
            face.landmarks2dCentered = None
            face.landmarks3dCentered = None
            face.angle = None
            face.axes = None

            keypoints = face.kps.astype(int)
            matrix = estimateNorm(keypoints, min(self.det_size))
            inverseMatrix = cv2.invertAffineTransform(matrix)

            alignedImage = cv2.warpAffine(image, matrix, self.det_size, borderValue=0.0)
            alignedFaces = self.detector.get(alignedImage)

            if len(alignedFaces) > 0:
                lmks2d = alignedFaces[0].landmark_2d_106
                lmks3d = alignedFaces[0].landmark_3d_68

                lmks2dForTransform = np.hstack([lmks2d, np.ones((LANDMARKS_2D_NUM, 1))]).T
                lmks3dForTransform = np.hstack([lmks3d[:, :2], np.ones((LANDMARKS_3D_NUM, 1))]).T

                face.landmarks2d = (np.dot(inverseMatrix,
                                                    lmks2dForTransform).T)[:, :2].astype(int)
                face.landmarks3dProjection = (np.dot(inverseMatrix,
                                              lmks3dForTransform).T)[:, :2].astype(int)

                lmks2d /= min(self.det_size)
                lmks3d /= min(self.det_size)

                lmks2dExceptNose = np.vstack([lmks2d[:NOSE_2D_POS - 1, :], lmks2d[NOSE_2D_POS:, :]])
                nose2d = lmks2d[NOSE_2D_POS, :]
                lmks2dCentered = lmks2dExceptNose - nose2d

                lmks3dExceptNose = np.vstack([lmks3d[:NOSE_3D_POS - 1, :], lmks3d[NOSE_3D_POS:, :]])
                nose3d = lmks3d[NOSE_3D_POS, :]
                lmks3dCentered = lmks3dExceptNose - nose3d

                face.landmarks2dCentered = lmks2dCentered
                face.landmarks3dCentered = lmks3dCentered

                face.angle = self.angle_model.run(image, face)

                if face.angle is not None:
                    box = face.bbox.astype(int)
                    
                    h = box[3] - box[1]
                    w = box[2] - box[0]

                    tdx = box[0] + w / 2
                    tdy = box[1] + h / 2

                    size = max(w, h) / 2
                    
                    yaw = face.angle[0] * np.pi / 180
                    pitch = -face.angle[1] * np.pi / 180
                    roll = face.angle[2] * np.pi / 180

                    x1 = size * (np.cos(yaw) * np.cos(roll)) + tdx
                    y1 = size * (np.cos(pitch) * np.sin(roll) + np.cos(roll) * np.sin(pitch) * np.sin(yaw)) + tdy

                    x2 = size * (-np.cos(yaw) * np.sin(roll)) + tdx
                    y2 = size * (np.cos(pitch) * np.cos(roll) - np.sin(pitch) * np.sin(yaw) * np.sin(roll)) + tdy

                    x3 = size * (np.sin(yaw)) + tdx
                    y3 = size * (-np.cos(yaw) * np.sin(pitch)) + tdy

                    face.axes = ((int(tdx), int(tdy)),
                                (int(x1), int(y1)),
                                (int(x2), int(y2)),
                                (int(x3), int(y3)))
        
        return faces
    
      
    def processImage(self, image, draw_bbox=True, draw_lmks='2d', write_angle=True, draw_axes=True):
        faces = self.process(image)
        processedImage = image.copy()
        if len(faces) > 0:
            for face in faces:
                if draw_bbox:
                    box = face.bbox.astype(int)
                    processedImage = drawBoundingBox(processedImage, box)

                if face.landmarks3dProjection is not None and draw_lmks == "3d":
                    processedImage = drawLandmarks(processedImage, face.landmarks3dProjection.astype(int))

                if face.landmarks2d is not None and draw_lmks == "2d":
                    processedImage = drawLandmarks(processedImage, face.landmarks2d.astype(int))

                if face.angle is not None and write_angle:
                    phi, th, _ = face.angle
                    processedImage = writeAngles(processedImage, box, phi, th)
                
                if face.axes is not None and draw_axes:
                    processedImage = drawAxes(processedImage, face.axes)

            return processedImage
            
        else:
            return None
    
    def processVideo(self, video, draw_bbox=True, draw_lmks="2d", write_angle=True, draw_axes=True):
        frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frameWidth = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        clip = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype("uint8"))

        fc = 0
        ret = True

        while fc < frameCount and ret:
            ret, clip[fc] = video.read()
            fc += 1

        video.release()

        frames = []
        for frame in clip:
            frames.append(frame)

        processed_frames = []
        for frame in tqdm(frames):
            processed_image = self.processImage(frame, draw_bbox, draw_lmks, write_angle, draw_axes)
            if processed_image is None:
                processed_frames.append(frame)
            else:
                processed_frames.append(processed_image)
        
        return processed_frames


# class AngleEstimator(FaceDetector):
#     def __init__(self, model_name, angle_estimator_path, det_size = (448, 448), angle_size = (448, 448), use_gpu = True):
#         super().__init__(det_size, use_gpu)
#         self.angle_estimator = ort.InferenceSession(angle_estimator_path,
#                                                     providers=['CPUExecutionProvider'])
#         self.angle_size = angle_size
#         self.model_name = model_name.lower()
#         if model_name.lower() not in ['faceangle', '6drepnet360', 'whenet']:
#             raise ValueError(f"Unknown model name: {model_name}")
    
#     def faceAngleProcessor(self, face):
#         if face.landmarks3dCentered is not None:
#             k = LANDMARKS_3D_NUM - 1
#             lmksForAngle = face.landmarks3dCentered.reshape(1, k * 3)
#             x, y, z = self.angle_estimator.run(None, {"landmarks": lmksForAngle})[0][0]
#             r, phi, th = toSpheric(x, y, z)
#             return phi, th
#         else:
#             return None

#     def process(self, image):
#         faces = super().process(image)
#         for face in faces:
#             if self.model_name == 'faceangle':
#                 phi, th = self.faceAngleProcessor(face)
#                 roll = 0
#             elif self.model_name == 'whenet':
#                 angle = self.WHENetProcessor(image, face)
#             face.angle = angle
        
#         return faces