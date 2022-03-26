# CogNative
## Translated Voice Synthesis

Clone a voice and output speech in another language with the original voice.

## Installation

### 1. Install Python:

  Python 3.9 is recommended.

### 2. Create virtual environment (optional):
  ```python3 -m venv pyvenv```

  Activate virtual environment:
  Windows: ```./pyvenv/Scripts/activate```
  MacOS/Linux: ```source pyvenv/bin/activate```

  Deactivating the virtual environment:
  ```deactivate```

### 3. Install [ffmpeg](https://ffmpeg.org/download.html#get-packages). 

Once installed, extract the folder and add ```<ffmpeg folder path>/bin``` to path.
  
### 4. Install [PyTorch](https://pytorch.org/get-started/locally/):
  1. Pytorch Build: Stable (1.11.0).
  2. Your OS: Pick the OS your environment is running CogNative in (Windows or Linux recommended).
  3. Package: Pick what package installer you are using (pip recommended).
  4. Language: Python.
  5. Compute Platform: CUDA 11.3 recommended. If you don't have a GPU pick CPU.
  
### 5. Install required Python packages:
```pip3 install -r requirements.txt```

### 6. Install [models](https://drive.google.com/drive/folders/1fipYnvRT3vayNuGvhfuX1hL0ZC4mEAfs?usp=sharing).

  Once installed, add the models (*.pt) to ```CogNative/CogNative/models/Real-Time-Voice-Cloning/saved_models/default```

## Contributing to the project

- Create your own branch ```git branch yourname-feature-name```
- Pull request with a good explanation of your branch
- Include issues that your pull request is addressing
- Squash and Merge, always.

## Python Styleguide

This style guide is important to make sure that all style matches throughout the project.
To style your code, please use the Black Python styler.

Single file:    ```black <python-file-name>```
All files:      ```black .```

## Credit to Real-Time-Voice-Cloning

This github repository serves as the foundation of our voice cloning module.

[Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)

See license [here](CogNative/backend/Real-Time-Voice-Cloning/LICENSE.md).

## Team Members

- Andrew Fennell
- Austin Currington
- Xingjian Hao
- Connor Tisdel
- Jacob Smith
- Aref Sadeghi

