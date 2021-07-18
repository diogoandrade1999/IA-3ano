from constraintsearch import *


def border_constraint(pais1,cor1,pais2,cor2):
    return cor1 != cor2

def make_constraint_graph(mapa):
    # cada dois paises vizinhos nao partilham a mesma cor
    return {(X,Y):border_constraint for X in mapa.keys() for Y in mapa[X]}

def make_domains(fronteiras, lista_cores):
    return {pais:lista_cores for pais in fronteiras.keys()}


mapa_a = {'A': ['B', 'E', 'D'], 
        'B': ['A', 'C', 'E'], 
        'C': ['B', 'D', 'E'], 
        'D': ['A', 'C', 'E'], 
        'E': ['A', 'B', 'C', 'D']
        }
cores = ['blue', 'red', 'green', 'white', 'black']
cs = ConstraintSearch(make_domains(mapa_a, cores),make_constraint_graph(mapa_a))

print(cs.search())
print(cs.calls)
