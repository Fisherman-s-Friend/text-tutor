from googletrans import Translator
import nltk
from nltk.corpus import wordnet as wn

import stanza

stanza.download("en")


def translate(text, source="en", dest="en") -> str:
    translator = Translator()
    translated_text = translator.translate(text, src=source, dest=dest).text
    return translated_text


def wordnet(word, lang="eng"):
    nltk.download("wordnet")
    nltk.download("omw-1.4")  # Open Multilingual WordNet

    word_synsets = wn.synsets(word, lang=lang)

    return word_synsets


def stanza_pipeline(text, lang="en"):
    # Initialize the English pipeline
    nlp = stanza.Pipeline(lang=lang)

    # Parse a sentence
    doc = nlp(text)

    # Iterate over sentences and print token text and part-of-speech tags
    for sentence in doc.sentences:
        for word in sentence.words:
            print(
                f"Word: {word.text}\tPart-of-Speech: {word.pos}\tHead: {word.head}\tDependency Relation: {word.deprel}"
            )

    return doc


if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog."
    translated_text = translate(text, dest="it")
    print(translated_text)
    word = "dog"
    word_synsets = wordnet(word)
    print(word_synsets)
    stanza_pipeline(translated_text, lang="es")
