

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2018
# v1.81 - 2018/11/18
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#
from collections import Counter


class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')


class AssocOne(Association):
    def __init__(self,e1,assoc,e2):
        Association.__init__(self,e1,assoc,e2)


class AssocNum(Association):
    def __init__(self,e1,assoc,e2):
        num = float(e2)
        Association.__init__(self,e1,assoc,num)


# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=[]):
        self.declarations = ldecl
    def __str__(self):
        return my_list2string(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
    def list_associations(self):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)]))
    def list_objects(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))
    def list_users(self):
        return list(set([d.user for d in self.declarations]))
    def list_types(self):
        return list(set([d.relation.entity2 for d in self.declarations \
            if isinstance(d.relation, Member) or isinstance(d.relation, Subtype)] + \
            [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)]))
    def list_local_associations(self, entity):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) \
            and (d.relation.entity1 == entity or d.relation.entity2 == entity)]))
    def list_relations_by_user(self, user):
        return list(set([d.relation.name for d in self.declarations if d.user == user]))
    def count_associations_by_user(self, user):
        return len(set([d.relation.name for d in self.declarations if d.user == user \
            and isinstance(d.relation, Association)]))
    def list_associations_per_entity(self, entity):
        return list(set([(d.relation.name, d.user) for d in self.declarations if isinstance(d.relation, Association) \
            and (d.relation.entity1 == entity or d.relation.entity2 == entity)]))
    def predecessor(self, A, B):
        rel = [d.relation for d in self.declarations if (isinstance(d.relation, Member) \
            or isinstance(d.relation, Subtype)) and d.relation.entity1 == B]
        if [r for r in rel if r.entity2 == A] != []:
            return True
        return any([self.predecessor(A, r.entity2) for r in rel])
    def predecessor_path(self, A, B):
        direct_predecessor = [d.relation for d in self.declarations if (isinstance(d.relation, Member) \
            or isinstance(d.relation, Subtype)) and d.relation.entity1 == B]
        if [r for r in direct_predecessor if r.entity2 == A] != []:
            return [A, B]
        for p in direct_predecessor:
            pp = self.predecessor_path(A, p.entity2)
            if pp:
                return pp + [B]
        return None
        # em vez do for
        # return [path + [B] for path in [self.predecessor_path(A, p.entity2) for p in direct_predecessor] if path][0]
    def query(self, entity, association=None):
        inherited = [self.query(d.relation.entity2, association) for d in self.declarations \
                    if d.relation.entity1 == entity and (isinstance(d.relation, Member) or \
                    isinstance(d.relation, Subtype))]
        self.query_result = [item for sublist in inherited for item in sublist] + \
                [d for d in self.declarations if d.relation.entity1 == entity and \
                isinstance(d.relation, Association) and (association == None or \
                d.relation.name == association)]
        return self.query_result
    def query2(self, entity, relation=None):
        inherited = [self.query2(d.relation.entity2, relation) for d in self.declarations \
                    if d.relation.entity1 == entity and (isinstance(d.relation, Member) or \
                    isinstance(d.relation, Subtype))]
        self.query_result = [item for sublist in inherited for item in sublist if not \
                (isinstance(item.relation, Member) or isinstance(item.relation, Subtype))] + \
                [d for d in self.declarations if d.relation.entity1 == entity and \
                (relation == None or d.relation.name == relation)]
        return self.query_result
    def query_cancel(self, entity, relation=None):
        inherited = [self.query_cancel(d.relation.entity2, relation) for d in self.declarations \
                    if d.relation.entity1 == entity and (isinstance(d.relation, Member) or \
                    isinstance(d.relation, Subtype))]
        local = [d for d in self.declarations if d.relation.entity1 == entity and \
                (relation == None or d.relation.name == relation)]
        local_rels = [l.relation.name for l in local]
        self.query_result = [item for sublist in inherited for item in sublist if not item.relation.name \
                in local_rels] + local
        return self.query_result
    def query_down(self, entity, association):
        descendents = [self.query_down(d.relation.entity1, association) for d in self.declarations \
                        if d.relation.entity2 == entity and (isinstance(d.relation, Member) \
                        or isinstance(d.relation, Subtype))]
        self.query_result = [item for sublist in descendents for item in sublist] + [d for d in \
                self.declarations if d.relation.entity1 == entity and d.relation.name == association]
        return self.query_result
    def query_induce(self, entity, association):
        suc = self.query_down(entity, association)
        c = Counter([d.relation.entity2 for d in suc])
        self.query_result =  [m[0] for m in c.most_common(1)]
        return self.query_result
    def query_local_assoc(self, entity, relation):
        local = self.query_local(e1=entity, rel=relation)
        if len(local) and isinstance(local[0].relation, AssocOne):
            counter = Counter([l.relation.entity2 for l in local])
            self.query_result = [(e, c/len(local)) for e,c in counter.most_common(1)]
        elif len(local) and isinstance(local[0].relation, AssocNum):
            self.query_result = [sum([l.relation.entity2 for l in local])/len(local)]
        else:
            counter = Counter([l.relation.entity2 for l in local])
            fsum = 0
            self.query_result =[]
            for e,c in counter.items():
                if fsum < 0.75:
                    self.query_result.append((e, c/len(local)))
                    fsum += c/len(local)
        return self.query_result

# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
