import pandas as pd


def get_dataframe():
    df = pd.read_csv("./data/stories.csv", sep=";")
    df['avg_word_length'] = df.apply(lambda row: row["letters_count"] / row["words_count"], axis=1)
    df['avg_sentence_length'] = df.apply(lambda row: row["words_count"] / row["sentences_count"], axis=1)
    df['avg_paragraph_length'] = df["sentences_count"] / df["paragraphs_count"]

    df["author_label"] = df.apply(lambda row: -1 if row["author"] == "A_I_Kuprin" else 1, axis=1)
    df = df[df.columns.difference(["author", "name"])]
    return df
