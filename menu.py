"""
Menu.py coded by Aaron Gold
April 18th 2023
This program asks the user for categories of food, and customizes a menu off of their request.
"""
import os


#Takes in file, converts to category list and item/price dictionary
def readDescriptions(descFileName, dataFolderName="data"):
    menu = {}
    category_name = ""
    temp_list, category_list = [], []
    f = open(os.path.join(dataFolderName, descFileName), 'r')
    for line in f:
        if ',' not in line:
            category_name = line[:-1].lower()
            category_list.append(category_name)
            temp_list.clear()
        else:
            word_list = line.replace('"', '').strip().split(",")
            print(word_list)
            temp_list.append(word_list[0])
            for j in range(len(temp_list)):
                menu[word_list[0]] = (category_name, word_list[1].lower(), float(word_list[2]))

    return menu, category_list


#Reads order files and computes total amount of each order
def summaryFromFiles(dataFolderName, prefix):
    numOrders = 0
    dictOrders = {}
    for filename in os.listdir(dataFolderName):
        if filename.startswith(prefix):
            numOrders += 1
            with open(os.path.join(dataFolderName, filename), 'r') as f:
                for line in f:
                    ord_list = line.strip().split(" ")
                    orderKey = ord_list[0]
                    numOrders = int(ord_list[-1])
                    if orderKey in dictOrders.keys():
                        dictOrders[orderKey] += numOrders
                    else:
                        dictOrders[orderKey] = numOrders
    return dictOrders


#Creates groupings of total orders and sorts them by most total ordered
def dictToOrderedReversedTuples(dictCounts):
    tupleList = []
    for i in range(len(dictCounts)):
        tupleKey = list(dictCounts.keys())[i]
        tupleValue = list(dictCounts.values())[i]
        tuplePair = (tupleValue, tupleKey)
        tupleList.append(tuplePair)
    tupleList.sort(reverse=True)
    return tupleList


#Checks that all inputs are categories, prints top items from each category on menu
def printTop3(dictMenu, dictOrders, chosenCategories, totalCategories):
    tupleList = dictToOrderedReversedTuples(dictOrders)
    wrongList, correctList = [], []

    category_list = chosenCategories.strip().split(", ")
    for cat in category_list:
        if cat in totalCategories:
            correctList.append(cat)
        else:
            wrongList.append(cat)
    for c in correctList:
        items_printed = 0
        print(f"{'--------------------':<20} {c:^15}{'--------------------':>20}")
        for t in tupleList:
            if c == dictMenu[t[1]][0] and items_printed < 3:
                print("\t\t", f'{dictMenu[t[1]][1]: <30} ${dictMenu[t[1]][2]:<10.2f}')
                items_printed += 1
    if len(wrongList) > 0:
        print("We omitted the following categories you requested, because they are not on the menu: ")
        for w in wrongList:
            print("\t", w)
        print("The categories on the menu are: ")
        for t in totalCategories:
            print("\t", t)


def main():
    print("This program will create a menu of top three most requested dishes per each of"
          " your specified categories, based on restaurant menu and data on recent orders. ")
    datafoldername = input("Please enter the name of the folder with data files or press enter for 'data': ").lower()
    descfilename = 'menuitems.txt'
    if datafoldername == '':
        datafoldername = 'data'
    menuDict, categories = readDescriptions(descfilename, datafoldername)
    ordDict = summaryFromFiles(datafoldername, 'ord')
    print("Found menu categories: ", (', '.join(categories)))
    top3Categories = input("Please enter categories you'd like to include in the Top-3 menu, separated with commas: ").lower()
    printTop3(menuDict, ordDict, top3Categories, categories)
main()
