"""
Project 12: Agent Data Flywheel & Trajectory Curator
=====================================================
Domain: AI Infrastructure, Trajectory Curation & Alignment Flywheels

An automated trajectory curation and synthetic dataset flywheel featuring:
1. Agent Trajectory Collector & Step Execution Quality Evaluator
2. Deterministic & LLM-Judge Rejection Sampling Filter
3. Preference Pair Curator (Exporting DPO / ORPO dataset pairs in JSONL format)
4. Telemetry Scorecard & Continuous Data Quality Analytics

Usage:
  python main.py
"""

import os
import sys
import json
import math
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


@dataclass
class TrajectoryStep:
    step_number: int
    thought: str
    action: str
    action_input: Dict[str, Any]
    observation: str
    is_error: bool = False


@dataclass
class AgentTrajectory:
    trajectory_id: str
    prompt: str
    steps: List[TrajectoryStep]
    final_answer: str
    total_tokens: int
    execution_time_ms: float


@dataclass
class CuratedPreferencePair:
    trajectory_id: str
    prompt: str
    chosen_trajectory: List[Dict[str, Any]]
    rejected_trajectory: List[Dict[str, Any]]
    reward_score_chosen: float
    reward_score_rejected: float
    margin: float


RAW_TRAJECTORY_DATA = [
    {
        "trajectory_id": "traj-001",
        "prompt": "Calculate final invoice for Enterprise Customer ACV $120,000 with 15% tier discount and $2,500 support fee.",
        "successful_run": {
            "steps": [
                {
                    "step_number": 1,
                    "thought": "First calculate tier discount: $120,000 * 0.15 = $18,000.",
                    "action": "calculator",
                    "action_input": {"expression": "120000 * 0.15"},
                    "observation": "18000.0",
                    "is_error": False
                },
                {
                    "step_number": 2,
                    "thought": "Discounted subtotal is $120,000 - $18,000 = $102,000. Now add support fee $2,500.",
                    "action": "calculator",
                    "action_input": {"expression": "102000 + 2500"},
                    "observation": "104500.0",
                    "is_error": False
                }
            ],
            "final_answer": "The total final invoice amount is $104,500.",
            "total_tokens": 340,
            "execution_time_ms": 1250.0
        },
        "flawed_run": {
            "steps": [
                {
                    "step_number": 1,
                    "thought": "Apply discount directly without subtotal calculation.",
                    "action": "calculator",
                    "action_input": {"expression": "120000 * 0.85 + 2500"},
                    "observation": "104500.0",
                    "is_error": False
                },
                {
                    "step_number": 2,
                    "thought": "Try invalid tool call format.",
                    "action": "unknown_tool",
                    "action_input": {"query": "verify"},
                    "observation": "Error: Tool unknown_tool not found.",
                    "is_error": True
                }
            ],
            "final_answer": "Final invoice is $104,500.",
            "total_tokens": 620,
            "execution_time_ms": 2800.0
        }
    },
    {
        "trajectory_id": "traj-002",
        "prompt": "Summarize user compliance status and send warning email if non-compliant.",
        "successful_run": {
            "steps": [
                {
                    "step_number": 1,
                    "thought": "Lookup user compliance record in database.",
                    "action": "db_lookup",
                    "action_input": {"user_id": "usr_9921"},
                    "observation": "Status: NON_COMPLIANT, LastAudit: 2026-01-15, MissingDoc: SOC2_Cert",
                    "is_error": False
                },
                {
                    "step_number": 2,
                    "thought": "User is non-compliant due to missing SOC2 certification. Send notice email.",
                    "action": "send_email",
                    "action_input": {
                        "to": "usr_9921@enterprise.com",
                        "subject": "Compliance Notice: Missing SOC2 Certification",
                        "body": "Your account requires an updated SOC2 certificate."
                    },
                    "observation": "Email sent successfully (ID: msg_8831).",
                    "is_error": False
                }
            ],
            "final_answer": "User status is NON_COMPLIANT. A warning email regarding the missing SOC2 cert has been delivered.",
            "total_tokens": 410,
            "execution_time_ms": 1400.0
        },
        "flawed_run": {
            "steps": [
                {
                    "step_number": 1,
                    "thought": "Guess user status without querying database.",
                    "action": "send_email",
                    "action_input": {
                        "to": "usr_9921@enterprise.com",
                        "subject": "Compliance Alert",
                        "body": "You might be non-compliant."
                    },
                    "observation": "Email sent successfully.",
                    "is_error": False
                }
            ],
            "final_answer": "Sent email assuming non-compliance.",
            "total_tokens": 280,
            "execution_time_ms": 950.0
        }
    }
]


