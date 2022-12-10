import functions

directory = input("Введите путь до директории с объектами (пример: test/.git/objects/): ")
if directory[-1] != '/':
    directory += '/'
if functions.checkPath(directory):
    functions.graph(directory)

