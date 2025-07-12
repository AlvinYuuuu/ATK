# Implementation Plan: AI Tech Consultant Agent

## 1. Introduction

This document outlines the technical implementation plan for the AI Tech Consultant Agent. It breaks down the development into a series of sprints, each with a specific goal and a set of technical tasks. The plan is designed to iteratively build the system, starting with core infrastructure and progressively adding agent capabilities.

This plan aligns with the project's [Technical Overview](mdc:Technical_Overview.md) and [Backend Structure](mdc:Backend_Structure.md).

## 2. High-Level Goals & Scope

The primary goal is to develop a Minimum Viable Product (MVP) that can:
1.  Ingest a tender document (PDF or DOCX).
2.  Analyze its requirements, constraints, and client needs.
3.  Propose a technical solution based on a core knowledge base of past projects and technologies.
4.  Generate a high-level project plan and a system architecture diagram.
5.  Draft a complete, coherent proposal document.

The scope of this initial implementation focuses on the core multi-agent system and its integration with the specified technology stack (ADK, Mem0, LiteLLM, LangFuse).

## 3. Technical Approach Summary

We will build the system sprint by sprint, focusing on one major capability at a time. Each sprint will involve developing one or two specialist agents and their associated tools, followed by integration into the main `OrchestratorAgent`. Automated testing and continuous integration will be key to ensuring components are robust and working correctly before moving to the next stage.

## 4. Sprint Plan

### Sprint 1: Core Infrastructure & Foundation

*   **Dates:** Week 1
*   **Sprint Goal:** Establish the project's foundational framework. Ensure all core services (ADK, Mem0, LiteLLM, LangFuse) are integrated and communicating, and create a basic, runnable agent skeleton.
*   **Technical Breakdown:**
    *   **Feature: Project Setup & CI**
        *   **Description**: Initialize the project with all dependencies, configuration, and environment variables. Set up a basic CI pipeline for quality assurance.
        *   **Affected Components**: `requirements.txt`, `.env.example`, `src/core/config.py`, `src/main.py`.
        *   **Key Implementation Steps**:
            *   Define and confirm all necessary packages in `requirements.txt`, including `google-generativeai-adk`, `mem0ai`, `litellm`, and `langfuse`.
            *   Create a `.env.example` file to manage all required API keys and configuration settings (e.g., for LLM providers, LangFuse, etc.).
            *   Implement LiteLLM configuration in `src/core/config.py` to create a model-routing instance, allowing for flexible switching between different LLMs.
            *   Implement Mem0 client initialization in `src/core/shared_memory.py`, ensuring a single, reusable client instance is available across the application.
            *   Write a basic "hello world" agent in `src/main.py` that utilizes the ADK runner to confirm the core environment is functional.
    *   **Feature: Basic Orchestrator & Observability**
        *   **Description**: Create a minimal `OrchestratorAgent` and confirm that its execution is correctly instrumented and traced in LangFuse, providing essential observability.
        *   **Affected Components**: `src/agents/orchestrator_agent.py`, `src/core/config.py`.
        *   **Key Implementation Steps**:
            *   Define the `OrchestratorAgent` class using the ADK framework.
            *   Implement a simple `run` method that logs a "start" and "finish" message.
            *   Integrate the LangFuse SDK, ensuring the agent's execution is wrapped in a trace.
            *   Run the agent and verify that a complete trace with input and output appears in the LangFuse dashboard.
    *   **Deliverables**: A runnable project that successfully initializes all clients, demonstrates a basic trace in LangFuse, and is ready for feature development.

### Sprint 2: Tender Ingestion & Analysis

*   **Dates:** Week 2
*   **Sprint Goal:** Implement the first functional step of the proposal workflow: ingesting and analyzing a tender document from multiple formats (PDF, DOCX).
*   **Technical Breakdown:**
    *   **Feature: Multi-format Document Parsing**
        *   **Description**: Create robust tools capable of extracting clean text from both PDF and DOCX documents.
        *   **Affected Components**: `src/tools/document_parsing_tools.py`, `tests/tools/`.
        *   **Key Implementation Steps**:
            *   Implement PDF text extraction using a library like `PyMuPDF` for its accuracy.
            *   Implement DOCX text extraction using the `python-docx` library.
            *   Create a single `@function_tool` named `parse_document` that inspects the file extension and delegates to the appropriate parsing logic.
            *   Write unit tests for the parsing tool with sample PDF and DOCX files to ensure reliability.
    *   **Feature: Tender Analysis Agent**
        *   **Description**: Develop the `TenderAnalysisAgent` to use the parsing tool, understand the document's content, and extract key requirements and context.
        *   **Affected Components**: `src/agents/tender_analysis_agent.py`.
        *   **Key Implementation Steps**:
            *   Define the agent with a detailed prompt instructing it to: "Read the provided text and identify the core problem, explicit functional/non-functional requirements, business goals, technical constraints, and key client details."
            *   Implement agent logic to call the `parse_document` tool with a given file path.
            *   Implement logic to save the structured analysis to Mem0 using a `save_memory` tool. The saved data should be a well-defined JSON object (e.g., `{ "summary": "...", "requirements": [...], "constraints": [...] }`).
    *   **Deliverables**: An `OrchestratorAgent` that can delegate a PDF or DOCX document to the `TenderAnalysisAgent`, which then extracts the text and saves a structured analysis to memory.

