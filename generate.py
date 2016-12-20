import os
import re
import pypandoc

filters = ['filter.py']


def generate(markdown, theme='Default'):
    '''Takes a markdown string and returns a full HTML document, ready to save.'''
    pandoc_arguments = ['--standalone',
                        '--toc',
                        '--smart',
                        '--html-q-tags']

    html_name = '{0}.html'.format(theme)
    css_name = '{0}.css'.format(theme)

    pandoc_arguments.append('--include-in-header={0}'.format(os.path.join('themes', html_name)))
    pandoc_arguments.append('--include-in-header={0}'.format(os.path.join('themes', 'before.html')))
    pandoc_arguments.append('--include-in-header={0}'.format(os.path.join('themes', css_name)))
    pandoc_arguments.append('--include-in-header={0}'.format(os.path.join('themes', 'after.html')))
    #pandoc_arguments.append('--css={0}'.format(css_location))

    return pypandoc.convert_text(markdown, 'html', format='md',
                                 extra_args=pandoc_arguments, filters=filters)


def load_words_from_lexicon(html_string, lexicon):
    '''Replace all words surrounded by double curly braces in the HTML string
    (created by the filter) with their dictionary definition according to the given
    lexicon.'''
    match_list = re.findall(r'{{[a-z]*}}', html_string, re.I)

    for match in match_list:
        word = match[2:-2]
        try:
            definition, full_definition, part_of_speech = lookup_definition(word, lexicon)
            html_definition = create_html_definition(word, definition,
                                                     full_definition,
                                                     part_of_speech)

            html_string = html_string.replace(match, html_definition)
        except KeyError:
            pass

    return html_string


def lookup_definition(word, lexicon):
    '''Find information about the current word from the dictionary.'''
    for line in lexicon:
        if line[0] == word:
            return line[1], line[4], line[2]

    raise KeyError


def create_html_definition(word, definition, full_definition, part_of_speech):
    html_string = '''<span class="word">{0}
    <span class="definition">{2} ({1})<br>
        <span class="full-definition">{3}</span>
    </span>
</span>'''

    return html_string.format(word, part_of_speech, definition, full_definition)
