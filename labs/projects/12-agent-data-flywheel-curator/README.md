# Project 12: Agent Data Flywheel & Trajectory Curator

**Domain:** AI Infrastructure, Trajectory Curation & Alignment Flywheels  
**Course Mapping:** Course 13 (LLM Evaluation) & Course 15 (Fine-Tuning & Alignment)

---

## 🎯 Overview

An automated trajectory curation and synthetic dataset flywheel for agentic AI platforms. Raw agent logs are captured, scored via deterministic sandbox verifiers and LLM-as-a-judge reward models, filtered via rejection sampling, and formatted into **DPO (Direct Preference Optimization)** JSONL dataset pairs for fine-tuning candidate models.

---

## 🚀 Key Features

1. **Trajectory Ingestion**: Parses multi-step reasoning steps, tool call parameters, observations, and error flags.
2. **Hybrid Reward Evaluator**: Combines hard sandbox checks (tool error detection, token budget caps) with LLM-as-a-judge quality scoring.
3. **Rejection Sampling Filter**: Filters out low-margin preference pairs (requiring $\Delta \text{score} \ge 0.20$).
4. **DPO JSONL Exporter**: Generates Hugging Face TRL-compatible preference pair datasets.

---

## 💻 Quickstart

Run the flywheel pipeline:

```bash
python main.py
```

---

## 📊 Output Schema

```json
{
  "trajectory_id": "traj-001",
  "prompt": "Calculate final invoice...",
  "chosen": [...],
  "rejected": [...],
  "reward_score_chosen": 0.965,
  "reward_score_rejected": 0.520,
  "margin": 0.445
}
```
