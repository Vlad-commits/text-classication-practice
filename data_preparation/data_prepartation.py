import os
import re
from typing import TextIO
from tokenizer import tokenize, TOK
from tokenizer import split_into_sentences


def extract_data(file_name: str):
    with open(file_name, "r", encoding="UTF-8") as file:
        return extract_many(file)


def extract_many(file: TextIO):
    paragraphs = []
    for paragraph in file:
        paragraph = paragraph.strip()
        if not (paragraph.isspace() | len(paragraph) == 0):
            obj = new_extract(paragraph)
            paragraphs.append(obj)
    return paragraphs


def new_extract(paragraph: str):
    paragraph_info = {"sentences_info": [], "question_marks_count": paragraph.count("?")}
    for sentence in split_into_sentences(paragraph):
        sentence_info = {"words_lengths": [], "punctuation_sings_count": 0}
        for token in tokenize(sentence):
            if token.kind == TOK.WORD:
                sentence_info["words_lengths"].append(len(token.txt))
            elif token.kind == TOK.PUNCTUATION:
                sentence_info["punctuation_sings_count"] += 1
        paragraph_info["sentences_info"].append(sentence_info)
    return paragraph_info


# def extract(paragraph: str):
#     sentences = [i.strip() for i in re.split(r"""[.?!;]""", paragraph) if
#                  not (len(i.strip()) == 0 | i.strip().isspace())]
#     paragraph_info = {"sentences_info": [], "question_marks_count": paragraph.count("?")}
#
#     for sentence in sentences:
#         sentence_info = {"words_lengths": []}
#         words = [i.strip() for i in re.split(r"""[^\d\w]""", sentence) if
#                  not (len(i.strip()) == 0 | i.strip().isspace())]
#         for index, word in enumerate(words):
#             sentence_info["words_lengths"].append(len(word))
#         paragraph_info["sentences_info"].append(sentence_info)
#     return paragraph_info


def reduce_data(paragraphs_info: list):
    total_paragraphs = len(paragraphs_info)
    total_sentences = sum([len(pi["sentences_info"]) for pi in paragraphs_info])
    total_question_marks = sum([pi["question_marks_count"] for pi in paragraphs_info])
    total_punctuation_signs = sum(
        [sum([si["punctuation_sings_count"] for si in pi["sentences_info"]]) for pi in paragraphs_info])
    total_words = sum([sum([len(si["words_lengths"]) for si in pi["sentences_info"]]) for pi in paragraphs_info])
    total_letters = sum([sum([sum(si["words_lengths"]) for si in pi["sentences_info"]]) for pi in paragraphs_info])
    return str(total_paragraphs) + ";" + str(total_sentences) + ";" + str(total_words) + ";" + str(
        total_letters) + ";" + str(total_question_marks) + ";" + str(total_punctuation_signs)


def transform(file_name: str, author: str):
    p = extract_data(file_name)
    return reduce_data(p) + ";" + file_name + ";" + author + "\n"


def process():
    lines = []
    dir1 = "./data/A_I_Kuprin"
    for fileName in os.listdir(dir1):
        print("processing " + fileName)
        lines.append(transform(dir1 + os.sep + fileName, "A_I_Kuprin"))
    dir2 = "./data/A_P_Chehov"
    for fileName in os.listdir(dir2):
        print("processing " + fileName)
        lines.append(transform(dir2 + os.sep + fileName, "A_P_Chehov"))
    with open("./data/stories.csv", "w+", encoding="UTF-8") as f:
        f.write("paragraphs_count;sentences_count;words_count;letters_count;total_question_marks;total_punctuation_signs;name;author\n")
        f.writelines(lines)
        f.flush()
    print("Done")


process()
