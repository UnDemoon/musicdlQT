import json

'''从json文件获取指定key'''


def loadKeyJsonFile(file: str, key: str = None):
    with open(file, 'r', encoding='utf-8') as f:
        try:
            conf_dict = json.load(f)
        except Exception as e:
            conf_dict = None
            print(e)
    if key:
        res = conf_dict.get(key)
    else:
        res = conf_dict
    return res


'''全覆盖写入文件'''


def writeOver(file: str, content: str):
    with open(file, 'w+', encoding='utf-8') as f:
        f.write(content)
