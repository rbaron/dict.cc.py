# -*- coding: utf-8 -*-

try:
    # python2
    import urllib2
    from urllib import quote_plus
except ImportError:
    # python3
    import urllib.request as urllib2
    from urllib.parse import quote_plus

import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
    BeautifulSoup.find_all = BeautifulSoup.findAll

AVAILABLE_LANGUAGES = {
    "en": "english",
    "de": "german",
    "fr": "french",
    "sv": "swedish",
    "es": "spanish",
    "bg": "bulgarian",
    "ro": "romanian",
    "it": "italian",
    "pt": "portuguese",
    "ru": "russian"
}


class UnavailableLanguageError(Exception):
    def __str__(self):
        return "Languages have to be in the following list: {}".format(
            ", ".join(AVAILABLE_LANGUAGES.keys()))


class Result(object):
    def __init__(self, from_lang=None, to_lang=None, translation_tuples=None):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.translation_tuples = list(translation_tuples) \
                                  if translation_tuples else []

    @property
    def n_results(self):
        return len(self.translation_tuples)


class Dict(object):
    @classmethod
    def translate(cls, word, from_language, to_language):
        if any(map(lambda l: l.lower() not in AVAILABLE_LANGUAGES.keys(),
                   [from_language, to_language])):
            raise UnavailableLanguageError

        response_body = cls._get_response(word, from_language, to_language)
        result = cls._parse_response(response_body)

        return cls._correct_translation_order(result, word)

    @classmethod
    def _get_response(cls, word, from_language, to_language):
        subdomain = from_language.lower()+to_language.lower()

        url = "https://"+subdomain+".dict.cc/?s=" + quote_plus(word.encode("utf-8"))

        req = urllib2.Request(
            url,
            None,
            {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}
        )

        res = urllib2.urlopen(req).read()
        return res.decode("utf-8")

    # Quick and dirty: find javascript arrays for input/output words on response body
    @classmethod
    def _parse_response(cls, response_body):
        soup = BeautifulSoup(response_body, "html.parser")

        suggestions = [tds.find_all("a") for tds in soup.find_all("td", class_="td3nl")]
        if len(suggestions) == 2:
            languages = [lang.string for lang in soup.find_all("td", class_="td2")][:2]
            if len(languages) != 2:
                raise Exception("dict.cc results page layout change, please raise an issue.")

            return Result(
                from_lang=languages[0],
                to_lang=languages[1],
                translation_tuples=zip(
                    [e.string for e in suggestions[0]],
                    [e.string for e in suggestions[1]]
                ),
            )

        translations = [tds.find_all("a") for tds in soup.find_all("td", class_="td7nl", attrs={'dir': "ltr"})]
        if len(translations) >= 2:
            languages = [next(lang.strings) for lang in soup.find_all("td", class_="td2", attrs={'dir': "ltr"})]
            if len(languages) != 2:
                raise Exception("dict.cc results page layout change, please raise an issue.")

            return Result(
                from_lang=languages[0],
                to_lang=languages[1],
                translation_tuples=zip(
                    [" ".join(map(lambda e: " ".join(e.strings), r)) for r in translations[0:-1:2]],
                    [" ".join(map(lambda e: e.string, r)) for r in translations[1:-1:2]]
                ),
            )

        return Result()

    # Heuristic: left column is the one with more occurrences of the to-be-translated word
    @classmethod
    def _correct_translation_order(cls, result, word):

        if not result.translation_tuples:
            return result

        [from_words, to_words] = zip(*result.translation_tuples)

        return result if from_words.count(word) >= to_words.count(word) \
                      else Result(
                          from_lang=result.to_lang,
                          to_lang=result.from_lang,
                          translation_tuples=zip(to_words, from_words),
                      )


