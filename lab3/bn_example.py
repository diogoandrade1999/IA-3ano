
from bayes_net import *

# Exemplo dos acetatos:

bn = BayesNet()

bn.add('st',[],0.600)
bn.add('pt',[],0.050)

bn.add('cp',[('st',True ),('pa',True )],0.020)
bn.add('cp',[('st',True ),('pa',False)],0.010)
bn.add('cp',[('st',False),('pa',True )],0.011)
bn.add('cp',[('st',False),('pa',False)],0.001)

bn.add('cnl',[('st',True )],0.900)
bn.add('cnl',[('st',False)],0.001)

bn.add('pa',[('pt',True )],0.250)
bn.add('pa',[('pt',False)],0.004)

bn.add('ur',[('pt',True )],0.900)
bn.add('ur',[('pt',False),('pa',True )],0.100)
bn.add('ur',[('pt',False),('pa',False)],0.010)

print(bn.indivProb('pa', True))
print(bn.indivProb('ur', True))
'''
conjunction = [('j',True),('m',True),('a',True),('r',False),('t',False)]

print(bn.jointProb(conjunction))
'''
