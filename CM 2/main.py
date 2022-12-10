import graphviz
import requests

packages = []  # инициализация массива который будет хранить все пакеты

Name = ""  # имя основного пакета

# блеклист пакетов (очень большое дерево у них)
packages_blacklist = ["six", "boto3-stubs", "wheel", "attrs", "mypy", "hypothesis", "pytest", "sphinx", "html5lib",
                      "furo",
                      "setuptools", "virtualenv", "backports-functools-lru-cache", "zope", "rich", "pep517",
                      "ipython",
                      "twisted", "pyparsing", "scipy", "numbagg", "scanpydoc", "fsspec"]


# убираем мусор из названия пакета
def getPackageName(requirement: str) -> str:
    for i in range(1, len(requirement)):
        if not (requirement[i].isalnum() or requirement[i] == "-" or requirement[i] == "_" or requirement[i] == "."):
            return requirement[:i]
    return requirement


def getDependencies(packageName):
    if len(packages) >= 16:
        return

    json1 = requests.get(f"https://pypi.org/pypi/{packageName}/json").json()

    # пробуем спарсить
    try:
        requirements = json1["info"]["requires_dist"]
    except:
        print("Пакет " + packageName + " не найден!!")
        return

    # Если нет наследований - выходим
    if not requirements:
        return

    # убираем мусор из названия пакета
    for i in range(len(requirements)):
        if requirements[i].__contains__(" "):
            requirements[i] = requirements[i][:requirements[i].find(" ")]
        elif requirements[i].__contains__(">"):
            requirements[i] = requirements[i][:requirements[i].find(">")]
        elif requirements[i].__contains__("~"):
            requirements[i] = requirements[i][:requirements[i].find("~")]

    requirements = set(requirements)

    # заносим пакеты в конечный массив
    for key in requirements:
        if packageName + " " + key not in packages:
            packages.append(packageName + " " + key)
            if key not in packages_blacklist:
                getDependencies(key)


# создание графа
def make_graph(graph):
    for package in packages:
        arr = package.split()
        if (len(arr) == 2): graph.edge(arr[0], arr[1])


# функция проверки графа на пустоту
def isEmpty(graph):
    count = 0
    for i in graph:
        count += 1
        if (count == 2): return False
    return True



print("Введите название пакета:", end=' ')
Name = "scikit-learn"
if len(Name) != 0:
    if (getDependencies(Name) != False):
        graph = graphviz.Digraph('Dependencies')  # создаем направленный граф с именем Dependencies
        graph.node(Name)
        packages.append(Name)
        if not isEmpty(graph):
            # формируем граф
            make_graph(graph)
            graph.render(filename=Name + "2.gv")  # сохраняем граф в формате gv
        print("Граф зависимостей пакета " + Name + " сохранен в " + Name + ".gv")