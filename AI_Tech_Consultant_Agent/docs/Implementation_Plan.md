# Implementation Plan: AI Tech Consultant Agent

## 1. Introduction

This document outlines the technical implementation plan for the AI Tech Consultant Agent. It breaks down the development into a series of sprints, each with a specific goal and a set of technical tasks. The plan is designed to iteratively build the system, starting with core infrastructure and progressively adding agent capabilities.

This plan aligns with the project's [Technical Overview](mdc:Technical_Overview.md) and [Backend Structure](mdc:Backend_Structure.md).

## 2. High-Level Goals & Scope

The primary goal is to develop a Minimum Viable Product (MVP) that can:
1.  Ingest a tender document.
2.  Analyze its requirements.
3.  Propose a technical solution based on a core knowledge base.
4.  Generate a basic project plan and architecture diagram.
5.  Draft a complete proposal document.

The scope of this initial implementation focuses on the core multi-agent system and its integration with the specified technology stack (ADK, Mem0, LiteLLM, LangFuse).

## 3. Technical Approach Summary

We will build the system sprint by sprint, focusing on one major capability at a time. Each sprint will involve developing one or two specialist agents and their associated tools, followed by integration into the main `OrchestratorAgent`. Testing will be conducted at each stage to ensure components are working correctly before moving to the next.

## 4. Sprint Plan

### Sprint 1: Core Infrastructure & Foundation

*   **Dates:** Week 1
*   **Sprint Goal:** Establish the project's foundational framework. Ensure all core services (ADK, Mem0, LiteLLM, LangFuse) are integrated and communicating, and create a basic, runnable agent skeleton.
*   **Technical Breakdown:**
    *   **Feature: Project Setup & CI**
        *   **Description**: Initialize the project with all dependencies and basic configuration.
        *   **Affected Components**: `requirements.txt`, `.env.example`, `src/core/config.py`, `src/main.py`.
        *   **Key Implementation Steps**:
            *   Confirm all packages in `requirements.txt` are correct.
            *   Implement LiteLLM configuration in `src/core/config.py` to route LLM calls.
            *   Implement Mem0 client initialization in `src/core/shared_memory.py`.
            *   Write a basic "hello world" agent in `src/main.py` to test the ADK runner.
    *   **Feature: Basic Orchestrator & Observability**
        *   **Description**: Create a minimal `OrchestratorAgent` and confirm that its execution is being traced in LangFuse.
        *   **Affected Components**: `src/agents/orchestrator_agent.py`, `src/core/config.py`.
        *   **Key Implementation Steps**:
            *   Define the `OrchestratorAgent` class in ADK.
            *   Implement a simple `run` method that logs a message.
            *   Run the agent and verify that a trace appears in the LangFuse dashboard.
    *   **Deliverables**: A runnable project that successfully initializes all clients and demonstrates a basic trace in LangFuse.

### Sprint 2: Tender Ingestion & Analysis

*   **Dates:** Week 2
*   **Sprint Goal:** Implement the first functional step of the proposal workflow: ingesting and analyzing a tender document.
*   **Technical Breakdown:**
    *   **Feature: Document Parsing**
        *   **Description**: Create tools capable of extracting text from PDF documents.
        *   **Affected Components**: `src/tools/document_parsing_tools.py`, `tests/tools/`.
        *   **Key Implementation Steps**:
            *   Choose and implement a robust Python library for PDF text extraction (e.g., `PyMuPDF`).
            *   Create a `` named `parse_pdf` that takes a file path and returns extracted text.
            *   Write unit tests for the parsing tool with a sample PDF.
    *   **Feature: Tender Analysis Agent**
        *   **Description**: Develop the `TenderAnalysisAgent` to use the parsing tool and extract key requirements.
        *   **Affected Components**: `src/agents/tender_analysis_agent.py`.
        *   **Key Implementation Steps**:
            *   Define the agent with a prompt instructing it to read a document's text and identify requirements, constraints, and client details.
            *   Implement logic to call the `parse_pdf` tool.
            *   Implement logic to save the analysis to Mem0 using a `save_memory` tool.
    *   **Deliverables**: An `OrchestratorAgent` that can delegate a PDF document to the `TenderAnalysisAgent`, which then extracts the text and saves an analysis to memory.

