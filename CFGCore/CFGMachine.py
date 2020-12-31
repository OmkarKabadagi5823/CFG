from CFG.CFGCore.CFGUtils import *
from CFG.CFGAlgorithms import CFGReductions

class CFGContainer():
    def __init__(self):
        self.terminals = set()
        self.nonTerminals = set()
        self.productions = dict()
        self.start = ''

class CFGMachine():
    def __init__(self):
        self.initProperties()
    
    def initProperties(self):
        self.container = CFGContainer() 
        self.buffer = CFGContainer()
    
    def readCFG(self, file):
        f = open(file, 'r')
        self.container.start = CFGFileParser.startParser(f.readline())
        self.container.terminals = CFGFileParser.terminalsParser(f.readline())
        self.container.productions = CFGFileParser.productionsParser(f.readline())
        self.container.nonTerminals = findNonTerminals(self.container.terminals, self.container.productions)
        f.close()
        self.bufferReset()

    def bufferReset(self):
        self.buffer.terminals = self.container.terminals.copy()
        self.buffer.nonTerminals = self.container.nonTerminals.copy()
        self.buffer.productions = self.container.productions.copy()
        self.buffer.start = self.container.start

    def save(self):
        self.container.terminals, self.container.nonTerminals, self.container.productions, self.container.start = \
            self.buffer.terminals.copy(), self.buffer.nonTerminals.copy(), self.buffer.productions.copy(), self.buffer.start
    
    def summary(self):
        print("{}".format(Format.underline("CFG:-")))
        print("{}: {}".format(Format.bold("Terminals"), self.container.terminals))
        print("{}: {}".format(Format.bold("Non-Terminals"), self.container.nonTerminals))
        print("{}: {}".format(Format.bold("Start"), self.container.start))
        print("{}:".format(Format.bold("Productions")))
        CFGPrinter.productionsPrinter(self.container.productions)

    def bufferSummary(self, msg):
        print("{}".format(Format.underline(msg)))
        print("{}: {}".format(Format.bold("Terminals"), self.buffer.terminals))
        print("{}: {}".format(Format.bold("Non-Terminals"), self.buffer.nonTerminals))
        print("{}: {}".format(Format.bold("Start"), self.buffer.start))
        print("{}:".format(Format.bold("Productions")))
        CFGPrinter.productionsPrinter(self.buffer.productions)

    def eliminateStartRhs(self, output=False):
        self.bufferReset()
        CFGReductions. eliminateStartRhs(self.buffer)
        if(output):
            self.bufferSummary("Eliminate start from RHS:")

    def removeNullable(self, output=False):
        self.bufferReset()
        CFGReductions.removeNullable(self.buffer)
        if(output):
            self.bufferSummary("Remove null productions:")
    
    def removeUnitProductions(self, output=False):
        self.bufferReset()
        CFGReductions.removeUnitProductions(self.buffer)
        if(output):
            self.bufferSummary("Remove unit productions:")

    def removeNonTerminating(self, output=False):
        self.bufferReset()
        CFGReductions.removeNonTerminating(self.buffer)
        if(output):
            self.bufferSummary("Remove non-terminating productions:")

    def removeNonSentential(self, output=False):
        self.bufferReset()
        CFGReductions.removeNonSentential(self.buffer)
        if(output):
            self.bufferSummary("Remove non-sentential productions:")