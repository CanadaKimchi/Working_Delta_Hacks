# Notation - Delta Hacks Project

Welcome to Notation, a project developed for Delta Hacks! This innovative device leverages Flask for the backend framework, HTML for the frontend, and seamlessly integrates AWS Textract and OpenAI APIs to provide users with summarized notes based on their writing style.

## Overview

Notation simplifies the process of summarizing slide notes by analyzing the user's writing style and extracting key information from PDF documents. The combination of AWS Textract and OpenAI enables the device to efficiently process and generate concise summaries.

## Technologies Used

- **Flask**: The backend framework powering the Notation device.
- **HTML**: Frontend design for a user-friendly interface.
- **AWS Textract API**: Used to extract text from PDF documents, enhancing the accuracy of the summarization process.
- **OpenAI API**: Employed for the summarization of slide notes based on the user's writing style.

## Features

1. **PDF Text Extraction**: Utilizes AWS Textract to extract text from uploaded PDF documents.

2. **User Writing Style Analysis**: Captures the user's writing style from provided notes.

3. **Summarization with OpenAI**: Applies OpenAI API to generate concise summaries based on the extracted text.

4. **Interactive User Interface**: The frontend design provides an intuitive and interactive experience for users.

## Getting Started

To run Notation locally:

1. Clone the repository.
   ```bash
   https://github.com/CanadaKimchi/Working_Delta_Hacks
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app with
   ```bash
   python run app.py
   ```
   
