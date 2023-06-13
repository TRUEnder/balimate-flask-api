from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stem = StemmerFactory().create_stemmer()
stopword = StopWordRemoverFactory().create_stop_word_remover()


def preprocessingWithoutStem(data):
    data = data.lower()
    data = stopword.remove(data)

    return data


def preprocessingWithStem(data):
    data = data.lower()
    data = stem.stem(data)
    data = stopword.remove(data)

    return data
