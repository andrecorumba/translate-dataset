# README

This document provides an overview and explanation of two Python scripts, `azure_openai_translate.py` and `openai_translate.py`, along with information about Python files, libraries, and the `.env` file used in these scripts.

## `azure_openai_translate.py`

### Python File
- **File Name:** `azure_openai_translate.py`
- **Purpose:** This Python script is designed to translate text from a dataset to English using the Azure OpenAI API. It also handles error logging and response aggregation.

### Libraries Used
- **`os`**: This library provides a way to use operating system-dependent functionality, such as reading environment variables and file operations.

- **`openai`**: The `openai` library is used to interact with the Azure OpenAI API for text translation.

- **`dotenv`**: The `dotenv` library helps in loading environment variables from a `.env` file.

- **`tqdm`**: This library is used to display progress bars during dataset iteration.

- **`json`**: This library is used for JSON file manipulation.

- **`datasets`**: The `datasets` library is used to load and work with datasets.

- **`time`**: It is used for adding delays to avoid reaching API rate limits.

### Functions

1. **`azure_openai_translate()`**
   - **Purpose:** This function performs the main translation process, iterating through a dataset, translating text to English, and handling errors and response logging.
   - **Parameters:** None.
   - **Usage:** It is called when the script is executed.

2. **`my_load_dataset()`**
   - **Purpose:** This function loads the dataset that needs to be translated.
   - **Parameters:** None.
   - **Usage:** Called within `azure_openai_translate()` to load the dataset.

3. **`translate(text)`**
   - **Purpose:** This function translates a given text to English using the Azure OpenAI API.
   - **Parameters:** 
     - `text` (str): The text to be translated.
   - **Usage:** Called within `azure_openai_translate()` to perform the actual translation.

4. **`union_responses()`**
   - **Purpose:** This function aggregates all the translated responses into a single JSON file.
   - **Parameters:** None.
   - **Usage:** Called after `azure_openai_translate()` to consolidate the translation results.

### .env File
- The script uses the `load_dotenv` function to load environment variables from a `.env` file, which is expected to be present in the same directory as the script. The following environment variables are expected in the `.env` file:
   - `AZURE_OPENAI_KEY`: API key for Azure OpenAI.
   - `AZURE_OPENAI_ENDPOINT`: Endpoint for Azure OpenAI.

## `openai_translate.py`

### Python File
- **File Name:** `openai_translate.py`
- **Purpose:** This Python script translates a given text to English using the OpenAI API.

### Libraries Used
- **`os`**: This library provides a way to use operating system-dependent functionality, such as reading environment variables.

- **`openai`**: The `openai` library is used to interact with the OpenAI API for text translation.

- **`dotenv`**: The `dotenv` library helps in loading environment variables from a `.env` file.

### Functions

1. **`openai_translate()`**
   - **Purpose:** This function translates a pre-defined text to English using the OpenAI API.
   - **Parameters:** None.
   - **Usage:** It is called when the script is executed.

### .env File
- Similar to `azure_openai_translate.py`, this script also uses the `load_dotenv` function to load environment variables from a `.env` file. The expected environment variable is:
   - `OPENAI_API_KEY`: API key for OpenAI.

---

These scripts primarily focus on translating text using either the Azure OpenAI API (`azure_openai_translate.py`) or the OpenAI API (`openai_translate.py`). They both rely on environment variables loaded from a `.env` file for API authentication. The former script is designed for batch translation of datasets and includes error handling and response aggregation functionalities. The latter script demonstrates a simple translation task for a predefined text.