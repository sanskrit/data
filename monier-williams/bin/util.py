import re
import xml.etree.cElementTree as ET


def key_fn(x):
    sounds = 'aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlLvSzsh|'
    assert all (L in sounds for L in x), x
    return tuple(sounds.index(L) for L in x)


def iter_mw_xml(xml_path, regexp=None):
    """Yield lines from the MW dictionary as parsed XML. Since parsing XML is
    relatively slow, parse only those lines that match `regexp`. If `regexp`
    is ``None``, parse all lines.

    :param ctx: the current :class:`Context`
    :param regexp: the regular expression to use for filtering
    """
    for line in open(xml_path, 'r'):
        if regexp and re.search(regexp, line) is None:
            continue
        try:
            yield ET.fromstring(line)
        except ET.ParseError:
            pass


def make_csv_string(labels, rows):
    """Print the given data as a CSV
    :param labels: a list of labels
    :param rows: a list of lists of strings. Each inner list must have
                 a 1:1 correspondence with `labels`.
    """
    data = [','.join(labels)]
    data.extend(','.join([x or '' for x in row]) for row in rows)
    return '\n'.join(data)


def unique(items, key_fn=None):
    """Keep only the unique items in `items`, maintaining order.
    :param items: the list
    :param key_fn: a function that, given an item, returns some ID for
                   the item.
    """
    seen = set()
    returned = []
    for item in items:
        key = key_fn(item) if key_fn else item
        if key in seen:
            continue
        else:
            returned.append(item)
            seen.add(key)
    return returned


def tick(word, i, num):
    if i % num == 0:
        print '-', word
