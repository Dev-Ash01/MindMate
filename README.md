


# MindMate: An AI Companion for Emotional Wellness 

## 🧠 Project Overview
This project implements a sophisticated sentiment analysis and mental health support system that combines multiple AI technologies to provide personalized assistance. The system uses sentiment analysis to understand user emotions and provides context-aware responses through a conversational interface. 

---

## 🔑 Key Features

- **Sentiment Analysis**: Real-time emotion detection using Hugging Face's transformers.
- **AI-Powered Chat Interface**: Interactive chat system with a psychologist persona.
- **Knowledge Integration**:
  - Wikipedia integration for factual information.
  - Mental health resources from *Medical News Today*.
  - Vector-based knowledge retrieval system.
- **Advanced AI Models**:
  - Groq's LLaMA 3.3 70B model for intelligent responses.
  - FAISS for efficient vector similarity search.
  - Hugging Face embeddings for semantic understanding and anlysis.

---

## 🛠️ Technical Architecture

### Core Components

- **Frontend**: Streamlit-based web interface  
- **Backend Services**:
  - Sentiment Analysis Pipeline
  - Knowledge Retrieval System
  - AI Chat Agent
- **Data Processing**:
  - Document loading and splitting
  - Vector embeddings
  - Semantic search capabilities

---

## 📦 Dependencies

This project uses several key Python packages:

- `transformers` (Hugging Face)
- `langchain` and its ecosystem
- `streamlit`
- `faiss`
- Various AI model integrations

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- GROQ API key
- Required Python packages (listed in `requirements.txt`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name


2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** with your GROQ API key:

   ```
   GROQ_API_KEY=your_api_key_here
   ```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open your browser to access the app.

---

## 🚧 Project Phases

### Phase 1: Foundation Setup

* Project initialization
* Basic dependency setup
* Environment configuration

### Phase 2: Core Implementation

* Sentiment analysis integration
* Streamlit interface development
* Basic chat functionality

### Phase 3: Advanced Features

* Knowledge base integration
* Vector database implementation
* AI agent development

### Phase 4: Integration and Testing

* Component integration
* System testing
* Performance optimization

---

## 🧭 Usage Guide

### Sentiment Analysis

* Enter your feelings in the sidebar text input.
* The system will analyze and display the sentiment.

### Chat Interface

* Type your message in the chat input.
* The AI psychologist will respond based on:

  * Your current sentiment
  * Available knowledge base
  * Contextual understanding

---

## 🚀 Future Enhancements

* Enhanced knowledge base integration
* Multi-language support
* Advanced analytics dashboard
* Integration with additional mental health resources

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

* [Hugging Face](https://huggingface.co) for the sentiment analysis model
* [Groq](https://groq.com) for the LLaMA model access
* [Medical News Today](https://www.medicalnewstoday.com) for mental health resources
* [Wikipedia](https://www.wikipedia.org) for factual information


