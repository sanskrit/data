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
    """Scrape unprefixed roots from the MW dictionary."""

    labels = ['root', 'hom', 'class', 'voice']
    rows = []

    all_vclasses = set('1 2 3 4 5 6 7 8 9 10 denom'.split())
    all_voices = set('para atma'.split())
    voice_translator = {'p': 'para', 'a': 'atma', 'a1': 'atma'}

    for i, xml in enumerate(util.iter_mw_xml(xml_path)):
        if has_prefix(xml):
            continue

        root = xml.find('h/key1').text

        paradigms = []
        vclasses = []
        voice = None

        # To make a paradigm, we need a class and voice. Viable roots come in
        # three flavors:
        #
        # - class and voice: gam
        # - class, no voice: patAkaya
        # - voice, no class: candrikAya
        #
        # Some roots have neither class and voice. These are currently
        # ignored.
        for token in tokenized_vlexes(xml):
            if token in all_vclasses:
                vclasses.append(token)
            elif token in voice_translator:
                voice = voice_translator[token]
                for vclass in vclasses:
                    paradigms.append((vclass, voice))
                vclasses = []

        # If the voice is not specified, search Sanskrit strings in the entry
        # to infer it.
        if vclasses and not paradigms:
            body = ET.tostring(xml.find('body'))

            # 'ti' at the end of a word
            if re.search('ti[,. <]', body):
                voice = voice_translator['p']
                for vclass in vclasses:
                    paradigms.append((vclass, voice))
            # 'te' or 'mAna' at the end of a word
            elif re.search('(te)|(mAna)|(mARa)[,. <]', body):
                voice = voice_translator['a']
                for vclass in vclasses:
                    paradigms.append((vclass, voice))

        # If the class is not specified, make some high-precision assumptions
        # about it.
        if voice and not paradigms:
            ends = root.endswith
            if ends('Aya') or ends('aya') or ends('Iya'):
                paradigms.append(('denom', voice))

        paradigms = [list(x) for x in util.unique(paradigms)]
        if not paradigms:
            continue

        # Some roots are homonymous. The MW <hom> element distinguishes one
        # root sense from another.
        hom = xml.find('h/hom')
        hom_value = hom.text if hom is not None else None

        for vclass, voice in paradigms:
            assert vclass in all_vclasses
            assert voice in all_voices
            rows.append((root, hom_value, vclass, voice))

    rows.sort(key=lambda x: util.key_fn(x[0]))
    print util.make_csv_string(labels, rows)


def main():
    path = sys.argv[1]
    scrape(path)


if __name__ == '__main__':
    main()
