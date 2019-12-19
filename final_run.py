from analyze import simple_case, with_choosing_c_param, with_svd


def final():
    savePlots = True
    columnss = [[] for i in range(4)]
    columnss[0] = ["letters_count", "words_count"]
    columnss[1] = ["sentences_count", "words_count"]
    columnss[2] = ["avg_word_length", "avg_sentence_length"]
    columnss[3] = ["letters_count", "total_punctuation_signs"]

    simple_cvs = [simple_case(columns, savePlots) for columns in columnss]

    with_choosing_c_param_cvs = [with_choosing_c_param(columns, savePlots) for columns in columnss]

    svd_cvs = with_svd(savePlots)

    print(simple_cvs)
    print(with_choosing_c_param_cvs)
    print(svd_cvs)

if __name__ == '__main__':
    final()