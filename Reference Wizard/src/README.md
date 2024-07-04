# Reference Wizard

Reference Wizard is a desktop application designed to transform academic references into BibTeX format. It leverages `mistral-7b-openorca` from GPT4All to intelligently parse and reformat references from plain text into the structured format required for LaTeX document preparation.

## Features

- Converting academic references into BibTeX entries with a single click.
- Processing multiple references at once. Each reference should be separated by a blank line.
- Adjusting the behavior of the GPT-4 model to suit your preferences.
- Importing references from a text file and export the BibTeX entries to a `.bib` file.
- An in-built guide explains the adjustable parameters and their impact on the conversion.

## Installation

Ensure that Python and the necessary dependencies are installed on your machine.

1. Clone the Reference Wizard repository to your local machine.
2. Navigate to the cloned directory via the terminal.
3. Install the required Python package using pip:

   ```sh
   pip install gpt4all
This command will:

- Instantiate GPT4All, the primary API for interacting with the LLM.
- Automatically download the specified model - `mistral-7b-openorca` to ~/.cache/gpt4all/ if it's not already present.

## Note:

The model's size is approximately 3.83 GB.
The default path used by gpt4all's Python library is /home/user/.cache/gpt4all, where the model will be installed.

- To start the application, run the reference_wizard.py script:

   ```sh
   python reference_wizard.py
# How to Use
1. Upon launching Reference Wizard, you'll see two main text areas. The left text area is for inputting your academic references, and the right area will display the generated BibTeX entries.
2. Input your references in the left text area. Make sure to separate each reference with a blank line.
3. Click the "Generate BibTeX" button. The BibTeX entries will appear on the right.
4. Use the "Import" and "Export" buttons to manage your references and BibTeX files.
5. Access the "Settings" to adjust parameters like temperature (temp), top_k, top_p, etc., which affect the generation process.
6. Click on "Help" for guidance on what each parameter does and how to use them effectively.

Thank you for using Reference Wizard!