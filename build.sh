#!/bin/bash

# Install system dependencies needed for scipy and scientific packages
apt-get update
apt-get install -y \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libgomp1

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies and build
cd frontend
npm install
npm run build
