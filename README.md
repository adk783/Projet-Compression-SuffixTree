# Ziv-Lempel Compression with Suffix Trees

## 📄 Description
This project implements a **lossless text compression tool** based on the **Ziv-Lempel algorithm (LZ77)**.

Unlike naive implementations that scan the past linearly (O(n^2)), we utilize a **Suffix Tree built with Ukkonen's Algorithm**. This allows us to find the longest repeated patterns in **Linear Time (O(n))**, making it highly efficient for large datasets like DNA sequences.

## 🚀 How to run
1. Ensure you have **Python 3** installed.
2. Run the main script:
   ```bash
   python main.py

## Authors
- Leonardo D.
- Raphaël D.
- Antoine D.
- A.Z.
