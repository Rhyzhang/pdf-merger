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

To set up and run this project, please follow these steps:

1.  **Create the Conda Environment**:
    Open your terminal and run the following command from the root of the repository to create a new Conda environment from the `environment.yml` file. This file contains all the necessary dependencies.

    ```bash
    conda env create -f ../environment.yml
    ```

2.  **Activate the Environment**:
    Once the environment is created, activate it using:

    ```bash
    conda activate pdf
    ```

3.  **Run the Application**:
    With the environment activated, you can start the Streamlit application by running:

    ```bash
    streamlit run app.py
    ```

## Exporting the Environment

If you make changes to the environment, such as adding new packages, you should update the `environment.yml` file. To export the current Conda environment, use the following command from within the `streamlit-pdf-merger` directory:

```bash
conda env export --name pdf > ../environment.yml
```

This will create an `environment.yml` file that can be used to recreate the environment later.