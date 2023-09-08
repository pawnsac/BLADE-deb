def write(content,file):
    with open(file, 'w+') as f:
        f.write('\n'.join(content))
    f.close()
