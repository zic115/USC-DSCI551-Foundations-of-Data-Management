def printf(elems):
    if isinstance(elems, list):
        for elem in elems:
            if isinstance(elem, str):
                print(elem)
            else:
                print(etree.tostring(elem).decode('utf-8'))
    else:
        print(etree.tostring(elems).decode('utf-8'))
