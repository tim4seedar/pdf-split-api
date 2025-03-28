# PDF Split API

A simple REST API built with Python that accepts a PDF file upload, splits it into individual pages, and returns a JSON response. This project uses PyPDF2 for handling PDF operations and can be deployed on Render.

## Features

- **PDF Splitting:** Upload a multi-page PDF and have it split into single-page documents.
- **Easy Deployment:** Designed for deployment on Render via a GitHub repository.
- **Extendable:** Serves as a foundation for future integrations (e.g., OCR processing using GPT).

## Technology Stack

- **Python 3.x**
- **Flask** (or [FastAPI](https://fastapi.tiangolo.com/) if preferred)
- **PyPDF2**
- **Gunicorn** (for production deployment)
- **Render** (cloud hosting)

## Getting Started

### Prerequisites

- Python 3.x installed
- `pip` package manager

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/pdf-split-api.git
   cd pdf-split-api
#   p d f - s p l i t - a p i  
 