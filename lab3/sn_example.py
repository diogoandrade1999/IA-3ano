



# Redes semanticas
# -- Exemplo
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2018
# 2018/10/22
#


from semantic_network import *

a = Association('socrates','professor','filosofia')
s = Subtype('homem','mamifero')
m = Member('socrates','homem')

da = Declaration('descartes',a)
ds = Declaration('darwin',s)
dm = Declaration('descartes',m)

z = SemanticNetwork()
z.insert(da)
z.insert(ds)
z.insert(dm)
z.insert(Declaration('darwin',Association('mamifero','mamar','sim')))
z.insert(Declaration('darwin',Association('homem','gosta','carne')))

# novas declaracoes

z.insert(Declaration('darwin',Subtype('mamifero','vertebrado')))
z.insert(Declaration('descartes', Member('aristoteles','homem')))

b = Association('socrates','professor','matematica')
z.insert(Declaration('descartes',b))
z.insert(Declaration('simao',b))
z.insert(Declaration('simoes',b))

z.insert(Declaration('descartes', Member('platao','homem')))

e = Association('platao','professor','filosofia')
z.insert(Declaration('descartes',e))
z.insert(Declaration('simao',e))

z.insert(Declaration('descartes',Association('mamifero','altura',1.2)))
z.insert(Declaration('descartes',Association('homem','altura',1.75)))
z.insert(Declaration('simao',Association('homem','altura',1.85)))
z.insert(Declaration('darwin',Association('homem','altura',1.75)))

z.insert(Declaration('descartes', Association('socrates','peso',80)))
z.insert(Declaration('darwin', Association('socrates','peso',75)))
z.insert(Declaration('darwin', Association('platao','peso',75)))


z.insert(Declaration('damasio', Association('filosofo','gosta','filosofia')))
z.insert(Declaration('damasio', Member('socrates','filosofo')))


# Extra - descomentar as restantes declaracoes para o exercicio II.2.16

z.insert(Declaration('descartes', AssocNum('socrates','pulsacao',51)))
z.insert(Declaration('darwin', AssocNum('socrates','pulsacao',61)))
z.insert(Declaration('darwin', AssocNum('platao','pulsacao',65)))

z.insert(Declaration('descartes',AssocNum('homem','temperatura',36.8)))
z.insert(Declaration('simao',AssocNum('homem','temperatura',37.0)))
z.insert(Declaration('darwin',AssocNum('homem','temperatura',37.1)))
z.insert(Declaration('descartes',AssocNum('mamifero','temperatura',39.0)))

z.insert(Declaration('simao',Association('homem','gosta','carne')))
z.insert(Declaration('darwin',Association('homem','gosta','peixe')))
z.insert(Declaration('simao',Association('homem','gosta','peixe')))
z.insert(Declaration('simao',Association('homem','gosta','couves')))

z.insert(Declaration('damasio', AssocOne('socrates','pai','sofronisco')))
z.insert(Declaration('darwin', AssocOne('socrates','pai','pericles')))
z.insert(Declaration('descartes', AssocOne('socrates','pai','sofronisco')))

print(z.list_associations())
print(z.list_objects())
print(z.list_users())
print(z.list_types())
print(z.list_local_associations('socrates'))
print(z.list_relations_by_user('descartes'))
print(z.count_associations_by_user('descartes'))
print(z.list_associations_per_entity('socrates'))
print(z.predecessor('vertebrado','socrates'))
print(z.predecessor('socrates','vertebrado'))
print(z.predecessor_path('vertebrado', 'socrates'))
print('-query:')
z.query('socrates', 'altura')
z.show_query_result()
print('-query2:')
z.query2('homem', 'mamar')
z.show_query_result()
print('-query2:')
z.query2('homem')
z.show_query_result()
print('-query cancel:')
z.query_cancel('socrates', 'altura')
z.show_query_result()
print('-query down:')
z.query_down('mamifero', 'altura')
z.show_query_result()
print('-query induce:', end=' ')
z.query_induce('vertebrado', 'altura')
z.show_query_result()
print('-query local association:', end=' ')
z.query_local_assoc('socrates', 'pai')
z.show_query_result()
print('-query local association:', end=' ')
z.query_local_assoc('socrates', 'pulsacao')
z.show_query_result()
print('-query local association:')
z.query_local_assoc('homem', 'gosta')
z.show_query_result()