# The Simp Game

# Buildings
# ---------------------- #
# Beach (BCH) , Factory (FAC) , House (HSE) , Shop (SHP) , Highway (HWY)

# Board
# ---------------------- #
# [['A1','B1','C1','D1'],
#  ['A2','B2','C2','D2'],
#  ['A3','B3','C3','D3'],
#  ['A4','B4','C4','D4']]

# Game Options
# -----------------------#
# 6 Options
# 1. Place Random Building
# 2. Place Random Building
# 3. See remaining buildings
# 4. See current score

# 5. Save game
# 0. Exit to main menu

# Imports

# for mapping locations to buildings
plots = {"A1": "\t", "A2": "\t", "A3": "\t", "A4": "\t", "B1": "\t",
         "B2": "\t", "B3": "\t", "B4": "\t", "C1": "\t", "C2": "\t",
         "C3": "\t", "C4": "\t", "D1": "\t", "D2": "\t", "D3": "\t",
         "D4": "\t", "Turn": "0", "lastPlace": ""}
locationDic = {"A1": ["A2", "B1"],
               "A2": ["A1", "A3", "B2"],
               "A3": ["A2", "A4", "B3"],
               "A4": ["A3", "B4"],
               "B1": ["A1", "B2", "C1"],
               "B2": ["A2", "B1", "B3", "C2"],
               "B3": ["A3", "B2", "B4", "C3"],
               "B4": ["A4", "B3", "C4"],
               "C1": ["B1", "C2", "D1"],
               "C2": ["B2", "C1", "C3", "D2"],
               "C3": ["B3", "C2", "C4", "D3"],
               "C4": ["B4", "C3", "D4"],
               "D1": ["C1", "D2"],
               "D2": ["C2", "D1", "D3"],
               "D3": ["D2", "D4", "C3"],
               "D4": ["D3", "C4"]}
buildings = {0: "BCH", 1: "FAC", 2: "HSE", 3: "SHP", 4: "HWY"}
hseScoreDic = {"FAC": 1, "BCH": 2, "HSE": 1, "SHP": 1}
houseHis = [] 
beachHis= []
factoryScoreHis = [] 
shopScoreHis = [] 
highwayScoreHis = []

bchCount = 8
facCount = 8
hseCount = 8
shpCount = 8
hwyCount = 8
lastPlace = ""  # stores last plot built upon


# module displays game/city grid
def CityMapFunc():
    print("\t     A \t     B \t     C \t     D")
    for i in range(4):
        print("\t   --------------------------------")
        if i == 0:
            print("\t", i + 1, "| ", plots["A1"], " | ", plots["B1"],
                  " | ", plots["C1"], " |", plots["D1"], "  | ")
        if i == 1:
            print("\t", i + 1, "| ", plots["A2"], " | ", plots["B2"],
                  " | ", plots["C2"], " |", plots["D2"], "  | ")
        if i == 2:
            print("\t", i + 1, "| ", plots["A3"], " | ", plots["B3"],
                  " | ", plots["C3"], " |", plots["D3"], "  | ")
        if i == 3:
            print("\t", i + 1, "| ", plots["A4"], " | ", plots["B4"],
                  " | ", plots["C4"], " |", plots["D4"], "  | ")

    print("\t   --------------------------------")


# function for main menu
def MenuSelection(option):

    FirstMenu()
    option = (int)(input("Your choice? "))
    MenuSelection(option)
    if option == 1:
        StartGameFunc()
    elif option == 2:
        LoadGameFunc()
    elif option == 0:
        exit(0)
    else:
        print("invalid option, try again")


# module returns a list of adjacent locations to the function parameter
def CheckAdjacency(loc):
    if(loc in locationDic.keys()):
        return locationDic.get(loc)
    else:
        raise ValueError('Unexpected location')


