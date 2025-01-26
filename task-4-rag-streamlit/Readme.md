# Task 4: Create a Retrieval Augmented Generation (RAG) Application in Streamlit

**Complexity:** Medium

## Overview

This project implements an interactive Retrieval Augmented Generation (RAG) application using Streamlit. Users can upload multiple documents and chat with the application to obtain relevant information based on the uploaded content. The application processes user queries by retrieving relevant passages from the documents and generating responses using a large language model.

## Features

- Upload multiple documents in PDF, DOCX, and TXT formats.
- Parse and preprocess the uploaded documents for effective content retrieval.
- Retrieve relevant passages using a document retrieval mechanism.
- Generate contextually relevant answers using a large language model.
- User-friendly chat interface for querying information from uploaded documents.
- Display responses based on the extracted content through chat interaction.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

**Run the Streamlit Application:**

You can start the application from the command line:

```bash
streamlit run app.py
```

Then, open your web browser and navigate to `http://localhost:8501` to access the application.

**Uploading Documents:**

1. Use the file uploader to select and upload multiple documents.
2. After the documents are processed, ask questions regarding the content in the chat interface.

Example of asking a question:
```text
What are the main points discussed in document X?
```