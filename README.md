# Text Tutor: Getting Texts to Make Sense

This application provides a simple and intuitive user interface that helps understand a text by providing additional cues. Word-level cues like Part-of-Speech (ADJ, NOUN, VERB, etc.) or grammatical function (subj, obj, indirect obj, etc.) are invoked by default, while additional functionalities like translation (using GoogleTranslate) and rephrasing (using OLLaMa's mistral model) can be leveraged on demand.

## Installation Instructions

- Step 0: Create a folder on your machine. Navigate into this folder using the command prompt, then clone this repository by running "git clone https://github.com/Fisherman-s-Friend/text-tutor.git"
- Step 1: Download and install OLLaMa (https://ollama.com/download).
  - Step 1a: Open the command prompt and type "ollama run mistral" or "ollama pull mistal" in order to pull the mistral model to your machine.
- Step 2: Download and install PostgreSQL (https://www.postgresql.org/download/).
  - Step 2a: Keep the master password you are prompted to set in mind.
  - Step 2b: Create an empty database and keep the name in mind.
- Step 3: Open the cloned repository by double-clicking on it, then open the folder "flask-server". Once in there, open the file "server.py" and write the database master password and the database name into it (rows 15 & 16).
- Step 4: Go back to the command prompt and navigate to the directory with the cloned repository. Start the application by running "main.py". This will automatically install all the dependencies, establish a connection to both the database and OLLaMa and open up the application in your browser.

## Usage Instructions

Once the application is open in your browser, you can log in on the "Sign In" page or input a text on the "Home" page. If you are signed in, your past requests will be saved in the database and can be retrieved quickly. Once you have copied or written the text into the input box, you can click the "Submit" button. This will process the text, which might take a couple of dozens of seconds.

A new box will then appear with the processed text. Upon hovering over individual words, additional information such as Part-of-Speech tags and grammatical function will be displayed.

For additional information - such as translation or rephrasing of (parts of) sentences, as well as getting definitions and synonyms for individual words - the text on which the action should be performed needs to be selected in the **input window**. Upon doing that, a context menu will appear (in case it does not, it can be prompted to open by right-clicking), where the desired action can be performed by hovering over it. In order to close the context menu, hover over "Hide".
