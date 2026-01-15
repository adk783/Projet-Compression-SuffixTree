# LZ77 Compression using Suffix Trees

## Description
This project implements a lossless text compression tool based on the **Lempel-Ziv 77 (LZ77) algorithm**.

Instead of a slow linear search, we use a **Suffix Tree** (constructed via **Ukkonen's Algorithm**) to efficiently find the longest repeated patterns in the text in linear time $O(n)$.

## Features
- **Efficient Construction:** Uses Ukkonen's algorithm for linear-time tree building.
- **Fast Compression:** Quickly identifies the longest previous match (Longest Common Substring).
- **Automated Testing:** Generates test files (DNA, Natural Language, Repetitive Patterns) to benchmark performance.

## How to run
1. Ensure you have **Python 3** installed.
2. Clone the repository and navigate to the folder.
3. Run the main script:
   ```bash
   python main.py

## Authors
- Leonardo DIB
- Raphaël DUCOURNAU
- Antoine DUPUY
- Adam ZEH
