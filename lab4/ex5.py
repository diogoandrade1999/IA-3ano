from constraintsearch import *


def amigos_constraint(a1, t1, a2, t2):
    c1, b1 = t1
    c2, b2 = t2

    # o mesmo objeto não pode ser partilhado por dois amigos
    if c1 == c2 or b1 == b2:
    	return False

    # não pode ter chapeu/bicicleta propria
    if a1 in [c1, b1] or a2 in [c2, b2]:
    	return False

    # chapeu e bicicleta pertencem a amigos diferentes
    if c1 == b1 or c2 == b2:
    	return False

    # o que leva a bicicleta do Claudio anda na bicicleta do Bernado
    if c1 == 'Claudio' and b1 != 'Bernardo':
    	return False
    return True

def make_constraint_graph(amigos):
    return {(X,Y):amigos_constraint for X in amigos for Y in amigos if X != Y}

def make_domains(amigos):
    return {amigo:[(c, b) for c in amigos for b in amigos] for amigo in amigos}


amigos = ['André', 'Bernardo', 'Claudio']
cs = ConstraintSearch(make_domains(amigos),make_constraint_graph(amigos))

print(cs.search())
print(cs.calls)