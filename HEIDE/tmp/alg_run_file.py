import sys
import ast
sys.path.append('../../PyHE/')
from PyHE import PyHE
from PyPtxt import PyPtxt
from PyCtxt import PyCtxt
_set_ = lambda c: c.set()
def run_heide_alg(RUN_PARAMS, DATA):
	HE = PyHE()
	HE.keyGen(RUN_PARAMS)

	for key in DATA:
		DATA[key] = PyPtxt(DATA[key], HE)

	for key in DATA:
		DATA[key] = HE.encrypt(DATA[key])
	
	
	l = len(DATA)
	for i in range(l - 1):
		ctxt_res = DATA[DATA.keys()[i]] + DATA[DATA.keys()[i+1]]
	
	print(HE.decrypt(ctxt_res))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


if __name__ == '__main__':
	run_heide_alg(ast.literal_eval(sys.argv[1]), 
			ast.literal_eval(sys.argv[2]))
