def compare_version(version1, version2):
    list1 = str(version1).split(".")
    list2 = str(version2).split(".")
    print(list1)
    print(list2)
    # 循环次数为短的列表的len
    for i in range(len(list1)) if len(list1) < len(list2) else range(len(list2)):
        if int(list1[i]) == int(list2[i]):
            pass
        elif int(list1[i]) < int(list2[i]):
            return -1
        else:
            return 1
    # 循环结束，哪个列表长哪个版本号高
    if len(list1) == len(list2):
        return 0
    elif len(list1) < len(list2):
        return -1
    else:
        return 1



if __name__ == '__main__':
    value1 = compare_version("1.2.3", "1.2.03.1")
    value2 = compare_version("1.2.3", "1.2.03")
    value3 = compare_version("1.2.3", "1.2.01")
    value4 = compare_version("1.2.3.1", "1.2.03")
    print(value1)
    print(value2)
    print(value3)
    print(value4)
