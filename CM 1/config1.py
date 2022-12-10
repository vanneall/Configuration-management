import zipfile
import os

def ls(arg):
    if arg[0] == "/":
        arg = arg[1:]
    
    flag = 0
    for file in file_zip.infolist():
        nameFile = file.filename
        if nameFile.__contains__(currentPath + arg):
            nameFile = file.filename[len(currentPath + arg):]
            if nameFile != "" and nameFile[0] == ".":
                break
            if (nameFile == nameFile[:nameFile.find('/') + 1] or nameFile.count('/') == 0) and nameFile != "":
                print(nameFile, end=" ")
                flag = 1
    if flag == 0:
        print("Такой директории не существует")

def pwd():
    print('/' + currentPath)

def cat(file):
    for filename in file_zip.namelist():
        if not os.path.isdir(filename):
            if filename.__contains__(currentPath):
                filename = filename[len(currentPath):]
                if filename == file:
                    with file_zip.open(currentPath + filename) as f:
                        for line in f:
                            print(line)


def cd(currentPath, arg):
    if arg == ".." and currentPath != "":
        currentPath = currentPath[:currentPath.rfind('/')]
        return currentPath[:currentPath.rfind('/')+1]
    elif arg == "/":
        return ""
    elif arg[0] == "/":
        for file in file_zip.infolist():
            if file.filename == arg[1:] and file.is_dir():
                return arg[1:]
    else:
        for file in file_zip.infolist():
            if file.filename == currentPath + arg + "/" and file.is_dir():
                return currentPath + arg + "/"
            elif file.filename == currentPath + arg and file.is_dir():
                return currentPath + arg
    print("Нет такого каталога")
    return currentPath


command = ""
path = input("Введите путь до архива >> ")
file_zip = zipfile.ZipFile(path, 'r')
currentPath = ""

while command != "break":
    command = input("/" + currentPath + "$ ").split(" ")

    if command[0] == "ls":
        if len(command) > 1:
            ls(command[1])
        else:
            ls("/")

    elif command[0] == "pwd":
       pwd()

    elif command[0] == "cat":
        if (len(command) == 1):
            print("Файл не выбран.")
        else:
            cat(command[1])

    elif command[0] == "cd":
        if (len(command) == 1):
            currentPath = ""
        elif command[1] == "":
            currentPath = ""
        else:
            currentPath = cd(currentPath, command[1])
    else:
        print("Команда <" + command[0] + "> не найдена.")
