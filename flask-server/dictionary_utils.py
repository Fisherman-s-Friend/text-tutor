import nltk
from nltk.corpus import wordnet as wn


def define_word(word, lang="eng"):
    nltk.download("wordnet")
    nltk.download("omw-1.4")  # Open Multilingual WordNet

    try:
        word_synsets = wn.synsets(word, lang=lang)
    except nltk.corpus.reader.wordnet.WordNetError:
        return "language n/a"

    return word_synsets[:5]


def get_synonyms(word, POS, lang="eng"):
    synonyms = []
    synsets = define_word(word, lang=lang)
    for synset in synsets:
        if synset.name().split(".")[1].upper() == POS[0]:
            print(synset)
            for lemma in synset.lemmas(lang=lang):
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())
    return synonyms[:5]


def get_dependency_and_pos(text, lang="en"):
    import stanza

    # stanza.download("en")

    # Initialize the English pipeline
    nlp = stanza.Pipeline(lang=lang)

    # Parse a sentence
    doc = nlp(text)

    return doc


if __name__ == "__main__":
    
    doc = get_dependency_and_pos("Nosotros veíamos los vecinos cuando entró il padre!", "es")
    for sentence in doc.sentences:
        for word in sentence.words:
            print(word.text, word.pos, word.head, word.deprel, word.lemma, word.start_char, word.feats)
