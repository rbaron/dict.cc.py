# -*- coding: utf-8 -*-

try:
    # python2
    import urllib2
except ImportError:
    # python3
    import urllib.request as urllib2

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
        formatted_word = word.replace(" ", "+")

        req = urllib2.Request(
            "http://"+subdomain+".dict.cc/?s="+formatted_word,
            None,
            {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}
        )

        res = urllib2.urlopen(req).read()
        return res.decode("utf-8")

    # Quick and dirty: find javascript arrays for input/output words on response body
    @classmethod
    def _parse_response(cls, response_body):

        in_list = []
        out_list = []

        def sanitize(word):
            return re.sub("[\\\\\"]", "", word)

        javascript_list_pattern = "\"[^,]+\""

        for line in response_body.split("\n"):
            if "var c1Arr" in line:
                in_list = map(sanitize, re.findall(javascript_list_pattern, line))
            elif "var c2Arr" in line:
                out_list = map(sanitize, re.findall(javascript_list_pattern, line))

        if not any([in_list, out_list]):
            return Result()

        soup = BeautifulSoup(response_body, "html.parser")

        # HTML parsing madness. Don't even bother.
        def extract_lang(html_b_selector):
            return re.sub("<[^>]*>| ", "", str(html_b_selector.contents[0])) \
                   if not html_b_selector.a \
                   else str(html_b_selector.a.contents[0])

        left_b_selector = soup.find_all("td", width="307")[0].b
        right_b_selector = soup.find_all("td", width="306")[0].b
        [left_lang, right_lang] = map(extract_lang, [left_b_selector, right_b_selector])

        # Okay, you can start bothering again.

        return Result(
            from_lang=left_lang,
            to_lang=right_lang,
            translation_tuples=zip(in_list, out_list),
        )

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


