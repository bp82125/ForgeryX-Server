# ForgeryX (Server)

ForgeryX is an image forensics tool designed to detect manipulated images. This repository contains the server-side component built with FastAPI, which leverages the Photoholmes library for implementing various forgery detection algorithms. It works in conjunction with the ForgeryX client to provide visual analysis and predictions of potentially edited areas in images.

Check out: [ForgeryX (Client)](https://github.com/bp82125/ForgeryX-Client)

## Technologies Used
- **Photoholmes**: Providing state-of-the-art method implementations and evaluation tools.
- **PyWavelets**: Wavelet transform library for image processing.
- **ExifTool**: EXIF metadata extraction tool.
- **FastAPI**: Backend framework handling processing logic and API endpoints.
- **Python**: Core programming language used for backend processing.

## Getting Started

### Prerequisites
- Python version 3.10 or higher.
- (Optional) WSL2 with Ubuntu 24.04 for a Linux-based development environment.

## Installation

### Clone the Photoholmes Repository (My fork)
```bash
git clone https://github.com/bp82125/photoholmes.git
```

### Install Miniconda
Download and install Miniconda from the [official website](https://docs.conda.io/en/latest/miniconda.html) based on your operating system.

### Create and Activate a Conda Environment

```bash
# Create a new conda environment with Python 3.10
conda create -n forgeryx python=3.10

# Activate the environment
conda activate forgeryx
```

### Install Photoholmes as a Python Library

```bash
# Navigate to the photoholmes directory
cd photoholmes

# Install Photoholmes from the cloned repository
pip install -e .

# Return to the parent directory
cd ..
```

### Clone the ForgeryX (Server) Repository
```bash
git clone https://github.com/bp82125/ForgeryX-Server.git
cd ForgeryX-Server
```

### Install Project Dependencies

```bash
# Install the required packages from requirements.txt
pip install -r requirements.txt
```

### Install ExifTool

ExifTool is required for metadata extraction.

1. Download and install ExifTool from the [official website](https://exiftool.org/) based on your operating system
2. Verify installation by running:
```bash
exiftool -ver
```

### Download Model Weights for Photoholmes Methods

Some detection methods in Photoholmes require pre-trained model weights. Download them from their respective repositories and place them in the appropriate directories:

- [TruFor](https://github.com/bp82125/photoholmes/blob/main/src/photoholmes/methods/trufor/README.md)
- [EXIF As Language](https://github.com/bp82125/photoholmes/blob/main/src/photoholmes/methods/exif_as_language/README.md) (Remember to run the prune weights command after downloading)
- [CAT-Net](https://github.com/bp82125/photoholmes/blob/main/src/photoholmes/methods/catnet/README.md)
- [Mesorch](https://github.com/bp82125/photoholmes/blob/main/src/photoholmes/methods/mesorch/README.md)


Expected weights directory structure:
```
photoholmes
└── weights
    ├── catnet
    │   └── weights.pth
    ├── exif_as_language
    │   ├── weights.pth
    │   └── wrapper_75_new.pth
    ├── mesorch
    │   └── mesorch.pth
    └── trufor
        └── trufor.pth.tar
```
## Run the Project

Once the environment is set up, you can start the project:
```bash
uvicorn app.main:app --reload
```
This will launch the application. You should see an output similar to the following:
```bash
...
WARNING -  CatNet is under a license that only allows research use. You can check the license inside the method folder's or at https://github.com/mjkwon2021/CAT-Net/blob/main/README.md#licence. If you use this method, you are agreeing to the terms of the license.
INFO:     Started server process [25608]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```


