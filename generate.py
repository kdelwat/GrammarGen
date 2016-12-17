import pypandoc

filters = ['filter.py']


def generate(markdown, theme='Default'):
    '''Takes a markdown string and returns a full HTML document, ready to save.'''
    return pypandoc.convert_text(markdown, 'html', format='md', filters=filters)
