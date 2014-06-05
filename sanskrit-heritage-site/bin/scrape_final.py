import sys

import scrape_utils

trans = scrape_utils.translator


def scrape_adverbs(filename):
    """Gerunds (lyap) and infinitives (tum).
    
    'tvA' gerunds come from SL_adverbs.xml.
    """
    labels = ['name', 'root', 'pos', 'modification']
    format_str = ','.join('{%s}' % x for x in labels)

    output = []
    output.append(','.join(labels))
    for xml in scrape_utils.iter_xml(filename):
        vu = xml.find('vu')
        if vu is None:
            continue

        name = xml.attrib['form']
        root = xml.find('s').attrib['stem']

        modification = trans[vu.find('cj')[0].tag]
        huet_pos = vu.find('iv')[0].tag
        if huet_pos == 'abs':
            pos = 'gerund'
        elif huet_pos == 'inf':
            pos = 'infinitive'
        else:
            raise Exception("Unknown POS %s" % huet_pos)

        output.append(format_str.format(**{
            'name': name,
            'root': root,
            'pos': pos,
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