### Sprint 3: Solution Strategy & Knowledge Base

*   **Dates:** Week 3
*   **Sprint Goal:** Enable the system to reason about solutions by searching a persistent, long-term knowledge base.
*   **Technical Breakdown:**
    *   **Feature: Knowledge Base Creation**
        *   **Description**: Define a schema and process for populating the long-term knowledge base in Mem0.
        *   **Affected Components**: `scripts/populate_kb.py` (new), `data/kb_data.json` (new).
        *   **Key Implementation Steps**:
            *   Create a script to ingest data about Votee's technologies, partners, and past projects into Mem0 under a shared `user_id`.
            *   Define a simple JSON structure for this data.
    *   **Feature: Solution Strategy Agent**
        *   **Description**: Develop the `SolutionStrategyAgent` to use the knowledge base and the tender analysis to propose a solution.
        *   **Affected Components**: `src/agents/solution_strategy_agent.py`, `src/tools/memory_tools.py`.
        *   **Key Implementation Steps**:
            *   Implement a `search_kb` tool that searches Mem0.
            *   Define the agent with a prompt that instructs it to:
                1.  Read the tender analysis from shared memory.
                2.  Search the knowledge base for relevant technologies.
                3.  Formulate a technical solution.
                4.  Save the solution to shared memory.
    *   **Deliverables**: The `SolutionStrategyAgent` can successfully generate a relevant technical solution based on an analysis and a populated knowledge base.

### Sprint 4: Planning & Visualization

*   **Dates:** Week 4
*   **Sprint Goal:** Add project planning and automated diagram generation capabilities.
*   **Technical Breakdown:**
    *   **Feature: Visualization Agent & Tools**
        *   **Description**: Create an agent that can generate Mermaid diagrams.
        *   **Affected Components**: `src/agents/visualization_agent.py`, `src/tools/diagram_tools.py`.
        *   **Key Implementation Steps**:
            *   Create a `create_architecture_diagram` tool that takes a description of components and generates Mermaid syntax.
            *   Develop the `VisualizationAgent` to use this tool based on the solution stored in memory.
    *   **Feature: Project Planner Agent & Tools**
        *   **Description**: Create an agent that can generate a high-level project plan.
        *   **Affected Components**: `src/agents/project_planner_agent.py`, `src/tools/planning_tools.py`.
        *   **Key Implementation Steps**:
            *   Create a `generate_timeline` tool that outputs a markdown-formatted timeline.
            *   Develop the `ProjectPlannerAgent` to use this tool based on the solution.
    *   **Deliverables**: The system can auto-generate a project plan and an architecture diagram based on the proposed solution.

### Sprint 5: Proposal Generation & End-to-End MVP

*   **Dates:** Week 5
*   **Sprint Goal:** Integrate all components to achieve a full end-to-end proposal generation flow and produce the final document.
*   **Technical Breakdown:**
    *   **Feature: Technical Writer Agent**
        *   **Description**: Develop the final agent in the chain, responsible for assembling the complete proposal.
        *   **Affected Components**: `src/agents/technical_writer_agent.py`.
        *   **Key Implementation Steps**:
            *   Define the agent with a detailed prompt instructing it to read all the data from shared memory (analysis, solution, plan, diagrams) and weave it into a coherent proposal document.
    *   **Feature: Full E2E Integration**
        *   **Description**: Enhance the `OrchestratorAgent` to manage the full, sequential execution of all specialist agents.
        *   **Affected Components**: `src/agents/orchestrator_agent.py`.
        *   **Key Implementation Steps**:
            *   Implement the state-machine logic to call each agent in the correct order.
            *   Handle the passing of data between steps.
            *   Implement the final step of presenting the completed proposal document to the user.
    *   **Deliverables**: A fully functional MVP that can take a tender document and produce a complete technical proposal with a plan and diagrams. 