import networkx as nx
from random import sample

def grouper(G, start, assigned_lst=[], num = 5):
    """Given a Graph G, a start node lm (line manager), 
    a list of people already assigned, and the desired number 
    of people per group return a list of the closest num-1 people to lm. 
    Sample is used to prevent stable patterns forming."""
    
    lm_lst = line_managers(G)
    
# Is start a line manager?
    if start in lm_lst:
        neb_lst = [start]
        
# If start is not a lm then they have a mentor line manager or are manager by Tess (more connections)
    else:
        if G.degree()[start] == G.number_of_nodes() - 2:
            lm_lst.remove([x for x in list(set(G.nodes) - set(G.neighbors(start))) if x != start][0])
            added_lm = sample(lm_lst,1)[0]
            neb_lst = [start, added_lm]
        
        else:
            added_lm = sample(lm_lst,1)[0]
            neb_lst = [start, added_lm]
            
    
    neb_weight = []
    
# If neb_list only has start then we pick new members from starts neighbours for the weight list
    if len(neb_lst) == 1:
        for i in list(nx.neighbors(G, start)):
            neb_weight.append((i, G[start][i]['weight']))

# If neb_lst has 2 members then we pick new ones from the intersection of start and lms neighbours for the weight list
    else:
        for i in [value for value in list(nx.neighbors(G, start)) if value in list(nx.neighbors(G, added_lm))]:
            neb_weight.append((i, G[start][i]['weight']))
    
# Shuffle the weight list then sort by weight, this breaks up stable formations
    neb_weight = sample(neb_weight, len(neb_weight))
    neb_weight.sort(key = lambda x: x[1])

# While then list of neighbours is less than the desired size add an element in from weight list as long as it's not been previously assigned (by earlier grouper)
    for i in neb_weight:
        if(len(neb_lst) < num):
            if i[0] not in assigned_lst:
                neb_lst.append(i[0])
        else:
            break
    return neb_lst


def line_managers(G, num=5):
    """Given G will return a list of the num nodes with fewest connections. In our model these represent line managers."""

    deg_lst = list(G.degree)
    deg_lst.sort(key= lambda x:x[1])
    return [x[0] for x in deg_lst[:num]]


def standups(G, lms=[], nm =5):
    """Given G, a list of starting nodes (when blank defaults to line managers), and a desired group size will return a list of groups partioning the entire graph."""
    
    if not lms:
        lm_lst = line_managers(G)
    else:
        lm_lst = lms
    
    groups_lst =[]
    as_lst = lm_lst
    
    if len(G.nodes) > len(lm_lst)*nm:
        
        print('Error: groups not large enough to cover entire team')
        return
    
    lm_lst = sample(lm_lst, len(lm_lst))
    
    for lm in lm_lst:
        semi_as_lst = as_lst
        semi_as_lst.remove(lm)
        grp = grouper(G, lm, semi_as_lst, num = nm)
        groups_lst.append(grp)
        as_lst.extend(grp)
    
    for mentor in list(G.nodes):
        if mentor not in as_lst:
            
            lm = [x for x in list(set(G.nodes) - set(G.neighbors(mentor))) if x != mentor][0]
            lm_neigh = [(i, G[lm][i]['weight']) for i in list(nx.neighbors(G, lm))]
            lm_neigh.sort(key = lambda x: x[1]) 
            
            for group in groups_lst:
                if lm_neigh[0][0] in group:
                    group.append(mentor)
                    group.remove(lm_neigh[0][0])
                if lm in group:
                    group.append(lm_neigh[0][0])
            
    return groups_lst

def update(G, group_lst):
    """Upticks the weighting between nodes in G if they are in group_lst."""
    
    G.add_weighted_edges_from([(i,j,G[i][j]['weight'] + 1) for i in group_lst for j in group_lst if ((i!=j) & (i in nx.neighbors(G, j)))])
    

def add_mentor(G, name, lm_name):
    """Add in a new mentor to the graph G given their line manager."""
    
    G.add_node(name)
    G.add_weighted_edges_from([(name, i, 1) for i in G.nodes if ((i!=lm_name) & (i!=name))])
    
def stand_update(G, start_lst = []):
    """Return the standup group for the month and updates the weights."""
    
    stup = standups(G,lms = start_lst, nm=5)
    for group in stup:
        update(G, group)
    return stup

def connectivity(G, name):
    """Returns a connectivity score (sum of neighbour weights) for a given node."""
    
    con = 0
    for neighbour in nx.neighbors(G,name):
        con += G[name][neighbour]['weight']
    return con

def group_connectivity(G, name, group):
    """Returns the increase in connectivity score (sum of neighbour weights) of a group that adding the named mentor would have"""
    
    con = 0
    for mentor in group:
        con += G[name][mentor]['weight']
    return con