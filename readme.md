# AD (Airworthiness Directives) Extractor
An AI-powered extractor for Airworthiness Directives (AD) documents issued by aviation authorities (FAA, EASA). The system uses an LLM (LLaMA) running on Ollama with LangChain to read and chunk documents, extracting key information such as AD number, date, affected aircraft models, modifications constraints, and the reason for the AD. The output is structured JSON, enabling easy integration with aviation databases or automated analysis pipelines.

## Prerequisites 
- Ollama is installed on your system

1. Install Ollama from the official website.
2. Pull the required model:
   ```bash
   ollama pull llama3.1:8b

## How to Run the Project 
1. Install the required dependencies
   ```bash
   pip install -r requirements.txt
2. Create a docs folder inside the datasets directory
4. Add the AD documents (dataset) to: datasets/docs
5. Run the main script
   ```bash
   python main.py
6. To test the given ADs, run 
   ```bash
   python test.py

# JSON Output
![Demo](datasets/json/data.json)

# Test Result 
![Demo](assets/result.png)
