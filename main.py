import pypandoc


def ensure_pandoc_exists():
    '''Check the current Pandoc version. If it isn't installed, download it using
    pypandoc.
    '''
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.pypandoc.pandoc_download()


def main():
    ensure_pandoc_exists()


if __name__ == '__main__':
    main()
