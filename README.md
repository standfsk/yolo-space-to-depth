This is unofficial implementation of SP-YOLO on YOLOv7
- Paper: https://www.mdpi.com/2076-3417/13/14/8161
- YOLOv7: https://github.com/WongKinYiu/yolov7

## Intro
- Added dataset configuration file(VisDrone.yaml)
- Added model configurtion file(yolov7-SP.yaml)
- Added Space-to-depth module

## Model
![image](https://github.com/user-attachments/assets/0869f091-4c2e-4b76-a516-e5c5a15a9d39)

## Dataset
- VisDrone(https://github.com/VisDrone/VisDrone-Dataset)

## Preprocess
```
python preprocess.py
```

## Train
```
python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train.py --workers 4 --device 0,1,2,3 --sync-bn --batch-size 16 --data data/VisDrone.yaml --img 640 640 --cfg cfg/training/yolov7-SP.yaml --weights weights/yolov7_training.pt --hyp data/hyp.scratch.p5.yaml --name visdrone-yolov7s2d --exist-ok
```

## Test
```
python test.py --device 0 --data data/visdrone.yaml --img 640 --cfg cfg/training/yolov7-SP.yaml --weights runs/train/visdrone-yolov7s2d/weights/best.pt --name yolov7s2d
```

## Detect
```
python detect.py --device 0 --source sample.jpg --weights runs/train/visdrone-yolov7s2d/weights/best.pt --name yolov7s2d
```

## Result
![res](https://github.com/user-attachments/assets/b4e1ae3f-2660-4032-bcdc-811e6b26f9cd)
