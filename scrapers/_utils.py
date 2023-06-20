import re

def extract_number_from_string(string):
    pattern = r"[-+]?\d*\.?\d+"
    matches = re.findall(pattern, string)
    if matches:
        return float(matches[0])
    else:
        return None