from langdetect import detect


def to_sentences(text):
    text = text.replace("\n", " ")
    sentences = [s + '.' for s in text.split(".") if s != ""]
    return sentences

def divide(text, input_size=5000):
    """
    Divide text into chunks of input_size

    Args:
        text (str): Text to be divided
        input_size (int): Size of each chunk
    """
    # short input_size if asian
    lang = detect(text)
    if lang in ['ko', 'ja', 'zh-cn', 'zh-tw', 'zh-hk']:
        input_size = min(input_size, 1300)

    # divide text by words
    text = to_sentences(text)
    result = []
    temp = ""
    for word in text:
        if len(temp + word) >= input_size:
            result.append(temp)
            temp = ""
        temp += word
    result.append(temp)
    return result
