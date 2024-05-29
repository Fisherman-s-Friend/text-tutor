# Text Tutor: Getting Texts to Make Sense

This application provides a simple and intuitive user interface that helps understand a text by providing additional cues. Word-level cues like Part-of-Speech (ADJ, NOUN, VERB, etc.) or grammatical function (subj, obj, indirect obj, etc.) are invoked by default, while additional functionalities like translation (using GoogleTranslate) and rephrasing (using OLLaMa's mistral model) can be leveraged on demand.

## Installation Instructions

- Step 1: Install OLLaMa
  - Step 1a: Open the command prompt and type "ollama run mistral" or "ollama pull mistal" in order to pull the mistral model to your machine.
- Step 2: Install PostgreSQL.
  - Step 2a: Keep the master password you are prompted to set in mind.
  - Step 2b: Create an empty database and keep the name in mind.
- Step 3: Write these two strings - the master password and the database name - into the "server.py" file (rows 15 & 16), in the folder "flask-server".
- Step 4: Start the application by running "main.py". This will automatically install all the dependencies, establish a connection to both the database and OLLaMa and open up the application in your browser.

## Usage Instructions

Once the application is open in your browser, you can log in on the "Sign In" page or input a text on the "Home" page. If you are signed in, your past requests will be saved in the database and can be retrieved quickly. Once you have copied or written the text into the input box, you can click the "Submit" button. This will process the text, which might take a couple of dozens of seconds.

A new box will then appear with the processed text. Upon hovering over individual words, additional information such as Part-of-Speech tags and grammatical function will be displayed.

For additional information - such as translation or rephrasing of (parts of) sentences, as well as getting definitions and synonyms for individual words - the text on which the action should be performed needs to be selected in the **input window**. Upon doing that, a context menu will appear (in case it does not, it can be prompted to open by right-clicking), where the desired action can be performed by hovering over it. In order to close the context menu, hovering over "Hide" is needed.