class TrajectoryEvaluator:
    """Evaluates agent trajectories using deterministic verifiers and LLM reward heuristics."""
    
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def score_trajectory(self, prompt: str, steps: List[Dict[str, Any]], final_answer: str, execution_time_ms: float) -> float:
        # Deterministic Penalty Checks
        has_tool_error = any(step.get("is_error", False) for step in steps)
        step_count = len(steps)
        
        base_score = 1.0
        
        if has_tool_error:
            base_score -= 0.35
            
        if step_count > 5:
            base_score -= 0.15
            
        # Reward heuristic bonus for proper tool parameter structure
        valid_actions = all(isinstance(step.get("action_input"), dict) for step in steps)
        if valid_actions:
            base_score += 0.05
            
        # LLM Reward Judge evaluation
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a trajectory reward model evaluator. Evaluate how logical, accurate, "
                    "and hallucination-free this agent execution trace is. "
                    "Return ONLY a JSON object with: {\"quality_score\": float (0.0 to 1.0), \"reason\": string}"
                )
            },
            {
                "role": "user",
                "content": f"Prompt: {prompt}\nSteps: {json.dumps(steps)}\nFinal Answer: {final_answer}"
            }
        ]
        
        try:
            res = self.gateway.generate(messages=messages, temperature=0.0)
            parsed = json.loads(res.content)
            llm_score = float(parsed.get("quality_score", 0.8))
        except Exception:
            llm_score = 0.85 if not has_tool_error else 0.40
            
        final_reward = round(min(1.0, max(0.0, 0.4 * base_score + 0.6 * llm_score)), 3)
        return final_reward


class DataFlywheelCurator:
    """Curates trajectories, applies rejection sampling, and exports DPO preference pairs."""
    
    def __init__(self, evaluator: Optional[TrajectoryEvaluator] = None):
        self.evaluator = evaluator or TrajectoryEvaluator()

    def process_flywheel_batch(self, raw_data: List[Dict[str, Any]]) -> List[CuratedPreferencePair]:
        preference_pairs = []
        
        for item in raw_data:
            tid = item["trajectory_id"]
            prompt = item["prompt"]
            
            good = item["successful_run"]
            bad = item["flawed_run"]
            
            score_good = self.evaluator.score_trajectory(
                prompt, good["steps"], good["final_answer"], good["execution_time_ms"]
            )
            score_bad = self.evaluator.score_trajectory(
                prompt, bad["steps"], bad["final_answer"], bad["execution_time_ms"]
            )
            
            # Rejection Sampling Filter: Accept only if margin > 0.20
            margin = round(score_good - score_bad, 3)
            if margin >= 0.20:
                pair = CuratedPreferencePair(
                    trajectory_id=tid,
                    prompt=prompt,
                    chosen_trajectory=good["steps"],
                    rejected_trajectory=bad["steps"],
                    reward_score_chosen=score_good,
                    reward_score_rejected=score_bad,
                    margin=margin
                )
                preference_pairs.append(pair)
                
        return preference_pairs

    def export_dpo_jsonl(self, pairs: List[CuratedPreferencePair]) -> str:
        records = []
        for p in pairs:
            records.append({
                "trajectory_id": p.trajectory_id,
                "prompt": p.prompt,
                "chosen": p.chosen_trajectory,
                "rejected": p.rejected_trajectory,
                "reward_score_chosen": p.reward_score_chosen,
                "reward_score_rejected": p.reward_score_rejected,
                "margin": p.margin
            })
        return json.dumps(records, indent=2)


def main():
    print("=" * 70)
    print("  Project 12: Agent Data Flywheel & Trajectory Curator")
    print("=" * 70 + "\n")

    curator = DataFlywheelCurator()
    print("📥 Ingesting raw multi-step agent execution traces...")
    print(f"   Batch size: {len(RAW_TRAJECTORY_DATA)} raw trajectory comparisons.\n")

    print("⚙️  Running Trajectory Evaluation & Rejection Sampling Filter...")
    curated_pairs = curator.process_flywheel_batch(RAW_TRAJECTORY_DATA)

    print(f"✅ Rejection Sampling complete. Retained {len(curated_pairs)} high-margin DPO preference pairs.\n")

    print("📊 Exported DPO Dataset Payload (JSONL Preview):")
    print("-" * 70)
    jsonl_output = curator.export_dpo_jsonl(curated_pairs)
    print(jsonl_output)
    print("-" * 70)

    print("\n📈 Data Flywheel Performance Summary:")
    print(f"   - Input Trajectories Processed: {len(RAW_TRAJECTORY_DATA) * 2}")
    print(f"   - Curated Preference Pairs Exported: {len(curated_pairs)}")
    print(f"   - Average Preference Margin Delta: {sum(p.margin for p in curated_pairs) / len(curated_pairs):.3f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
