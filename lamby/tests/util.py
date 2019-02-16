def get_response_data(response):
    return response.get_data(as_text=True)


def remove_whitespace(text):
    text_without_spaces = text.replace(' ', '')
    text_without_spaces_and_newlines = text_without_spaces.replace('\n', '')
    return text_without_spaces_and_newlines


def get_response_data_without_whitespace(response):
    return remove_whitespace(get_response_data(response))
