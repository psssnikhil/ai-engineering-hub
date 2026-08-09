"""
Project 12: Agent Data Flywheel & Trajectory Curator
=====================================================
Domain: AI Infrastructure, Trajectory Curation & Alignment Flywheels

Features:
  1. Trajectory Loop Detector: Detects consecutive tool loops or redundant reasoning thoughts.
  2. Multi-Metric Reward Evaluator: Combines program check rules and LLM-as-a-Judge evaluations.
  3. Rejection Sampling Filter: Accepts DPO preference pairs only if margin threshold (chosen - rejected) is met.
  4. Fine-tuning export format: Generates DPO/ORPO JSON structures ready for trl/alignment frameworks.
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
                },
                {
                    "step_number": 3,
                    "thought": "Try invalid tool call format again.",
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
    """Evaluates agent trajectories using programmatic checks and LLM-as-a-Judge reward metrics."""
    
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()

    def check_trajectory_loops(self, steps: List[Dict[str, Any]]) -> bool:
        """Heuristic check: Detects if same tool called consecutively with identical parameters."""
        for i in range(1, len(steps)):
            prev = steps[i-1]
            curr = steps[i]
            if prev.get("action") == curr.get("action") and prev.get("action_input") == curr.get("action_input"):
                return True
        return False

    def score_trajectory(self, prompt: str, steps: List[Dict[str, Any]], final_answer: str) -> float:
        # 1. Programmatic Rule-based Deductions
        base_score = 1.0
        
        # Tool errors deduction
        has_tool_error = any(step.get("is_error", False) for step in steps)
        if has_tool_error:
            base_score -= 0.30
            
        # Loop/Repetition deduction
        if self.check_trajectory_loops(steps):
            base_score -= 0.40
            
        # Excess step limit deduction
        if len(steps) > 5:
            base_score -= 0.15

        # 2. LLM Reward Judge Score
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert trajectory critic. Evaluate this agent trace for efficiency, "
                    "logical flow, and validity of thoughts. "
                    "Score quality from 0.0 (unusable) to 1.0 (perfect reasoning).\n"
                    "Return ONLY JSON: {\"quality_score\": <float>, \"explanation\": \"<string>\"}"
                )
            },
            {
                "role": "user",
                "content": f"User Prompt: {prompt}\n\nSteps:\n{json.dumps(steps, indent=2)}\n\nFinal Answer:\n{final_answer}"
            }
        ]
        
        try:
            res = self.gateway.generate(messages=messages, temperature=0.0)
            # Simple JSON cleaner
            import re
            cleaned = res.content.strip()
            if cleaned.startswith("```"):
                match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
                if match:
                    cleaned = match.group(1)
            parsed = json.loads(cleaned)
            llm_score = float(parsed.get("quality_score", 0.8))
        except Exception:
            # Fallback rating
            llm_score = 0.85 if not has_tool_error else 0.40
            
        # Combined score weighting
        final_reward = round(min(1.0, max(0.0, 0.4 * base_score + 0.6 * llm_score)), 3)
        return final_reward


class DataFlywheelCurator:
    """Curates trajectories, applies rejection sampling, and exports DPO alignment pairs."""
    
    def __init__(self, evaluator: Optional[TrajectoryEvaluator] = None, min_margin: float = 0.20):
        self.evaluator = evaluator or TrajectoryEvaluator()
        self.min_margin = min_margin

    def process_flywheel_batch(self, raw_data: List[Dict[str, Any]]) -> List[CuratedPreferencePair]:
        preference_pairs = []
        
        for item in raw_data:
            tid = item["trajectory_id"]
            prompt = item["prompt"]
            
            good = item["successful_run"]
            bad = item["flawed_run"]
            
            score_good = self.evaluator.score_trajectory(prompt, good["steps"], good["final_answer"])
            score_bad = self.evaluator.score_trajectory(prompt, bad["steps"], bad["final_answer"])
            
            # Rejection Sampling Filter: Accept only if margin exceeds threshold
            margin = round(score_good - score_bad, 3)
            
            # Accept if margin criteria and absolute score criteria are met
            if margin >= self.min_margin and score_good >= 0.70:
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
            else:
                print(f"  [Rejection Sampling] Trajectory '{tid}' filtered out. Margin: {margin} (Min required: {self.min_margin})")
                
        return preference_pairs

    def export_dpo_payload(self, pairs: List[CuratedPreferencePair]) -> str:
        """Formulate DPO-style alignment dataset compatible with standard trainers."""
        records = []
        for p in pairs:
            # Formulate chat prompts structure
            records.append({
                "prompt": p.prompt,
                "chosen": self._convert_steps_to_chat(p.chosen_trajectory),
                "rejected": self._convert_steps_to_chat(p.rejected_trajectory),
                "metadata": {
                    "trajectory_id": p.trajectory_id,
                    "reward_score_chosen": p.reward_score_chosen,
                    "reward_score_rejected": p.reward_score_rejected,
                    "margin": p.margin
                }
            })
        return json.dumps(records, indent=2)

    def _convert_steps_to_chat(self, steps: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        chat_format = []
        for s in steps:
            # Convert thought/actions to assistant blocks and observations to tool responses
            chat_format.append({
                "role": "assistant",
                "content": f"Thought: {s.get('thought')}\nAction: {s.get('action')}({json.dumps(s.get('action_input'))})"
            })
            chat_format.append({
                "role": "tool",
                "content": f"Observation: {s.get('observation')}"
            })
        return chat_format


def main():
    print("=" * 75)
    print("  Agent Data Flywheel & Trajectory Curator (Project 12)")
    print("=" * 75 + "\n")

    curator = DataFlywheelCurator(min_margin=0.20)
    
    print("📥 Ingesting multi-step agent logs...")
    print(f"   Batch size: {len(RAW_TRAJECTORY_DATA)} trajectory pairs.\n")

    print("⚙️  Running Trajectory Evaluation & Loop Detection...")
    curated_pairs = curator.process_flywheel_batch(RAW_TRAJECTORY_DATA)

    print(f"\n✅ Curation complete. Retained {len(curated_pairs)} DPO alignment pairs.")

    print("\n📊 Formatted DPO Dataset Payload Preview:")
    print("-" * 75)
    payload_str = curator.export_dpo_payload(curated_pairs)
    print(payload_str)
    print("-" * 75)


if __name__ == "__main__":
    main()
