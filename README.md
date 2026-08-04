# AI Engineer Course Journey 🚀

This repository contains my learning journey while exploring **Large Language Models (LLMs), Generative AI, Prompt Engineering, and AI Application Development**.

The goal of this repository is to document my concepts, experiments, implementations, and projects while building a strong foundation in AI Engineering.

---

# Learning Progress

## Day 1 — Environment Setup

Completed the initial development environment setup:

* Python environment configuration
* Virtual environment creation
* Required library installation
* API configuration setup

---

# Day 2 — First LLM Call & Understanding LLM Responses

Learned how to interact with Large Language Models through APIs.

## Concepts Covered

### Virtual Environment

* Understanding why virtual environments are used.
* Keeping project dependencies isolated.
* Managing different Python packages for different projects.

### API Keys

* Understanding API authentication.
* Connecting applications with LLM providers securely.
* Managing API keys using environment variables.

### Choosing an LLM Model

Learned how to select models based on:

* Capability
* Response quality
* Speed
* Cost
* Context window size

### First LLM API Call

Explored:

* Sending user prompts to an LLM.
* Understanding request and response structure.
* Analyzing generated responses.
* Understanding how applications communicate with AI models.

---

# Day 3 — System Role, Temperature & Tokens

Learned about controlling and understanding LLM behavior.

## Roles in LLM Conversations

Understanding the three major message roles:

### System Role

Defines the behavior, rules, and personality of the AI.

Example:

* Setting the assistant as a coding expert.
* Providing instructions before user interaction.

### User Role

Contains the user's input, questions, or instructions.

### Assistant Role

Contains the AI-generated responses.

---

## Temperature

Learned how temperature controls randomness in LLM outputs.

* Lower temperature → More deterministic and consistent responses.
* Higher temperature → More creative and diverse responses.

Understanding when to use different temperature values based on the task.

---

## Tokens

Learned how LLMs process text using tokens.

The process:

```
Human Text
     ↓
Tokenization
     ↓
Numbers/Tokens
     ↓
LLM Processing
     ↓
Generated Tokens
     ↓
Converted Back Into Human Language
```

Covered:

* What tokens represent.
* How input and output tokens work.
* Why token limits matter.

---

# Day 5 — Pydantic & JSON Structured Output

Learned how to create structured and reliable AI outputs.

## JSON

Covered:

* JSON data format.
* How information is stored using key-value pairs.
* Using JSON for communication between applications.

## Pydantic

Learned about:

* Pydantic BaseModel.
* Defining expected data structures.
* Data validation.
* Creating structured outputs from LLM responses.

Used Pydantic to control how AI-generated responses should be formatted.

---

# Day 6 — Mini Project: AI Resume Analyzer 📄

Built a mini project using LLM capabilities.

## Project Overview

An AI-powered resume analyzer that compares:

* Candidate Resume (PDF)
* Job Description (PDF)

and provides analysis based on the requirements.

## Concepts Used

* PDF file handling
* Reading and extracting information from documents
* Sending extracted data to an LLM
* Resume analysis
* Matching skills with job requirements
* Generating scores and feedback

---

# Day 7 — Prompt Engineering

Learned how to design effective prompts for better AI responses.

## Six Main Components of a Good Prompt

1. Role
2. Task
3. Context
4. Instructions
5. Output Format
6. Constraints/Fallback Instructions

Also learned:

* Zero-shot prompting
* One-shot prompting
* Few-shot prompting

Understanding how prompt structure affects model performance.

---

# Day 8 — ReAct Framework (Reasoning + Action)

Learned about the ReAct approach.

## What is ReAct?

ReAct combines:

* Reasoning
* Action

It allows AI systems to think through problems and use external tools when required.

Learned:

* Why ReAct is needed.
* How AI agents work in a loop.
* Interaction between reasoning and tool execution.

Basic flow:

```
Thought → Action → Observation → Repeat
```

---

# Day 9 — Prompt Chaining & AI Workflow Design

Learned how complex AI tasks can be divided into smaller steps.

## Concepts Covered

* Breaking large problems into smaller prompts.
* Connecting multiple LLM calls together.
* Debugging AI workflows.
* Retry mechanisms.
* Improving reliability using multiple steps.

Understanding how production-level AI systems are designed.

---

# Day 10 — Streaming Responses

Learned how applications provide real-time AI responses like ChatGPT.

## What is Streaming?

Instead of waiting for the complete response, the model sends generated tokens continuously.

Example:

```
Token 1 → Token 2 → Token 3 → Token 4
```

## Learned:

* How streaming works.
* Why streaming improves user experience.
* When to use streaming.
* Implementing real-time response generation.

---

# 🛠️ Technologies Used

* Python
* LLM APIs
* JSON
* Pydantic
* Prompt Engineering
* Virtual Environments
* File Handling
* Generative AI Concepts

---

# Goal

My goal is to become an AI Engineer by building strong fundamentals in:

* Large Language Models
* AI Agents
* Generative AI Applications
* Machine Learning
* Real-world AI Projects

This repository represents my continuous learning journey in AI Engineering.
