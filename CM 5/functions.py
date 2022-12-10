import os
import zlib
import graphviz
import time

graph = []

fileMessages = dict()
folders = list()


def checkPath(directory: str):
    if os.path.exists(directory):
        print("Найдена директория " + directory + "...")
        return True
    else:
        print("Директория " + directory + " не найдена")
        return False


def fillFoldersAndMessages(directory: str):
    temps = list()
    for folder in os.listdir(directory):
        temp = []
        if folder == 'info' or folder == 'pack':
            break
        folders.append(folder)
        for file in os.listdir(directory + folder):
            temps.append(folder + file)
            temp.append(file)
        folders.append(temp)
    for folder in temps:
        c = zlib.decompress(open(directory + folder[:2] + '/' + folder[2:], 'rb').read())
        if c.__contains__(b'blob'):
            c = c[c.find(b'\x00') + 1:c.rfind(b'\n')]
            fileMessages[c] = folder
    time.sleep(1)


createdNodes = []


def getMessage(fileName):
    time.sleep(1)
    print("\t\tСчитывание содержимого файла " + fileName + "...")
    file = open("test/" + fileName, 'rb').read()
    file = file.replace(b'\n', b'')
    message = file.decode('utf-8')
    hash = fileMessages[file]
    for nodes in createdNodes:
        if nodes == fileName + " " + hash[:5] + "\n'" + message + "'":
            return
    else:
        graph.append(fileName + " " + hash[:5] + "\n'" + message + "'")
        createdNodes.append(fileName + " " + hash[:5] + "\n'" + message + "'")


def createTree(code: str, directory: str):
    time.sleep(1)
    print("\tФормирование дерева " + code[5:10] + ":")
    info = zlib.decompress(open(directory + code[5:7] + '/' + code[7:], 'rb').read())
    info = info.split(b' ')
    temparray = []
    for i in range(0, len(info)):
        if info[i].__contains__(b'\x00'):
            info[i] = info[i][:info[i].find(b'\x00')]
        if info[i].__contains__(b'\xdd'):
            info[i] = info[i][:info[i].find(b'\xdd')]
        if not (info[i].decode('utf-8').isdigit() or info[i].decode('utf-8') == "tree") and len(info[i]) > 1:
            temparray.append(info[i].decode('utf-8'))
    for a in temparray:
        graph.append(code[0:10] + " " + a)
        if a == "bak":
            print("\t\tСчитывание bak...")
            time.sleep(1)
            continue
        else:
            getMessage(a)
    time.sleep(1)
    print("\tДерево " + code[5:10] + " удачно сформировано!\n")


def start(directory: str):
    fillFoldersAndMessages(directory)
    isGraphEmpty = True
    MY_GRAPH = graphviz.Digraph('Trees of a package')
    parrent = ""
    root = ""
    time.sleep(1)
    print("Начато формирование графа...")
    for i in range(0, len(folders), 2):
        folder = folders[i]
        for name in folders[i + 1]:
            content = zlib.decompress(open(directory + folder + '/' + name, 'rb').read())
            if content.__contains__(b'commit'):
                messageInCommit = list[list[str]]
                for s in content.decode().split('\n'):
                    messageInCommit = [s.split(' ')]
                for message in messageInCommit:
                    if message[0] == '':
                        messageInCommit.remove(message)
                    for i in range(0, len(message), 1):
                        if message[i].find('tree') != -1:
                            temp = message[i]
                            temp = temp[temp.find('tree'):]
                            message[i] = temp
                message = messageInCommit[-1]
                b = []
                for msg in message:
                    b.append(msg)
                message.clear()
                message.append('message')
                for msg in b:
                    message.append(msg)
                info = dict()
                for message in messageInCommit:
                    temp = message[0]
                    text = ""
                    for i in range(1, len(message), 1):
                        text += message[i] + ' '
                    if temp == "message":
                        info[temp] = text + "\n" + folder + name[:4]
                    else:
                        info[temp] = text
                if isGraphEmpty:
                    MY_GRAPH.node(info['message'])
                    isGraphEmpty = False
                info.pop('author')
                info.pop('committer')
                print(info['message'].split('\n')[0])
                MY_GRAPH.edge(info['message'], info['commit'][0:10])
                createTree(info['commit'], directory)
                if parrent != "":
                    if len(info) == 3:
                        MY_GRAPH.edge(parrent, info['message'])
                    else:
                        root = info['message']
                if len(info) == 3:
                    parrent = info['message']
                else:
                    root = info['message']
    MY_GRAPH.edge(parrent, root)
    for message in graph:
        arr = message.split(' ')
        if arr[0] != "tree":
            MY_GRAPH.edge(arr[0], arr[1] + " " + arr[2])
        else:
            MY_GRAPH.edge(arr[0] + " " + arr[1], arr[2])
    MY_GRAPH.render(filename="graph.gv")
    time.sleep(1)
    print("Граф сформирован")