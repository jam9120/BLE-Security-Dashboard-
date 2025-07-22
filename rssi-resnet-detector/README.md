# RSSI ResNet Detector

This module contains a simple pipeline for training a ResNet model on RSSI screenshot images to classify anomalies or identify BLE devices.

## Directory Layout

```
rssi-resnet-detector/
├── data/
│   ├── train/
│   ├── val/
│   └── test/
├── models/
│   └── resnet_rssi.py
├── utils/
│   └── dataset_loader.py
├── train.py
├── eval.py
├── requirements.txt
```

Place your images under the `data` directories in class-specific folders and run `train.py` to start training.
