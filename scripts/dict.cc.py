#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import re
import colorama as clr

from dictcc import Dict, AVAILABLE_LANGUAGES

clr.init(autoreset=True)

LINE_LENGTH = 60


def ensure_unicode(string):
    if hasattr(string, "decode"):
        return string.decode("utf-8")
    return string


def str2bool(v):
    """
    Used to parse binary flag args
    Copy-paste from stack overflow
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_args():
    parser = argparse.ArgumentParser(description="Unoficial CLI for dict.cc. "\
        "It supports translations between the following languages: {}".format(
        ", ".join(AVAILABLE_LANGUAGES)))
    parser.add_argument("input_language", type=str, help="Input language",
        choices=AVAILABLE_LANGUAGES.keys())
    parser.add_argument("output_language", type=str, help="Output language",
        choices=AVAILABLE_LANGUAGES.keys())
    parser.add_argument("word",
                         type=ensure_unicode,
                         help=("Word to translate (use quotation marks for "
                               "phrases like \"free beer\")."))
    parser.add_argument("--max-results", "-n", type=int, default=10,
                        help="Number of results to display. -1 for no limit.")
    parser.add_argument("--color", "-c", type=str2bool, default=True,
                        help="Use color in output.")
    args = parser.parse_args()

    if args.input_language == args.output_language:
        raise ValueError("Please choose different languages")

    return args


def print_header(from_lang, to_lang):
    print(u"{}{}{}\n{}{}{}".format(
        from_lang,
        " "*(LINE_LENGTH-len(from_lang)),
        to_lang,
        "="*len(from_lang),
        " "*(LINE_LENGTH-len(from_lang)),
        "="*len(to_lang),
    ))


def print_translation(input_word, output_word, do_color, search_phrase):
    def apply_color(string):
        if do_color:
            # Apply color codes to string for meta data and searched word

            # Meta data is found within square or curly brackets
            # First replace square brackets as the color codes themselves
            # contain square brackets which should not be replaced
            string = string.replace("[", clr.Fore.BLUE + "[")\
                            .replace("]", "]" + clr.Fore.RESET)
            string = string.replace("{", clr.Fore.BLUE + "{")\
                            .replace("}", "}" + clr.Fore.RESET)

            # Colorize words in search_phrase
            # 1.Remove non alphabet characters from search_phrase
            # 2.Split on spaces.
            # 3.Match words in search_phrase as whole words only, ignore case
            # NB. if the word is within brackets colorization will be inaccurate
            for wrd in re.sub('[^\w] ', '', search_phrase).split(" "):
                string = re.sub(r"\b(" + re.escape(wrd) + r")\b",
                            clr.Fore.GREEN + r"\1" + clr.Fore.RESET,
                            string,
                            flags=re.IGNORECASE)
        return string

    # Three points less for the spaces and one point less for the equal sign,
    # so tables don't break
    padding_len = LINE_LENGTH-len(input_word)-4
    print(u"{} {} = {}".format(apply_color(input_word),
                                "."*padding_len,
                                apply_color(output_word)))



def run():
    args = parse_args()

    result = Dict.translate(args.word,
                            args.input_language,
                            args.output_language)

    if not result.n_results:
        print("No results found for {} ({} <-> {}).".format(
            args.word, args.input_language, args.output_language))
        return
    else:
        print("Showing {} of {} result(s)\n".format(
            min(args.max_results, result.n_results), result.n_results))

    print_header(result.from_lang, result.to_lang)

    for i, (input_word, output_word) in enumerate(result.translation_tuples):
        print_translation(input_word, output_word, args.color, args.word)
        if i == args.max_results:
            break


if __name__ == "__main__":
    run()


