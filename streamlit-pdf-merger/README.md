# Streamlit PDF Merger

This project is a Streamlit application that allows users to upload two PDF files and merge them into a single PDF file. The application handles file uploads, processes the PDFs, and provides a download link for the merged file.

## Project Structure

```
streamlit-pdf-merger
├── app.py
├── requirements.txt
└── README.md
```

## Setup Instructions

To set up the project, follow these steps:

1. **Create a new Conda environment:**
   ```bash
   conda create --name pdf python=3.9
   ```

2. **Activate the environment:**
   ```bash
   conda activate pdf
   ```

3. **Install the required packages:**
   ```bash
   pip install streamlit PyPDF2
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

## Exporting the Environment

To export the Conda environment into the repository, use the following command:

```bash
conda env export > environment.yml
```

This will create an `environment.yml` file that can be used to recreate the environment later.