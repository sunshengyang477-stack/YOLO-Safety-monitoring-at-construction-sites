#coding:utf-8
#根据实际情况更换模型
# yolov8n.yaml (nano)：轻量化模型，适合嵌入式设备，速度快但精度略低。
# yolov8s.yaml (small)：小模型，适合实时任务。
# yolov8m.yaml (medium)：中等大小模型，兼顾速度和精度。
# yolov8b.yaml (base)：基本版模型，适合大部分应用场景。
# yolov8l.yaml (large)：大型模型，适合对精度要求高的任务。

from ultralytics import YOLO

model_path = 'yolov8m.pt'
data_path = 'data.yaml'

if __name__ == '__main__':
    model = YOLO(model_path)
    results = model.train(data=data_path,
                          epochs=500,
                          batch=8,
                          device='0',
                          workers=0,
                          project='runs',
                          name='exp',
                          )








