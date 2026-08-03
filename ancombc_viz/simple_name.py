def extract_p_g_or_f(top: str) -> str:
    """
    formatting taxon string return to level(p/f/g).
    """
    if top == "Others":
        return "Others"

    parts = top.split(";")
    p = [x for x in parts if x.startswith("p__")]
    c = [x for x in parts if x.startswith("c__")]
    o = [x for x in parts if x.startswith("o__")]
    f = [x for x in parts if x.startswith("f__")]
    g = [x for x in parts if x.startswith("g__")]

    stripped = top.strip()
    last = parts[-1]
    # 0) End completely "o__;f__;g__" likes pattern → p + c
    if len(parts) >= 3 and parts[-3:] == ["o__", "f__", "g__"]:
        pg = ";".join(p + c)

    # 1) End to "g__", but genus name have empty space  → p + f
    elif last == "g__":
        pg = ";".join(p + f)

    # 2) Normal genus pattern ("g__" name included) → p + g 
    elif g and stripped.endswith(g[-1]):
        pg = ";".join(p + g)

    # 3) Not included "g__", end at "f__"  → p + c
    elif (not g) and f and last.startswith("f__"):
        pg = ";".join(p + c)

    # Normal: p + g (if doesn't have "g__", start with "p__")
    else:
        pg = ";".join(p + g)

    return pg if pg else top
