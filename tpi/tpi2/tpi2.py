# Diogo Andrade, nmec 89265
# comentá-mos os exercicios: 88751

from semantic_network import *
from bayes_net import *


class MySN(SemanticNetwork):

    def query_dependents(self,entity):
        depends = [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Depends) \
            and (d.relation.entity2 == entity)]
        subtype = [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype) \
            and (d.relation.entity2 == entity)]
        if not depends and not subtype: return []
        query = depends
        for entity_depend in depends:
            subtype_depend = [d.relation.entity1 for d in self.declarations \
                            if isinstance(d.relation, Subtype) and (d.relation.entity2 == entity_depend)]
            if subtype_depend: query.remove(entity_depend)
            query.extend(subtype_depend)
            query.extend(self.query_dependents(entity_depend))
        for entity_subtype in subtype:
            depends_depend = [d.relation.entity1 for d in self.declarations \
                            if isinstance(d.relation, Depends) and (d.relation.entity2 == entity_subtype)]
            query.extend(depends_depend)
            query.extend(self.query_dependents(entity_subtype))
        return list(set(query))

    def query_causes(self, entity):
        depends = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Depends) \
                    and (d.relation.entity1 == entity)]
        subtype = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype) \
                    and (d.relation.entity1 == entity)]
        causes = depends + subtype
        if not causes: return []
        query = depends + [c for e in causes for c in self.query_causes(e)]
        return list(set(query))

    def query_causes_sorted(self,entity):
        query_causes = self.query_causes(entity)
        causes = {}
        for d in self.declarations:
            if isinstance(d.relation, Association) and (d.relation.name == 'debug_time') \
                and d.relation.entity1 in query_causes:
                if d.relation.entity1 not in causes: causes[d.relation.entity1] = (0, 0)
                causes[d.relation.entity1] = (causes[d.relation.entity1][0]+1, causes[d.relation.entity1][1]+d.relation.entity2)
        causes = sorted([(c, causes[c][1]/causes[c][0]) for c in causes], key=lambda value:(value[1], value[0]))
        return causes

class MyBN(BayesNet):

    def markov_blanket(self,var):
        var_plus_childs = [var]
        childs = list(set([d for d in self.dependencies for item in self.dependencies[d].items() \
            if var in dict(item[0])]))
        var_plus_childs.extend(childs)
        parents = list(set([mother for vc in var_plus_childs for d in self.dependencies[vc].items() \
            for mother in dict(d[0]) if mother != var]))
        return parents + childs
