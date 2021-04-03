def clean_string(s):
    s = s.replace('\r', '\\r')
    s = s.replace('\n', '\\n')
    return s
