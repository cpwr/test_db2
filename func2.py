def handle_string1(value):
    d = {"Letters": 0, "Digits": 0}

    for k in value:
        if k.isalpha():
            d["Letters"] += 1
        elif k.isdigit():
            d["Digits"] += 1

    return f"Letters - {d['Letters']}\nDigits - {d['Digits']}"
