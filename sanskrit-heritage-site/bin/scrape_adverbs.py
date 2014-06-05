import sys

import scrape_utils

trans = scrape_utils.translator


def scrape_adverbs(filename):
    """Gerunds (ktvA).
    
    Infinitives (tum) come from SL_final.xml, and other indeclinables
    come from the MW data.
    """
    labels = ['name', 'root', 'pos', 'modification']
    format_str = ','.join('{%s}' % x for x in labels)

    output = []
    output.append(','.join(labels))
    for xml in scrape_utils.iter_xml(filename):
        # Only gerunds
        ab = xml.find('ab')
        if not ab:
            continue

        name = xml.attrib['form']
        root = xml.find('s').attrib['stem']
        modification = trans[ab.find('cj')[0].tag]

        # Filter out e.g. "Asam"
        if name[-2:] not in ('vA', 'ya'):
            continue

        output.append(format_str.format(**{
            'name': name,
            'root': root,
            'pos': 'gerund',
            'modification': modification or '',
        }))

    return '\n'.join(output)



def main():
    if len(sys.argv) < 2:
        print 'Usage: scrape_adverbs.py <filename>'
        sys.exit()
    print scrape_adverbs(sys.argv[1])

if __name__ == '__main__':
    main()
