#!/bin/bash

# Function to run the public repo scanner
run_public_repo_scanner() {
    echo "Starting public_repo_scanner..."
    python3 public_repo_scanner/public_repo_scanner.py
}

# Function to run the k8s scanner
run_k8s_scanner() {
    echo "Starting k8s_scanner..."
    python3 k8s_scanner/k8s_scanner.py
}

# Run both scanners in the background
run_public_repo_scanner &
PUBLIC_REPO_SCANNER_PID=$!

run_k8s_scanner &
K8S_SCANNER_PID=$!

# Wait for both processes to complete
wait $PUBLIC_REPO_SCANNER_PID
wait $K8S_SCANNER_PID
