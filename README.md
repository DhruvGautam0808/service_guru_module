# AM Service AI - Retrieval & Routing Module

## Overview
This module is a scalable, local testing and orchestration environment for the Service Guru AI Assistant. It is designed to optimize token consumption and improve document ranking accuracy for John Deere dealer technicians diagnosing and repairing equipment.

By enforcing strict intent routing, query expansion, and OpenSearch block thresholds, this module directly addresses the challenge of consuming 3 billion tokens per day while paving the way for a 50% reduction in response time.

## Core Features
1. **Sanity Agent (`sanity_agent.py`):** Acts as a gatekeeper using GPT-4o-Mini to classify user intent (DEERE, NON_DEERE, HYBRID). Rejects unrelated queries immediately to save downstream token costs.
2. **Query Expander (`expander.py`):** Uses AI to expand short user queries into detailed technical queries, drastically improving vector database match scores.
3. **Optimized Retriever (`retriever.py`):** Connects securely to AWS OpenSearch. Strictly limits results to a maximum of 10 blocks with a relevancy score greater than 0.5.
4. **Evaluator (`evaluator.py`):** A built-in testing suite to measure latency and track average relevancy scores, helping prevent model drift.
5. **Orchestrator (`main.py`):** The master script that wires the pipeline together end-to-end.

## Prerequisites
* Python 3.x
* AWS OpenSearch Domain (for production use)
* OpenAI API Key

## Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR-USERNAME/service_guru_module.git](https://github.com/YOUR-USERNAME/service_guru_module.git)
cd service_guru_module