
# Custom AI Chatbot with Microservices & Deep Learning Integration

Instead of relying only on LLM knowledge, the chatbot intelligently calls external tools (like a plant disease model) to provide accurate, real-world responses.
## Key Highlights:

-   Integrated Groq LLM for ultra-fast responses
-   Custom prompt engineering + intent extraction pipeline
-   Microservice-based architecture (scalable & modular)
-   Dockerized services for seamless deployment
-   MCP integration for tool orchestration + customized orchestration
-   Deep Learning model for Plant Disease Detection as a tool
-   Built using Python & FastAPI
-   Robust data cleaning and preprocessing pipeline
## Parts of the Project

**User Interface Service**
-   Customizable chat interface supporting text and image input
-   Allows users to upload plant images for disease detection

**Orchestrator Service**
-   Central decision-making component
-   Routes user queries to appropriate services or tools based on intent

**Extractor & Cleaning Service**
-   Handles query preprocessing and normalization
-   Extracts key information such as user intent from the input

**Tool Service**
-   Hosts a collection of custom tools
-   Currently includes a Plant Disease Detection model built using a Deep Learning (CNN) approach

**LLM Service**
-   Generates responses using a Groq-based LLM
-   Designed to be extensible for integration with other LLM providers

**Model Building Module**
-   Separate from the microservice architecture
## Prerequisites

-   **Docker**
-   **Docker Compose**
-   **Python 3.13**
-   **Groq API Keys**
## Installation

Install customized-chatbot with docker

-   **Extract** the project folder after cloning it.
-   **Navigate** to the project directory.
```bash
  cd customized-chatbot
  
```
-   **Put Groq API Key** in .env file currently it has dummy api key

-   **Build and run**
```bash
  docker compose up --build
```
## Installation

Install customized-chatbot with docker

-   **Extract** the project folder after cloning it.
-   **Navigate** to the project directory.
```bash
  cd customized-chatbot
  
```
-   **Put Groq API Key** in .env file currently it has dummy api key

-   **Build and initiate all services**
```bash
  docker compose up --build
```
- **Run locally** by using this local url http://localhost:8000