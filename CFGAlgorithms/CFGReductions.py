from CFG.CFGCore.CFGUtils import Convert, findNonTerminals, removeDuplicates

class CFGReductions():
	## REMOVE START FROM RHS
	@staticmethod
	def eliminateStartRhs(cfg):
		flag = 0
		for lhs in cfg.productions:
			for production in cfg.productions[lhs]:
				for character in production:
					if character==cfg.start:
						flag = 1
						break
		
		if flag:
			cfg.productions.update({'#' : [cfg.start]})
			cfg.start = '#'

	## REMOVE NULLABLE
	@staticmethod
	def _recursiveFindNullable(terminals, productions,  nullable):
		nullableBefore = nullable.copy()
		for lhs in productions:
			for production in productions[lhs]:
				for character in production:
					if character in nullable:
						nullable.add(lhs)

		if nullableBefore == nullable:
			return nullable
		else:
			return CFGReductions._recursiveFindNullable(terminals, productions,  nullable)
		
	@staticmethod
	def _check(production, productionEmpty, index, replacement):
		if replacement == "$" or replacement == production[index]:
			return True
		else:
			return False

	@staticmethod
	def _recursiveReplace(production, productionEmpty, permutationList, replace, start):
		index = productionEmpty.find('_')
		if(index == -1):
			permutationList.append(productionEmpty)
			return 0, permutationList

		for replacement in replace:
			if(CFGReductions._check(production, productionEmpty, index, replacement)):
				productionEmpty = productionEmpty[:index] + \
					replacement + productionEmpty[index+1:]
				flag, permutationList = CFGReductions._recursiveReplace(
					production, productionEmpty, permutationList, replace, start)
				if(flag):
					return 1, permutationList
				productionEmpty = productionEmpty[:index] + '_' + productionEmpty[index+1:]

		if(index == start):
			return 1, permutationList

		return 0, permutationList

	@staticmethod
	def removeNullable(cfg):
		productionsList = []
		nullable = set({'$'})
		nullable = CFGReductions._recursiveFindNullable(cfg.terminals, cfg.productions,  nullable)
		nullable.remove('$')
		if cfg.start in nullable:
			nullable.remove(cfg.start)
		for lhs in cfg.productions:
			for production in cfg.productions[lhs]:
				replace = set(['$'])
				productionEmpty = production[:]
				permutationList = []
				for index in range(len(production)):
					if(production[index] in nullable):
						replace.add(production[index])
						productionEmpty = productionEmpty[:index] + \
							'_' + productionEmpty[index+1:]

				start = productionEmpty.find('_')
				_, permutationList = CFGReductions._recursiveReplace(
					production, productionEmpty, permutationList, replace, start)
				for production in permutationList:
					production = production.replace('$', '')
					if production != '':
						productionsList.append([lhs, production])
		
		cfg.productions = removeDuplicates(Convert.listToDict(productionsList))

	## REMOVE UNIT PRODUCTIONS	
	@staticmethod
	def _recursiveRemoveUnitProductions(lhs, unitRhs, productions, terminals):
		rhs = []
		if unitRhs in productions.keys():
			for production in productions[unitRhs]:
				if len(production) == 1 and production[0] not in terminals and unitRhs != production[0]:
					rhs.extend(CFGReductions._recursiveRemoveUnitProductions(unitRhs, production[0], productions, terminals))
				elif len(production) == 1 and production[0] not in terminals and unitRhs != production[0]:
					continue
				else:
					rhs.append(production)
		return rhs
	
	@staticmethod
	def removeUnitProductions(cfg):
		productionsList = []
		for lhs in cfg.productions:
			for production in cfg.productions[lhs]:
				if len(production) == 1 and production[0] not in cfg.terminals and lhs != production[0]:
					rhsList = CFGReductions._recursiveRemoveUnitProductions(lhs, production[0], cfg.productions, cfg.terminals)
					for rhs in rhsList:
						productionsList.append([lhs, rhs])
				elif len(production) == 1 and production[0] not in cfg.terminals and lhs == production[0]:
					continue
				else:
					productionsList.append([lhs, production])

		cfg.productions = removeDuplicates(Convert.listToDict(productionsList))		

	## REMOVE NON-TERMINATING
	@staticmethod
	def _VnGenerator(w, alpha, productions):
		wBefore = w.copy()
		for lhs in productions:
			for production in productions[lhs]:
				flag = 0
				for character in production:
					if character not in alpha:
						flag = 1
				if not flag:
					w.add(lhs)
		alpha.update(w)
		if(wBefore == w):
			return w, alpha
		else:
			return CFGReductions._VnGenerator(w, alpha, productions)

	@staticmethod
	def _filterProductions(alpha, productions):
		productionsList = []
		for lhs in productions:
			if lhs not in alpha:
				continue
			for production in productions[lhs]:
				flag = 0
				for character in production:
					if character not in alpha:
						flag = 1
						break
				if not flag:
					productionsList.append([lhs, production])
		
		return productionsList

	@staticmethod
	def removeNonTerminating(cfg):
		cfg.nonTerminals = set()
		alpha = cfg.terminals.copy()
		cfg.nonTerminals, alpha = CFGReductions._VnGenerator(cfg.nonTerminals, alpha, cfg.productions)
		productionsList = CFGReductions._filterProductions(alpha, cfg.productions)

		cfg.productions = removeDuplicates(Convert.listToDict(productionsList))

	## REMOVE NON-SENTENTIAL
	@staticmethod
	def _setBuilder(terminals, w1, productions):
		for itr in productions:
			lhs = itr[0]
			rhs = itr[1]
			if(lhs in w1):
				for values in rhs:
					temp = []
					temp[:] = values
					for x in temp:
						if(x not in w1):
							w1.add(x)
		return w1

	@staticmethod
	def _productionBuilder(wn, productions):
		productionsList = []
		for itr in productions:
			if(itr[0] in wn):
				productionsList.append([itr[0], itr[1]])
		return productionsList
	
	@staticmethod
	def removeNonSentential(cfg):
		w1 = set()
		w1.add(cfg.start)
		wn = CFGReductions._setBuilder(cfg.terminals, w1, Convert.DictToList(cfg.productions))
		productionsList = CFGReductions._productionBuilder(wn, Convert.DictToList(cfg.productions))

		cfg.productions = removeDuplicates(Convert.listToDict(productionsList))
		

