import re
import sys
import xml.etree.cElementTree as ET

import util


def has_prefix(xml):
    """Return ``True`` iff `xml` has a prefix. `xml` should represent a
    verb root.

    :param xml: an :class:`~xml.etree.Element`
    """
    key2 = ET.tostring(xml.find('h/key2'))
    return ('-' in key2 or '<srs' in key2)


def tokenized_vlexes(xml):
    """Generate tokens from <vlex> items.

    :param xml: the :class:`~xml.etree.Element` to check
    """
    for vlex in xml.findall('.//vlex'):
        vlex = re.sub('\\_|\\.', ' ', vlex.text or '')
        for token in vlex.lower().split():
            yield token


def scrape(xml_path):
    """Scrape prefixed roots from the MW dictionary.

    This function doesn't scrape everything, but it's good enough.
    """

    labels = ['prefixed_root', 'unprefixed_root', 'hom']
    rows = []

    for i, xml in enumerate(util.iter_mw_xml(xml_path, 'vlex')):
        if not has_prefix(xml):
            continue

        prefixed_root = xml.find('h/key1').text

        # Skip any entries without a <root> element. This element wraps the
        # unprefixed root. If <root> is absent, this probably isn't a prefixed
        # root.
        #
        # TODO: The following prefixed roots have no <root> element:
        # - gavez
        # - pAWAntaraya
        # - sampalAy
        # - samprAv
        unprefixed_root = None
        root_elem = xml.find('.//root')
        if root_elem is not None:
            unprefixed_root = root_elem.text
            if (not unprefixed_root) and root_elem.tail:
                unprefixed_root = root_elem.tail.strip()

        if not unprefixed_root or unprefixed_root == '~':
            continue

        # Some roots are homonymous. The MW <hom> element distinguishes one
        # root sense from another.
        hom = xml.find('.//root/hom')
        hom_value = hom.text if hom is not None else None

        rows.append((prefixed_root, unprefixed_root, hom_value))

    rows.sort(key=lambda x: util.key_fn(x[0]))
    print util.make_csv_string(labels, rows)


def main():
    path = sys.argv[1]
    scrape(path)


if __name__ == '__main__':
    main()
