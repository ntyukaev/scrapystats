
def name_file(url):
    return url.replace('https://', '')\
        .replace('?', '')\
        .replace('/', '_') + '.json'
