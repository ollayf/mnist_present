# MNIST Present
The project is split into 3 parts:
- Detector
- Frontend
- Backend + Tensorflow server

# Detector

## Start training
- Access the detector/utils folder
- Create a new model using keras API in models.py
- Create new models folder by duplicating template_arch, and then changing the name of this folder
- Inside train.py, edit:
    - `ARCH_DIR = './models/arch10'`
    - `model = models.build_arch10(learning_rate = LR)`

# Frontend

## Setup
Go into the frontend folder
```
npm install
npm start
```