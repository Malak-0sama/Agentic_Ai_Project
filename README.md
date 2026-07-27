# AI Business Intelligence Agent

## Overview

AI Business Intelligence Agent is a modular machine learning platform designed to automate the complete analytical workflow for structured business datasets. The system follows a multi-agent architecture in which each agent is responsible for a specific stage of the pipeline, from dataset understanding to model training and validation.

The platform allows users to upload a dataset, automatically analyze its structure, generate an execution strategy using a large language model, preprocess the data, train an appropriate machine learning model, evaluate its performance, and save the trained model for future inference.

---

## Key Features

* Automatic dataset schema analysis
* Intelligent workflow planning using Gemini
* Automated data preprocessing
* Regression and classification support
* Automatic model selection
* Model training and validation
* Model persistence
* REST API built with FastAPI
* Modular and extensible multi-agent architecture

---

## Architecture

```
Client
   │
   ▼
FastAPI
   │
   ▼
Schema Agent
   │
   ▼
LLM Planner Agent
   │
   ▼
Preprocessing Agent
   │
   ▼
Model Agent
   │
   ▼
Evaluation
   │
   ▼
Saved Model
```

---

## Project Structure

```
business-ai-agent/
│
├── agents/
│   ├── schema_agent.py
│   ├── llm_planner_agent.py
│   ├── preprocessing_agent.py
│   └── model_agent.py
│
├── models/
│   ├── trainer.py
│   ├── splitter.py
│   ├── validator.py
│   └── registry.py
│
├── uploads/
├── api.py
├── requirements.txt
└── README.md
```

---

## Components

### Schema Agent

The Schema Agent performs an initial inspection of the uploaded dataset. It extracts structural information including column names, data types, missing values, duplicate records, numerical features, categorical features, memory usage, and potential target columns.

### LLM Planner Agent

The LLM Planner Agent uses the Gemini API to analyze the dataset metadata and generate a machine learning execution plan. The generated plan includes task identification, preprocessing recommendations, algorithm suggestions, and execution reasoning.

### Preprocessing Agent

The Preprocessing Agent applies the preprocessing pipeline required by the selected machine learning task. The workflow includes handling missing values, encoding categorical variables, feature scaling, and dataset preparation before training.

### Model Agent

The Model Agent manages dataset splitting, model selection, training, validation, evaluation, and model serialization. The agent supports both regression and classification workflows.

---

## Supported Machine Learning Tasks

* Regression
* Binary Classification
* Multi-class Classification

---

## Technology Stack

* Python
* FastAPI
* Pandas
* NumPy
* Scikit-learn
* CatBoost
* XGBoost
* LightGBM
* Gemini API
* Joblib

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/Agentic_Ai_Project.git
```

Navigate to the project directory:

```bash
cd Agentic_Ai_Project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the API server:

```bash
uvicorn api:app --reload
```

Default endpoint:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Workflow

```
Dataset Upload
      │
      ▼
Schema Analysis
      │
      ▼
LLM Planning
      │
      ▼
Data Preprocessing
      │
      ▼
Model Training
      │
      ▼
Model Validation
      │
      ▼
Evaluation
      │
      ▼
Model Persistence
```

---

## Future Work

* Hyperparameter optimization
* Explainable AI integration
* Feature engineering automation
* Time series forecasting
* Ensemble model selection
* Automated business insight generation
* Dashboard generation
* Multi-model benchmarking

---

## License

This project is released under the MIT License.
