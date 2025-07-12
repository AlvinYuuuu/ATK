# AI Tech Consultant Agent

An advanced multi-agent system designed to automate the creation of high-quality, technically-sound proposals in response to tenders. Built with Google ADK and Mem0 for intelligent knowledge management and agent coordination.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different aspects of proposal generation
- **Intelligent Document Analysis**: Extract requirements and constraints from tender documents
- **Solution Strategy Design**: Create comprehensive technical solutions
- **Visual Diagram Generation**: Generate Mermaid diagrams for architecture and workflows
- **Project Planning**: Create detailed timelines, cost estimates, and resource allocation
- **Comprehensive Proposals**: Generate professional technical proposals ready for client presentation
- **Shared Memory System**: Persistent knowledge storage using Mem0
- **Observability**: Full tracing and monitoring with LangFuse

## 🏗️ System Architecture

The system consists of 6 specialized agents coordinated by an Orchestrator:

1. **OrchestratorAgent**: Central coordinator managing the workflow
2. **TenderAnalysisAgent**: Analyzes tender documents and extracts requirements
3. **SolutionStrategyAgent**: Designs technical solutions and architecture
4. **VisualizationAgent**: Creates diagrams and visual aids
5. **ProjectPlannerAgent**: Creates project plans, timelines, and cost estimates
6. **TechnicalWriterAgent**: Generates comprehensive technical proposals

## 🛠️ Technology Stack

- **Google ADK**: Agent Development Kit for building intelligent agents
- **Mem0**: Persistent memory system for knowledge storage
- **LiteLLM**: Model routing and LLM management
- **LangFuse**: Observability and tracing
- **Poetry**: Dependency management
- **OpenTelemetry**: Distributed tracing

## 📦 Installation

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Poetry (for Python dependency management)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI_Tech_Consultant_Agent
```

### 2. Start Required Services

The system requires Mem0 and Langfuse services. You can start them using Docker Compose:

```bash
# Start all services
./scripts/start-services.sh start

# Or manually with Docker Compose
docker-compose up -d
```

**Service URLs:**
- Mem0: http://localhost:8080
- Langfuse: http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 3. Install Python Dependencies

```bash
poetry install
```

### 4. Set Up Environment Variables

Create a `.env` file with the following variables:

```env
# Google API Keys
GOOGLE_API_KEY=your-google-api-key-here

# OpenAI API Key (for LiteLLM)
OPENAI_API_KEY=your-openai-api-key-here

# Mem0 Configuration
MEM0_API_KEY=your-mem0-api-key-here
MEM0_ENV=development
MEM0_HOST=http://localhost:8080

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key-here
LANGFUSE_SECRET_KEY=your-langfuse-secret-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# General Settings
ENV=development
DEBUG=true
```

**Note**: See [ENV_SETUP.md](ENV_SETUP.md) for detailed instructions on obtaining API keys and troubleshooting.

### 5. Service Management

Use the provided script to manage services:

```bash
# Start services
./scripts/start-services.sh start

# Check status
./scripts/start-services.sh status

# View logs
./scripts/start-services.sh logs

# Stop services
./scripts/start-services.sh stop

# Restart services
./scripts/start-services.sh restart
```

For detailed Docker Compose documentation, see [docker-compose.md](docker-compose.md).

## 🚀 Quick Start

### Run the Example Workflow

```bash
poetry run python src/main.py --example
```

This will run a complete example workflow with sample tender content.

### Use the System Programmatically

```python
from src.agents.orchestrator_agent import orchestrator_agent

# Run complete workflow
result = orchestrator_agent.run_complete_workflow(
    tender_content="Your tender document content here"
)

# Check workflow status
status = orchestrator_agent.check_workflow_status()

# Generate proposal summary
summary = orchestrator_agent.generate_proposal_summary()
```

## 📋 Usage Guide

### 1. Tender Analysis

The system starts by analyzing the tender document to extract:
- Functional and non-functional requirements
- Technical constraints
- Budget and timeline information
- Missing information that needs clarification

### 2. Solution Strategy

Based on the analysis, the system designs:
- Technical architecture
- Technology stack recommendations
- Implementation approach
- Risk assessment and mitigation strategies

### 3. Visualizations

The system generates various diagrams:
- System architecture diagrams
- Infrastructure deployment diagrams
- Data flow diagrams
- Project workflow diagrams
- Sequence diagrams
- Database entity-relationship diagrams

### 4. Project Planning

Comprehensive project planning including:
- Detailed timeline with phases and milestones
- Cost estimates (labor, infrastructure, third-party services)
- Resource allocation and team structure
- Risk assessment and quality assurance plans

### 5. Final Proposal

The system generates a complete technical proposal with:
- Executive summary
- Requirements analysis
- Proposed solution
- Technical architecture
- Implementation plan
- Project timeline and costs
- Risk assessment
- Quality assurance plan
- Diagrams and visualizations

## 🔧 Configuration

### Model Routing

The system uses LiteLLM for intelligent model routing:

```python
LITELLM_CONFIG = {
    "complex_reasoning": "gpt-4",        # Complex analysis
    "text_generation": "gpt-3.5-turbo",  # General text
    "summarization": "claude-3-haiku",   # Summarization
    "code_generation": "gpt-4"          # Technical content
}
```

### Memory Management

The shared memory system stores:
- Tender analysis results
- Solution strategies
- Visualizations
- Project plans
- Technical proposals

## 📊 Monitoring and Observability

The system includes comprehensive observability:

- **LangFuse Tracing**: Track all agent interactions and LLM calls
- **OpenTelemetry**: Distributed tracing across the system
- **Memory Analytics**: Monitor knowledge storage and retrieval
- **Performance Metrics**: Track workflow completion times and success rates

## 🧪 Testing

Run the test suite:

```bash
poetry run pytest tests/
```

## 📈 Performance

The system is designed for:
- **Scalability**: Handle multiple concurrent proposal generations
- **Reliability**: Robust error handling and recovery
- **Efficiency**: Optimized model routing and memory usage
- **Quality**: Comprehensive validation and quality checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in the `docs/` folder
- Review the example workflows

## 🔮 Roadmap

- [ ] PDF and DOCX document parsing
- [ ] Integration with external knowledge bases
- [ ] Advanced diagram customization
- [ ] Multi-language support
- [ ] Real-time collaboration features
- [ ] Advanced cost optimization
- [ ] Integration with project management tools
