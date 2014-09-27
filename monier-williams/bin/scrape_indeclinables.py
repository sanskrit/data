import sys

import util

def scrape(xml_path):
    """Scrape indeclinables from the MW dictionary."""

    labels = ['name']
    rows = []
    regexp = 'body>\s*<lex>ind'
    for i, xml in enumerate(util.iter_mw_xml(xml_path, regexp=regexp)):
        word = xml.find('h/key1').text
        rows.append([word])
        # util.tick(word, i, 50)

    rows.sort(key=lambda x: util.key_fn(x[0]))
    print util.make_csv_string(labels, rows)


def main():
    path = sys.argv[1]
    scrape(path)


if __name__ == '__main__':
    main()
