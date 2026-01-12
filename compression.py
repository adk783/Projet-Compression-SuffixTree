"""
COMPRESSION MODULE (Ziv-Lempel)
-------------------------------
This file implements the Ziv-Lempel (LZ77) compression algorithm.
It uses the Suffix Tree from 'suffix_tree.py' to find the Longest Common Prefix (LCP)
and replace repeated patterns with (position, length) references.

Authors: [Dev2]
"""
