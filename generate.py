import os
import pypandoc

filters = ['filter.py']
pandoc_arguments = ['--standalone', '--toc', '--smart', '--html-q-tags']


def generate(markdown, theme='Default'):
    '''Takes a markdown string and returns a full HTML document, ready to save.'''
    css_location = os.path.join('themes', '{0}.css'.format(theme))
    pandoc_arguments.append('--css={0}'.format(css_location))

    return pypandoc.convert_text(markdown, 'html', format='md',
                                 extra_args=pandoc_arguments, filters=filters)
