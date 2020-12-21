import pandas as pd
from math import inf

def min_col(frame, col):
    min_d = inf
    for e in frame:
        min_d = min(e[col], min_d)
    return min_d

line = list()
singleElement = list()
tasks = dict()
number = -1
input_file = open('input.txt')

for line in input_file:
    singleElement = (line.split(','))
    number += 1
    for i in range(len(singleElement)):
        tasks['task' + str(singleElement[0])] = dict()
        tasks['task' + str(singleElement[0])]['id'] = singleElement[0]
        tasks['task' + str(singleElement[0])]['name'] = singleElement[0]
        tasks['task' + str(singleElement[0])]['duration'] = singleElement[1]
        if singleElement[2] != "\n":
            tasks['task' + str(singleElement[0])]['dependencies'] = singleElement[2].strip().split(';')
        else:
            tasks['task' + str(singleElement[0])]['dependencies'] = ['-1']
        tasks['task' + str(singleElement[0])]['ES'] = 0
        tasks['task' + str(singleElement[0])]['EF'] = 0
        tasks['task' + str(singleElement[0])]['LS'] = 0
        tasks['task' + str(singleElement[0])]['LF'] = 0
        tasks['task' + str(singleElement[0])]['float'] = 0
        tasks['task' + str(singleElement[0])]['isCritical'] = False

# =============================================================================
# Прямой ход
# =============================================================================
for taskFW in tasks:
    if '-1' in tasks[taskFW]['dependencies']:  # проверка если это 1я задача
        tasks[taskFW]['ES'] = 0
        tasks[taskFW]['EF'] = (tasks[taskFW]['duration'])
    else:
        for k in tasks.keys():
            for dep in tasks[k]['dependencies']:
                if dep != '-1' and len(tasks[k]['dependencies']) == 1:  # у задачи 1 зависимость
                    tasks[k]['ES'] = int(tasks['task' + dep]['EF'])
                    tasks[k]['EF'] = int(tasks[k]['ES']) + int(tasks[k]['duration'])
                elif dep != '-1':  # у задачи больше 1 зависимости
                    if int(tasks['task' + dep]['EF']) > int(tasks[k]['ES']):
                        tasks[k]['ES'] = int(tasks['task' + dep]['EF'])
                        tasks[k]['EF'] = int(tasks[k]['ES']) + int(tasks[k]['duration'])

aList = list()
for element in tasks.keys():
    aList.append(element)

bList = aList[:]
bList.reverse()

# =============================================================================
# Обратный ход
# =============================================================================
for taskBW in bList:
    if bList.index(taskBW) == 0:  # Если это последняя задача
        tasks[taskBW]['LF'] = tasks[taskBW]['EF']
        tasks[taskBW]['LS'] = tasks[taskBW]['ES']

    for dep in tasks[taskBW]['dependencies']:
        if dep != '-1':  # Если не последняя задача
            if tasks['task' + dep]['LF'] == 0:
                tasks['task' + dep]['LF'] = int(tasks[taskBW]['LS'])
                tasks['task' + dep]['LS'] = int(tasks['task' + dep]['LF']) - int(tasks['task' + dep]['duration'])
                tasks['task' + dep]['float'] = int(tasks['task' + dep]['LF']) - int(tasks['task' + dep]['EF'])
            if int(tasks['task' + dep]['LF']) > int(tasks[taskBW]['LS']):
                tasks['task' + dep]['LF'] = int(tasks[taskBW]['LS'])
                tasks['task' + dep]['LS'] = int(tasks['task' + dep]['LF']) - int(tasks['task' + dep]['duration'])
                tasks['task' + dep]['float'] = int(tasks['task' + dep]['LF']) - int(tasks['task' + dep]['EF'])
# =============================================================================
# PRINTING
# =============================================================================
id = []
data = {"Длительность задачи": [], "Раннее начало": [], "Ранний конец": []
    ,"Позднее начало":[],"Поздний конец":[], "Запас":[], "Крит. путь":[]}
for task in tasks:
    id.append(tasks[task]['id'])
    data["Длительность задачи"].append(tasks[task]['duration'])
    data["Раннее начало"].append(tasks[task]['ES'])
    data["Ранний конец"].append(tasks[task]['EF'])
    data["Позднее начало"].append((tasks[task]['LS']))
    data["Поздний конец"].append((tasks[task]['LF']))
    data["Запас"].append((tasks[task]['float']))
    data["Крит. путь"].append(tasks[task]['float'] == 0)

#data["Позднее начало"] = [0, 7, ]
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
    print(pd.DataFrame(data, index=id))
