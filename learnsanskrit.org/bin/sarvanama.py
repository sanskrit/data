#!/usr/bin/env python
import re
from pathlib import Path


LSO_DIR = Path(__file__).parent.parent


def _number(i) -> str:
    d = {
        0: "s",
        1: "d",
        2: "p",
    }
    return d[i]


def _case(i) -> str:
    d = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        5: "6",
        6: "7",
        7: "8",
    }
    return d[i]


def _apply_natva(s: str) -> str:
    """Apply `n` --> `ṇ` retroflexion."""
    # For details, see Ashtadhyayi 8.4.1 - 8.4.2.
    return re.sub(r"([fFrz][aAiIuUfFxXeEoOhyvrkKgGNpPbBm]*)n(.)", r"\1R\2", s)


def _create_pada(base: str, ending: str) -> str:
    raw_pada = base[:-1] + ending
    return _apply_natva(raw_pada)


bases = [
    "sarva",
    "viSva",
    "uBa",
    "uBaya",
    "katara",
    "yatara",
    "tatara",
    "ekatara",
    "katama",
    "yatama",
    "tatama",
    "ekatama",
    "anya",
    "anyatara",
    # Turn these off for now as they are rare.
    # "tvat",
    # "tva",
    "itara",
    "nema",
    "sama",
    "sima",
    "pUrva",
    "para",
    "avara",
    "dakziRa",
    "uttara",
    "apara",
    "aDara",
    "sva",
    "antara",
    "eka",
    "dvi",
]

t_bases = [
    "katara",
    "yatara",
    "tatara",
    "ekatara",
    "katama",
    "yatama",
    "tatama",
    "ekatama",
    "anya",
    "anyatara",
    "itara",
]

pum_endings = [
    "as",
    "O",
    "e",
    "am",
    "O",
    "An",
    "ena",
    "AByAm",
    "Es",
    "asmE",
    "AByAm",
    "eByas",
    "asmAt",
    "AByAm",
    "eByas",
    "asya",
    "ayos",
    "ezAm",
    "asmin",
    "ayos",
    "ezu",
    "as",
    "O",
    "e",
]
stri_endings = [
    "A",
    "e",
    "As",
    "Am",
    "e",
    "As",
    "ayA",
    "AByAm",
    "ABis",
    "asyE",
    "AByAm",
    "AByas",
    "asyAs",
    "AByAm",
    "AByas",
    "asyAs",
    "ayos",
    "AsAm",
    "asyAm",
    "ayos",
    "Asu",
    "A",
    "e",
    "As",
]
napum_endings = ["am", "e", "Ani"] * 2 + pum_endings[6:18] + ["am", "e", "Ani"] * 2

assert len(napum_endings) == len(pum_endings) == len(stri_endings)

genders = {
    "m": pum_endings,
    "f": stri_endings,
    "n": napum_endings,
}


def _create_inflected_words(output_file: Path):
    buf = []
    buf.append("stem,stem_genders,form,form_gender,case,number")
    for base in bases:
        for (gender, endings) in genders.items():
            for i, ending in enumerate(endings):
                number = _number(i % 3)
                case = _case(i // 3)
                if number != "d" and base in {"uBa", "dvi"}:
                    continue

                # For "anyat," etc.
                # https://ashtadhyayi.com/sutraani/7.1.25
                if base in t_bases and (gender, number) == ('n', 's') and case in ('1', '2'):
                    ending = 'at'

                pada = _create_pada(base, ending)
                row = [base, "mfn", pada, gender, case, number]
                buf.append(",".join(row))
    output_file.write_text("\n".join(buf) + "\n")


def main():
    output_file = LSO_DIR / "sarvanamas-inflected.csv"
    _create_inflected_words(output_file)
    pass


if __name__ == "__main__":
    main()
