def findNonTerminals(terminals, productions):
        nonTerminals = []

        for lhs in productions:
            if lhs not in terminals:
                nonTerminals.append(lhs)
            for production in productions[lhs]:
                for character in production:
                    if character not in terminals:
                        nonTerminals.append(character)
        
        return set(sorted(nonTerminals))

def removeDuplicates(productions):
    productionsList = []
    for lhs in productions:
        for production in set(productions[lhs]):
            productionsList.append([lhs, production])
    
    return Convert.listToDict(productionsList)

class CFGFileParser():
    @staticmethod
    def startParser(line):
        return line.replace(" ", "").replace("\n", "").replace("\r", "")

    @staticmethod
    def terminalsParser(line):
        return set(sorted(line.replace(" ", "").replace("\n", "").replace("\r", "").split(",")))
    
    @staticmethod
    def productionsParser(line):
        productionsList = line.replace(" ", "").replace("\n", "").replace("\r", "").split(",")
        productions = dict()
        nonTerminals = []
        for index in range(len(productionsList)):
            production = productionsList[index].split('->')
            productions.update({production[0]: production[1].split('|')})

        return productions
    
class Convert():
    @staticmethod
    def listToDict(productionsList):
        productions = dict()
        for production in productionsList:
            if production[0] in productions.keys():
                productions[production[0]].append(production[1])
            else:
                productions[production[0]] = [production[1]]
        
        return productions

    @staticmethod 
    def DictToList(productions):
        productionsList = []
        for lhs in productions:
            for production in productions[lhs]:
                productionsList.append([lhs, production])
        
        return productionsList

class CFGPrinter():
    @staticmethod
    def productionsPrinter(productions):
        keyList = productions.keys()
        for value in keyList:
            counter = 0
            rule = value + ' -> '
            length = len(productions[value])
            for itr in productions[value]:
                counter += 1
                if(length > 1 and counter < length):
                    rule = rule + itr + ' | '
                else:
                    rule = rule + itr
            
            print("{}".format(rule))

class Formater():
    @staticmethod
    def bold(str):
        return "\033[1m" + str + "\033[0m"
    
    @staticmethod
    def underline(str):
        return "\033[4m" + str + "\033[0m"
