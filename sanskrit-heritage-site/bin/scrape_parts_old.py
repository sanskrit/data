"""
Scrapes an older version of SL_parts.xml.
"""
import sys
import xml.etree.cElementTree as ET

import scrape_utils

trans = scrape_utils.translator

def scrape(parts_file):
    """Participles."""

    labels = ['stem', 'root', 'class', 'mode', 'voice', 'modification']
    rows = []
    num_written = 0

    for xml in scrape_utils.iter_xml(parts_file):
        form = xml.attrib['form']
        root = xml.find('s').attrib['stem']

        for pa in xml.findall('pa'):
            # Inflectional info
            na = pa.find('na')
            case = trans[na[0].tag]
            number = trans[na[1].tag]
            gender = trans[na[2].tag]

            if (gender, case, number) != ('m', '1', 's'):
                continue

            # Morphological info (stem)
            modification = trans[pa.find('cj')[0].tag]
            mode_elem = pa.find('no')[0]
            mode, voice = trans[mode_elem.tag]
            if (mode, voice) == ('pres', 'active'):
                vclass = mode_elem[0].text
                voice = trans[mode_elem[1].tag]
            elif (mode, voice) in [('fut', 'active'), ('perf', 'active')]:
                vclass = None
                voice = trans[mode_elem[0].tag]
            else:
                vclass = None
                # voice = default

            # '11', '12', and '13' refer to "modified" verb classes. We can
            # just discard these.
            if vclass and modification is not None:
                vclass = None

            # Construct stem
            if form[-1] == 's':
                stem = form[:-1]
            elif form.endswith('an'):
                stem = form[:-1] + 't'   # -an  -> -at
            elif mode == 'perf':
                stem = form[:-2] + 'as'  # -vAn -> -vas
            elif mode == 'past':
                stem = form[:-2] + 'at'  # -vAn -> -vat
            else:
                # Encoding error, but high recall is OK.
                stem = form

            rows.append((stem, root, vclass, mode, voice, modification))
            num_written += 1

    return labels, rows


def main():
    if len(sys.argv) < 2:
        print 'Usage: scrape_roots.py <parts_file>'
        sys.exit()
    labels, rows = scrape(sys.argv[1])
    print scrape_utils.make_csv_string(labels, rows)


if __name__ == '__main__':
    main()
