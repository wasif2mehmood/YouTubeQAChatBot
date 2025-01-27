# YouTubeQAChatBot

A YouTube Retrieval-Augmented Generation (RAG) system built with LangGraph, LangChain, FastAPI, and Streamlit for semantic search and contextual query responses.

## Overview

This application allows users to interact with a chatbot that can retrieve and generate responses based on YouTube video transcripts. The system uses various AI models and tools to provide contextual and relevant answers to user queries. Additionally, it provides the functionality to view a particular part of the video related to the question asked.

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/wasif2mehmood/YouTubeQAChatBot.git
    cd YouTubeQAChatBot
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

#### Backend

1. Navigate to the BackEnd directory:

    ```sh
    cd BackEnd
    ```

2. Run the FastAPI backend server:

    ```sh
    python -m uvicorn app:app --reload
    ```

#### Frontend

1. Open a new terminal and navigate to the FrontEnd directory:

    ```sh
    cd FrontEnd
    ```

2. Run the Streamlit frontend application:

    ```sh
    python -m streamlit run app.py
    ```

## Usage

1. Open your web browser and go to the URL provided by Streamlit to access the frontend interface.
2. Enter your OpenAI API key and the YouTube video URL to load the transcript.
3. Interact with the chatbot by typing your queries in the input field.
4. Use the "Watch in Video" button to view the particular part of the video related to the question asked.
