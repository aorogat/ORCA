# ORCA

**Automated Specification and Visualization of Multi-Agent Systems**

![Orca Slogan](orca_slogan.png)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ORCA converts natural-language requirements into structured multi-agent system specifications. The system supports specification of agent roles, communication topologies, tools, constraints, and execution parameters. It is intended for design exploration, analysis, and prototyping of multi-agent architectures.

The system focuses on design-time automation: specification generation, requirement elicitation, and visualization. It does not provide execution, training, or deployment capabilities.

![ORCA Demo](https://raw.githubusercontent.com/aorogat/multi-agent-automation/main/images/Automation.gif)

*Interactive design and visualization interface (demonstration).*

---

## System Capabilities

- **Natural-language requirement elicitation** - Iterative refinement of multi-agent system requirements through structured dialogue
- **Real-time graph visualization** - Dynamic rendering of agent relationships and communication topologies
- **Structured specification generation** - Automatic generation of specifications including agents, tools, topology, and constraints
- **Framework-agnostic specification** - Output compatible with multiple MAS frameworks (LangGraph, CrewAI, Concordia)
- **Interactive refinement** - Incremental specification updates through clarification and constraint discovery

---

## Local Execution

### Prerequisites

- Python 3.10 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/orca.git
   cd orca
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the system**
   ```bash
   python run.py
   ```

   This starts both services:
   - **Backend API**: http://localhost:8000
   - **Frontend UI**: http://localhost:8080

### Running Services Separately

**Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Frontend:**
```bash
python webui/app.py
```

---

## Design Workflow

1. Open http://localhost:8080
2. Provide initial requirements for the multi-agent system:
   - *"Build a customer service system with a manager and three specialist agents"*
   - *"Create a simulation of a school with 200 students and 10 teachers"*
   - *"Design an anomaly detection system with monitoring and analysis agents"*
3. The system performs requirements elicitation:
   - Identifies missing or ambiguous requirements
   - Requests clarification through structured questions
   - Updates the MAS specification incrementally
   - Renders the agent architecture visualization
   - Generates a specification summary

---

## Architecture

The system consists of a backend specification engine and a frontend interaction interface. The backend processes natural-language input, maintains the current specification state, and generates graph visualizations. The frontend provides the interaction interface and displays the specification and visualization.

```
orca/
├── backend/
│   ├── main.py                      # FastAPI application entry point
│   ├── engine/
│   │   ├── mas_engine.py            # Core MAS automation engine
│   │   └── requirements_agent/
│   │       ├── agent.py             # LLM-powered requirements extractor
│   │       └── prompts/             # Prompt templates
│   └── models/                      # Data models and schemas
├── webui/
│   └── app.py                       # NiceGUI frontend application
├── run.py                           # Combined launcher script
├── requirements.txt                 # Python dependencies
├── .env                             # Environment configuration
└── README.md                        # This file
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | REST API for chat handling and MAS engine execution |
| **Frontend** | NiceGUI | Interactive conversational interface and visualization |
| **Visualization** | Cytoscape.js | Dynamic graph rendering of agent architectures |
| **Language Model** | OpenAI GPT-4 | Natural language understanding and specification generation |
| **Runtime** | Python 3.10+ | Core application runtime |

---

## API Reference

### POST `/chat`

Processes user messages and returns updated system state.

**Request Body:**
```json
{
  "message": "string",
  "history": [
    {"role": "user", "content": "string"},
    {"role": "assistant", "content": "string"}
  ]
}
```

**Response:**
```json
{
  "reply": "Assistant response message",
  "graph": [
    {"data": {"id": "agent1", "label": "Manager"}},
    {"data": {"source": "agent1", "target": "agent2"}}
  ],
  "spec": {
    "task": "string",
    "goal": "string",
    "agents": ["string"],
    "tools": ["string"],
    "communication": "string",
    "topology": "string",
    "constraints": {}
  },
  "spec_text": "Natural language design summary"
}
```

---

## Roadmap

- [x] Conversational MAS design interface
- [x] Real-time architecture visualization
- [x] Multi-framework specification generation
- [ ] Code generation - Export runnable Python projects
- [ ] Template library - Pre-built MAS patterns
- [ ] Simulation runner - Execute and test generated systems
- [ ] Multi-LLM support - Support for Claude, Gemini, and open-source models
- [ ] Collaborative design - Multi-user system design sessions

---

## Contributing

Contributions are welcome. Please submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [NiceGUI](https://nicegui.io/)
- Visualization by [Cytoscape.js](https://js.cytoscape.org/)
- Language model capabilities by [OpenAI](https://openai.com/)

---

## Contact

Project Link: [https://github.com/yourusername/orca](https://github.com/yourusername/orca)
