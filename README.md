# Brain Tumor Segmentation AI

This project is an AI-powered system for brain tumor segmentation from MRI scans. It consists of three main components:

- **AI Model**: A deep learning model trained to segment brain tumors from MRI images.
- **Backend (Flask)**: A lightweight backend API that serves the AI model and processes image requests.
- **Frontend (React)**: A web-based interface that allows users to upload MRI images and visualize the segmentation results.

## Features
- Upload MRI scans for processing
- AI-based brain tumor segmentation
- Visual representation of the results
- REST API for model inference

## Tech Stack
- **Backend**: Flask, TensorFlow/PyTorch (for AI model)
- **Frontend**: React, TailwindCSS
- **Virtualization**: Docker (optional), REST API

## Usage

### Docker
```bash
    cd app
    docker compose up -d
```
## License
This project is open-source under the MIT License.
