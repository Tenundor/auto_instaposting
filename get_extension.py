def get_file_extension_from_url(url):
    extension_index = url.rindex(".")
    return url[extension_index + 1:]