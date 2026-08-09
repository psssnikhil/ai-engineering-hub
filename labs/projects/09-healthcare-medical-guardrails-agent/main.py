"""
Project 09: Healthcare Medical Guardrails & Clinical Support Agent
====================================================================
Domain: Healthcare, Medical Knowledge RAG & Multi-Layer Guardrails Gateway

Production-style healthcare clinical assistant featuring:
1. Multi-layer Safety Guardrails Gateway (Medical disclaimer check, PII/HIPAA redactor)
2. Clinical Triage Classifier (Emergency / Escalation / Self-care)
3. Grounded Medical Knowledge retrieval with strict safety checks

Usage:
  python main.py
"""

import re
import os
import sys
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


MEDICAL_KNOWLEDGE_BASE = [
    {"topic": "Type 2 Diabetes", "text": "Type 2 diabetes management includes regular blood glucose monitoring, balanced diet, exercise, and prescribed oral medications such as Metformin under medical supervision."},
    {"topic": "Hypertension", "text": "Hypertension (high blood pressure) management involves low-sodium diet, stress reduction, exercise, and ACE inhibitors or ARBs prescribed by a physician."},
]


class MedicalGuardrailsGateway:
    """Multi-layer Healthcare Safety & Compliance Gateway."""

    @staticmethod
    def inspect_input(user_prompt: str) -> Dict[str, Any]:
        """Layer 1: Input Triage & Emergency Classifier."""
        emergency_keywords = ["chest pain", "shortness of breath", "unconscious", "stroke", "severe bleeding"]
        for kw in emergency_keywords:
            if kw in user_prompt.lower():
                return {
                    "is_emergency": True,
                    "action": "TRIAGE_EMERGENCY_ESCALATION",
                    "response": "🚨 EMERGENCY NOTICE: Your query indicates a potential medical emergency. Please call 911 (or your local emergency services) immediately or go to the nearest emergency room."
                }
        return {"is_emergency": False}

    @staticmethod
    def sanitize_output(model_output: str) -> str:
        """Layer 2: Output Safety Guardrails — Medical Disclaimer Enforcement & PII Redaction."""
        # Redact potential PII (SSN, Phone numbers)
        sanitized = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', model_output)
        sanitized = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[REDACTED_PHONE]', sanitized)

        disclaimer = "\n\n⚠️ Medical Disclaimer: This AI assistant provides general information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified physician."
        if "Medical Disclaimer:" not in sanitized:
            sanitized += disclaimer
        return sanitized


class HealthcareClinicalAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.guardrails = MedicalGuardrailsGateway()

    def process_patient_query(self, query: str) -> Dict[str, Any]:
        # Step 1: Run Input Guardrails
        triage = self.guardrails.inspect_input(query)
        if triage["is_emergency"]:
            return {
                "query": query,
                "status": "EMERGENCY_ESCALATION",
                "response": triage["response"]
            }

        # Step 2: Retrieve Grounded Medical Knowledge
        context = "\n".join(f"[{item['topic']}] {item['text']}" for item in MEDICAL_KNOWLEDGE_BASE)

        messages = [
            {
                "role": "system",
                "content": "You are a professional Clinical AI Assistant. Answer patient queries concisely based ONLY on validated medical knowledge."
            },
            {"role": "user", "content": f"Medical Context:\n{context}\n\nPatient Query: {query}"}
        ]

        resp = self.gateway.generate(messages=messages, temperature=0.0)

        # Step 3: Run Output Safety & Compliance Guardrails
        safe_response = self.guardrails.sanitize_output(resp.content)

        return {
            "query": query,
            "status": "PROCESSED_SAFE",
            "response": safe_response,
            "provider": resp.provider_name
        }


def main():
    print("=" * 60)
    print("  Healthcare Medical Guardrails Agent (Project 09)")
    print("=" * 60 + "\n")

    agent = HealthcareClinicalAgent()

    # Query 1: Routine query
    q1 = "What are standard lifestyle guidelines for managing Type 2 Diabetes?"
    print(f"Patient Query 1: {q1}")
    res1 = agent.process_patient_query(q1)
    print(f"Status: {res1['status']}")
    print(f"Response:\n{res1['response']}\n")

    # Query 2: Emergency query triggering input triage
    q2 = "I am experiencing severe chest pain and shortness of breath."
    print("-" * 60)
    print(f"Patient Query 2: {q2}")
    res2 = agent.process_patient_query(q2)
    print(f"Status: {res2['status']}")
    print(f"Response:\n{res2['response']}")


if __name__ == "__main__":
    main()
