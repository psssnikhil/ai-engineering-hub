"""
Project 14: Multimodal Document RAG Engine
==========================================
Domain: Multimodal RAG, ColPali Layout Embeddings & Vision-Language Processing

Features:
  1. Rich Layout Page Element Struct: Defines element types (text, table, chart) with bounding box dimensions.
  2. Cross-Modal Hybrid Retriever: Evaluates text match and chart layout type correlations.
  3. Vision Bounding Box Citation verifier: Evaluates coordinates mentioned in answers against ground-truth box locations.
  4. Grounded Vision LLM response synthesis.
"""

import os
import sys
import json
import re
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from labs.common.gateway import LLMGateway


@dataclass
class DocumentPageElement:
    element_id: str
    page_number: int
    element_type: str  # "text", "table", "chart"
    content_text: str
    bounding_box: List[float]  # [ymin, xmin, ymax, xmax] normalized (0 to 1000)
    image_uri: Optional[str] = None


SAMPLE_MULTIMODAL_DOCUMENTS = [
    DocumentPageElement(
        element_id="elem_001",
        page_number=1,
        element_type="text",
        content_text="Q4 2025 Financial Overview: Total revenue reached $45.2M, reflecting a 28% YoY increase driven by Cloud Enterprise adoption.",
        bounding_box=[100, 100, 250, 900]
    ),
    DocumentPageElement(
        element_id="elem_002",
        page_number=1,
        element_type="table",
        content_text="<table><tr><th>Segment</th><th>Q4 Revenue</th><th>Margin</th></tr><tr><td>Cloud Infra</td><td>$28.4M</td><td>72%</td></tr><tr><td>AI Services</td><td>$16.8M</td><td>64%</td></tr></table>",
        bounding_box=[300, 100, 550, 900]
    ),
    DocumentPageElement(
        element_id="elem_003",
        page_number=2,
        element_type="chart",
        content_text="[Chart Image: Bar chart comparing quarterly net income from Q1 to Q4 2025 showing Q4 peak at $8.1M]",
        bounding_box=[150, 100, 600, 900],
        image_uri="mcp://images/net_income_q4_chart.png"
    )
]


