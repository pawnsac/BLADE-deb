def remove_lines(file, addr):
    output = file.copy()
    if addr[0] == addr[2]:
        line = output[addr[0] - 1]
        line = list(line)
        line[addr[1] - 1 : addr[3]] = " " * (addr[3] - addr[1] + 1)
        line = "".join(line)
        output[addr[0] - 1] = line
    else:
        start = True
        for i in range(addr[0] - 1, addr[2]):
            line = output[i]
            line = list(line)
            if start:
                line[addr[1] - 1 :] = " " * (len(line) - addr[1])
                start = False
            elif i == addr[2] - 1:
                line[: addr[3]] = " " * (addr[3])
            else:
                line = " " * len(line)
            line = "".join(line)
            output[i] = line
    return output


def restore_lines(output, original_doc, addr):
    output = output.copy()
    if addr[0] == addr[2]:
        line = output[addr[0] - 1]
        line = list(line)
        line[addr[1] - 1 : addr[3]] = original_doc[addr[0] - 1][addr[1] - 1 : addr[3]]
        line = "".join(line)
        output[addr[0] - 1] = line
    else:
        start = True
        for i in range(addr[0] - 1, addr[2]):
            line = output[i]
            line = list(line)
            if start:
                line[addr[1] - 1 :] = original_doc[i][addr[1] - 1 :]
                start = False
            elif i == addr[2] - 1:
                line[: addr[3]] = original_doc[i][: addr[3]]
            else:
                line = original_doc[i]
            line = "".join(line)
            output[i] = line
    return output
