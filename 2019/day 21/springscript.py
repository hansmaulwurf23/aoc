def preprocess_script(script):
    out = []
    for line in script.split('\n'):
        if line.strip() and not line.startswith('#'):
            out.extend(list(map(ord, line)) + [10])

    return out

def print_output(output):
    for o in output:
        if 0 <= o <= 255:
            print(chr(o), end='')
        else:
            print(o)

    return output