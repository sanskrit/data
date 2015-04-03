import re
import sys
import xml.etree.cElementTree as ET

import util

UPASARGAS = """
ati
aDi
anu
antar
apa
api
aBi
ava
A
ud
upa
dus
ni
nis
parA
pari
upra
prati
vi
sam
su
"""

def make_tidy(prefix):
    """Undo certain kinds of sandhi. This is a hacky upasarga check."""
    if not prefix:
        return prefix
    if prefix.endswith('A'):
        return prefix[:-1] + 'a'
    if prefix[-1] in 'zr':
        return prefix[:-1] + 's'
    if prefix.endswith('M'):
        return prefix[:-1] + 'm'
    return prefix


def scrape(xml_path):
    """Scrape verb prefixed from the MW dictionary."""

    upasargas = set(UPASARGAS.splitlines())
    labels = ['name', 'prefix_type']
    regexp = 'root'

    rows = []
    for i, xml in enumerate(util.iter_mw_xml(xml_path, regexp=regexp)):
        key1 = xml.find('h/key1')
        key2 = xml.find('h/key2')
        entry = key1.text
        if not (entry.endswith('kf') or entry.endswith('BU')):
            continue

        # A root is prefixed iff it has a <root> element. Any matches without
        # one are almost certainly nominals, which we can disregard.
        root = key2.find('.//root')
        if root is None:
            continue

        # Remove lingering XML
        root.clear()
        key2.tag = None
        name = ET.tostring(key2)
        name = re.sub('(<.*?>)|/', '', name)

        # Remove groups ending in upasargas
        splits = [x for x in name.split('-') if x]
        last = splits[-1]
        if last in upasargas or make_tidy(last) in upasargas:
            continue


        # Add prefixes to the proper category
        name = ''.join(splits)
        _type = None

        if name[-1] in ('I', 'U'):
            _type = 'cvi'
        elif name.endswith('A'):
            _type = 'DAc'
        else:
            _type = 'other'

        # 'sampra' is suggested as a prefix. This is wrong.
        if name == 'sampra':
            continue

        rows.append((name, _type))

    rows = util.unique(rows, lambda x: x[0])
    rows.sort(key=lambda x: util.key_fn(x[0]))
    print util.make_csv_string(labels, rows)


def main():
    path = sys.argv[1]
    scrape(path)


if __name__ == '__main__':
    main()