# Functions to calculate scores
# calculate BCH score
def calculateBCHscore(place):
    placeSplit = list(place)
    row = placeSplit[0]
    col = placeSplit[1]
    rowLeft = list(plots.keys())[0][0]
    rowRight = list(plots.keys())[-3][0]

    if (row == rowLeft or row == rowRight):
        return 3
    else:
        return 1


# calculate factory score
def calculateFACscore(factoryNumber):

    if (isinstance(factoryNumber, int)):
        if factoryNumber < 5:
            factoryScoreHis = [factoryNumber for i in range(factoryNumber)]
            return factoryNumber * factoryNumber
        else:
            factoryNumber = factoryNumber - 4
            factoryScoreHis = [4 for i in range(4)]
            factoryScoreHis.append([1 for i in range(factoryNumber)])
            return factoryNumber
    else:
        raise TypeError('Invalid Data Type')


def calculateSHPscore(adjacencylist, plots):
    fcount = 0
    bcount = 0
    scount = 0
    hcount = 0
    shopScore = 0

    for item in adjacencylist:
        if plots[item] == "FAC":
            if fcount == 1:
                break
            shopScore = shopScore + 1
            fcount = fcount + 1
        elif plots[item] == "BCH":
            if bcount == 1:
                break
            shopScore = shopScore + 2
            bcount = bcount + 1
        elif plots[item] == "HSE":
            if hcount == 1:
                break
            shopScore = shopScore + 1
            hcount = hcount + 1
        elif plots[item] == "SHP":
            if scount == 1:
                break
            shopScore = shopScore + 1
            scount = scount + 1
    return shopScore


def calculateHSEscore(plots, item):
    if (plots[item] in hseScoreDic.keys()):
        return hseScoreDic.get(plots[item])
    else:
        return 0


def calculateHWYscore(adjacencylist, plots):
    for item in adjacencylist:
        if plots[item] == "HWY":
            return 1
            print("Highway Score + 1")
    return 0


def printScoreHis(history):
    for i in range(len(history)):
        print(history[i], end=" ")
        if(i != len(history)):
            print("+", end=" ")


# function incorportes scoring logic for all types of buildings
def ScoreAdjacentBuildings(plots):
    TLScore, houseScore, beachScore, factoryScore, shopScore, highwayScore = 0
    global houseHis, beachHis, factoryScoreHis, shopScoreHis, highwayScoreHis

    factoryNumber = 0

    for place, build in plots.items():
        if build == "BCH":
            score = calculateBCHscore(place)
            beachScore = beachScore + score
            beachHis.append(score)

        if build == "FAC":
            factoryNumber = factoryNumber + 1
        if build == "HSE":
            adjacencylist = CheckAdjacency(place)
            for item in adjacencylist:
                score = calculateHSEscore(plots, item)
                houseScore = houseScore + score
                houseHis.append(score)

        if build == "SHP":
            adjacencylist = CheckAdjacency(place)
            score = calculateSHPscore(adjacencylist, plots)
            shopScore = shopScore + score
            shopScoreHis.append(score)
        if build == "HWY":
            adjacencylist = CheckAdjacency(place)
            score = calculateHWYscore(adjacencylist, plots)
            highwayScore = highwayScore + score
            highwayScoreHis.append(score)

    factoryScore = calculateFACscore(factoryNumber)

    print("BCH : ", printScoreHis(beachHis) + " = " + beachScore)
    print("FAC : ", printScoreHis(factoryScoreHis) + " = " + factoryScore)
    print("HSE : ", printScoreHis(houseHis) + " = " + houseScore)
    print("SHP : ", printScoreHis(shopScoreHis) + " = " + shopScore)
    print("HWY : ", printScoreHis(highwayScoreHis) + " = " + highwayScore)

    TLScore = beachScore + factoryScore + houseScore + shopScore + highwayScore
    print("Total Score = ", TLScore)


def FirstMenu():
    print("Welcome, mayor of Simp City!")
    print("------------------------------")
    print("1- Start new game")
    print("2- Load saved game")
    print("0- Exit")


def StartGameFunc():
    print("start")


def LoadGameFunc():
    print("load")
