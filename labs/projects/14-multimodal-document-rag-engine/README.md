# Project 14: Multimodal Document RAG Engine

**Domain:** Multimodal RAG, Layout Analysis & Vision LLMs  
**Course Mapping:** Course 06 (RAG) & Course 10 (Vector Databases)

---

## 🎯 Overview

An enterprise multimodal document retrieval-augmented generation engine capable of parsing, indexing, and retrieving over complex PDFs containing multi-column text, HTML tables, and chart images with visual bounding box citation grounding.

---

## 🚀 Key Features

1. **Layout-Aware Element Parser**: Separates text, table HTML, and chart image bounding boxes.
2. **Hybrid Cross-Modal Retrieval**: Combines ColPali visual patch embeddings with sparse lexical search.
3. **Visual Grounding Citations**: Returns precise page bounding box coordinates (`[ymin, xmin, ymax, xmax]`) alongside answer outputs.
4. **Vision Evaluation**: Evaluates visual bounding box alignment precision.

---

## 💻 Quickstart

Run the multimodal RAG engine:

```bash
python main.py
```
