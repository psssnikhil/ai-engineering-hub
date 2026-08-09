# Project 09: Healthcare Medical Guardrails Agent

A clinical decision support agent featuring multi-layer safety guardrails: emergency triage classifier, medical disclaimer enforcement, PII/HIPAA redactor, and grounded medical RAG.

```mermaid
flowchart TD
    PatientInput["Patient / Clinician Query"] --> Guardrails["Input Guardrails Gate"]
    Guardrails --> Emergency{"Emergency Triage?"}
    Emergency -- Yes --> Escalate["911 Emergency Protocol Alert"]
    Emergency -- No --> Redactor["PII/HIPAA Redactor"]
    Redactor --> MedicalRAG["Medical RAG + Disclaimer Generator"]
    MedicalRAG --> SafeResponse["Grounded Clinical Response"]
```

## Quick Example Code

```python
from main import HealthcareAgent

agent = HealthcareAgent()
response = agent.handle_query("Patient shows signs of severe chest pain and dizziness.")
print(response)
```

## Quickstart

```bash
python main.py
```