### Sprint 3: Solution Strategy & Knowledge Base

*   **Dates:** Week 3
*   **Sprint Goal:** Enable the system to reason about solutions by searching a persistent, long-term knowledge base of organizational expertise.
*   **Technical Breakdown:**
    *   **Feature: Knowledge Base Creation & Population**
        *   **Description**: Define a schema and create a script to populate the long-term knowledge base in Mem0 with data on past projects, technologies, and partners.
        *   **Affected Components**: `scripts/populate_kb.py` (new), `data/kb_data.json` (new).
        *   **Key Implementation Steps**:
            *   Define a clear JSON schema for knowledge entries (e.g., distinguishing between `case_study`, `technology_profile`, `partner_info`).
            *   Create an idempotent script that reads from a structured data source (like a JSON file or CSV) and populates Mem0, avoiding duplicate entries.
            *   Populate the data source with initial information about Votee's capabilities.
    *   **Feature: Solution Strategy Agent**
        *   **Description**: Develop the `SolutionStrategyAgent` to use the knowledge base and the tender analysis to formulate a high-level technical solution.
        *   **Affected Components**: `src/agents/solution_strategy_agent.py`, `src/tools/memory_tools.py`.
        *   **Key Implementation Steps**:
            *   Implement a `search_kb` tool that provides a structured interface to search Mem0, allowing for queries and filters.
            *   Define the agent with a multi-step prompt that instructs it to:
                1.  Read the tender analysis from shared memory.
                2.  Search the knowledge base for relevant case studies and technologies.
                3.  Formulate a technical solution, including a recommended tech stack and high-level architecture. Justify choices by referencing the KB.
                4.  Save the structured solution (e.g., `{ "tech_stack": [...], "architecture_overview": "...", "justification": "..." }`) to shared memory.
    *   **Deliverables**: The `SolutionStrategyAgent` can successfully generate and justify a relevant technical solution based on a tender analysis and the populated knowledge base.

### Sprint 4: Planning & Visualization

*   **Dates:** Week 4
*   **Sprint Goal:** Add project planning and automated diagram generation capabilities to translate the solution into concrete deliverables.
*   **Technical Breakdown:**
    *   **Feature: Visualization Agent & Tools**
        *   **Description**: Create an agent that can generate system architecture diagrams in Mermaid syntax based on the proposed solution.
        *   **Affected Components**: `src/agents/visualization_agent.py`, `src/tools/diagram_tools.py`.
        *   **Key Implementation Steps**:
            *   Create a `create_architecture_diagram` tool that takes a structured description of components and their connections (e.g., list of nodes and edges) and generates a valid Mermaid diagram string.
            *   Develop the `VisualizationAgent` with a prompt that directs it to synthesize the solution from memory into a component structure and then use the tool to generate the diagram.
    *   **Feature: Project Planner Agent & Tools**
        *   **Description**: Create an agent that can generate a high-level project plan and timeline from the solution.
        *   **Affected Components**: `src/agents/project_planner_agent.py`, `src/tools/planning_tools.py`.
        *   **Key Implementation Steps**:
            *   Create a `generate_project_plan` tool that outputs a markdown-formatted plan with phases (e.g., Discovery, Development, Deployment) and key milestones.
            *   Develop the `ProjectPlannerAgent` with a prompt that instructs it to break down the solution into logical work packages and map them onto a timeline.
    *   **Deliverables**: The system can auto-generate a markdown project plan and a Mermaid architecture diagram based on the proposed solution.

### Sprint 5: Proposal Generation & End-to-End MVP

*   **Dates:** Week 5
*   **Sprint Goal:** Integrate all components to achieve a full end-to-end proposal generation flow and produce the final document.
*   **Technical Breakdown:**
    *   **Feature: Technical Writer Agent**
        *   **Description**: Develop the final agent in the chain, responsible for assembling all generated artifacts into a single, polished, and professional proposal document.
        *   **Affected Components**: `src/agents/technical_writer_agent.py`.
        *   **Key Implementation Steps**:
            *   Define the agent with a detailed prompt and a template instructing it to synthesize all data from shared memory (analysis, solution, plan, diagram) into a coherent document.
            *   The prompt should enforce a professional tone and structure, including sections for Introduction, Problem Understanding, Proposed Solution, Architecture, Project Plan, and an "About Us" section derived from the KB.
    *   **Feature: Full E2E Integration**
        *   **Description**: Enhance the `OrchestratorAgent` to manage the full, sequential execution of all specialist agents from document ingestion to final output.
        *   **Affected Components**: `src/agents/orchestrator_agent.py`.
        *   **Key Implementation Steps**:
            *   Implement state-machine logic within the `OrchestratorAgent` to call each specialist agent in the correct order (`TenderAnalysis` -> `SolutionStrategy` -> `Visualization` & `ProjectPlanner` -> `TechnicalWriter`).
            *   Ensure seamless data flow between agents via the shared Mem0 instance.
            *   Implement the final step of writing the completed proposal to a markdown file and notifying the user of its location.
    *   **Deliverables**: A fully functional MVP that can take a tender document (PDF or DOCX) and produce a complete technical proposal with a plan and diagrams, saved as a markdown file.