class MultimodalRAGEngine:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.corpus = SAMPLE_MULTIMODAL_DOCUMENTS

    def search_layout_elements(self, query: str, top_k: int = 2) -> List[DocumentPageElement]:
        """Hybrid search matching query against text tokens and target layout elements (chart, table)."""
        query_words = set(query.lower().split())
        scored = []

        for elem in self.corpus:
            # Baseline keyword overlap score
            text_score = sum(1.0 for word in query_words if word in elem.content_text.lower())
            
            # Structural alignment boosts
            if "table" in query.lower() or "revenue" in query.lower():
                if elem.element_type == "table":
                    text_score += 3.0
            if "chart" in query.lower() or "net income" in query.lower() or "graph" in query.lower():
                if elem.element_type == "chart":
                    text_score += 4.0
                    
            scored.append((elem, text_score))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        return [elem for elem, score in scored[:top_k]]

    @staticmethod
    def calculate_box_iou(box_a: List[float], box_b: List[float]) -> float:
        """Calculates Intersection over Union (IoU) of normalized 2D bounding boxes."""
        # Box format: [ymin, xmin, ymax, xmax]
        y_min = max(box_a[0], box_b[0])
        x_min = max(box_a[1], box_b[1])
        y_max = min(box_a[2], box_b[2])
        x_max = min(box_a[3], box_b[3])

        # Compute intersection area
        intersection_w = max(0.0, x_max - x_min)
        intersection_h = max(0.0, y_max - y_min)
        intersection_area = intersection_w * intersection_h

        # Compute union area
        area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
        area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
        union_area = area_a + area_b - intersection_area

        if union_area <= 0:
            return 0.0
        return intersection_area / union_area

    def verify_citations(self, answer: str, retrieved_elements: List[DocumentPageElement]) -> List[Dict[str, Any]]:
        """Parses coordinates in output and cross-checks layout groundedness."""
        # Find citations matching format: [page, ymin, xmin, ymax, xmax] or Box: [ymin, xmin, ymax, xmax]
        box_pattern = r'\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]'
        matches = re.findall(box_pattern, answer)
        
        verifications = []
        for match in matches:
            cited_box = [float(x) for x in match]
            best_iou = 0.0
            best_match_elem = None
            
            for elem in retrieved_elements:
                # Compare cited coordinates directly (ignoring scale differences)
                iou = self.calculate_box_iou(cited_box, elem.bounding_box)
                if iou > best_iou:
                    best_iou = iou
                    best_match_elem = elem
                    
            verifications.append({
                "cited_coordinates": cited_box,
                "matched_element_id": best_match_elem.element_id if best_match_elem else "None",
                "iou_score": round(best_iou, 3),
                "is_grounded": best_iou > 0.40
            })
        return verifications

    def generate_multimodal_answer(self, query: str) -> Dict[str, Any]:
        # Step 1: Retrieve Layout Elements
        retrieved = self.search_layout_elements(query, top_k=2)
        
        # Format elements context including layout boundary details
        context_str = ""
        for elem in retrieved:
            context_str += (
                f"\n---\n"
                f"Element ID: {elem.element_id} (Page: {elem.page_number}, Type: {elem.element_type})\n"
                f"Bounding Box: {elem.bounding_box}\n"
                f"Content: {elem.content_text}\n"
            )

        system_instruction = (
            "You are a multimodal RAG document analyst. Answer the user query using details "
            "from the context. When you reference facts, cite the bounding box coordinate of the source "
            "element exactly as documented, using format: [ymin, xmin, ymax, xmax]. For example, "
            "'based on the table [300, 100, 550, 900], Cloud Infra revenue was...'."
        )

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Query: {query}\n\nContext:\n{context_str}"}
        ]

        try:
            resp = self.gateway.generate(messages=messages, temperature=0.0)
            answer = resp.content
            provider = resp.provider_name
        except Exception:
            # Fallback mock answer containing precise coordinate citation
            answer = (
                "Based on the Page 1 table [300, 100, 550, 900], the Q4 revenue for Cloud Infra "
                "was $28.4M with a margin of 72%. Additionally, net income peaked at $8.1M in the Q4 chart [150, 100, 600, 900]."
            )
            provider = "LocalFallback"

        # Step 2: Bounding Box Citation Verification
        verifications = self.verify_citations(answer, retrieved)
        
        # Calculate grounding precision score (percentage of grounded citations)
        if verifications:
            grounded_count = sum(1 for v in verifications if v["is_grounded"])
            precision = round(grounded_count / len(verifications), 2)
        else:
            precision = 1.0  # No citations to fail

        return {
            "query": query,
            "answer": answer,
            "provider": provider,
            "retrieved_elements": [e.element_id for e in retrieved],
            "citation_verifications": verifications,
            "visual_grounding_precision": precision
        }


def main():
    print("=" * 75)
    print("  Multimodal Document RAG Engine (Project 14)")
    print("=" * 75 + "\n")

    engine = MultimodalRAGEngine()

    query = "List Q4 revenue details for Cloud Infra from the segments table."
    print(f"User Query: '{query}'\n")

    result = engine.generate_multimodal_answer(query)
    
    print("Answer Output:")
    print("-" * 75)
    print(result["answer"])
    print("-" * 75 + "\n")

    print("📐 Visual Bounding Box Grounding Evaluator Results:")
    for v in result["citation_verifications"]:
        print(
            f"  - Cited Box: {v['cited_coordinates']} matched '{v['matched_element_id']}' "
            f"| IoU Score: {v['iou_score']} | Grounded: {v['is_grounded']}"
        )
    print(f"\n🎯 Overall Visual Grounding Precision Score: {result['visual_grounding_precision']}")
    print("=" * 75)


if __name__ == "__main__":
    main()
