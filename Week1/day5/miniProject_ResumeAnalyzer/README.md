# AI Resume Analyzer 📄🤖

## Overview

AI Resume Analyzer is an LLM-powered application that analyzes a candidate's resume against a given job description.

The project extracts information from PDF documents and uses a Large Language Model to evaluate how well the resume matches the job requirements.

The goal of this project is to explore practical applications of Generative AI, prompt engineering, and LLM-based analysis.

---

## Features

* Extract text from PDF resumes
* Extract information from job descriptions
* Analyze resume-job description compatibility
* Generate ATS-style match score
* Identify matching skills
* Identify missing requirements
* Highlight strengths and gaps

---

## How It Works

The workflow of the application:

```
Resume PDF
     |
     ↓
PDF Text Extraction
     |
     ↓
LLM Resume Analysis


Job Description PDF
     |
     ↓
PDF Text Extraction
     |
     ↓
LLM Job Requirement Extraction


Resume Data + Job Data
     |
     ↓
ATS Analysis
     |
     ↓
Final Report
```

---

## Demo

Example terminal output:

![Terminal Output](images/demo.png)

---

## Technologies Used

* Python
* Groq LLM API
* Llama 3.3 70B Model
* Pypdf
* Prompt Engineering
* Environment Variables
* Large Language Models (LLMs)

---

## Concepts Learned

Through this project, I practiced:

* Calling LLM APIs
* Writing effective system prompts
* PDF file handling
* Resume and job description analysis
* Prompt-based information extraction
* Building an AI workflow

---

## Project Structure

```
AI_Resume_Analyzer/
│
├── main.py
├── requirements.txt
├── resume.pdf
├── job_description.pdf
│
├── images/
│   └── demo.png
│
└── README.md
```

---

## How to Run

### 1. Clone the repository

```bash
git clone <repository-link>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API Key

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

### 4. Run the application

```bash
python main.py
```

---

## Future Improvements

* Add a web interface using Streamlit
* Add structured JSON output using Pydantic
* Store previous analysis reports
* Improve scoring algorithm
* Add support for multiple resume formats

---

## Author

Paras Bansal
