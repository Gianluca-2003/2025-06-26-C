import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()



    def buildGraph(self,y_min,y_max):
        self._graph.clear()
        self._nodes = DAO.get_nodes()
        self._idMapNodes = {}
        for node in self._nodes:
            self._idMapNodes[node.constructorId] = node
        self._edges = DAO.get_edges(y_min,y_max,self._idMapNodes)
        self._graph.add_nodes_from(self._nodes)
        self._pesi = DAO.get_pesi(y_min,y_max)
        for edge in self._edges:
            u = edge[0]
            v = edge[1]
            peso = self._pesi[u.constructorId] + self._pesi[v.constructorId]
            self._graph.add_edge(u,v, weight=peso)


    def printGraph(self):
        return f"Il grafo ha {len(self._graph.nodes)} nodi e {len(self._graph.edges)} archi."



    def get_info_comp(self):
        componenti = list(nx.connected_components(self._graph))
        max_comp = []
        for comp in componenti:
            if len(comp) > len(max_comp):
                max_comp = copy.deepcopy(comp)

        lista = []
        for node in max_comp:
            peso_max = 0
            vicini = list(self._graph.neighbors(node))
            for vic in vicini:
                peso = self._graph[node][vic]['weight']
                if peso > peso_max:
                    peso_max = peso
            lista.append((peso_max,node))

        lista.sort(key=lambda x: x[0], reverse=True)

        return lista


    def get_max_comp(self):
        componenti = list(nx.connected_components(self._graph))
        max_comp = []
        for comp in componenti:
            if len(comp) > len(max_comp):
                max_comp = copy.deepcopy(comp)
        return max_comp



    def get_opt_set(self,k,m,y_min,y_max):
        validi = []
        costruttori = self.get_max_comp()
        m_costruttori = DAO.get_validi_costuttori(y_min,y_max,m,self._idMapNodes)
        for c in costruttori:
            if c in m_costruttori:
                validi.append(c)
        if len(validi) < k:
            return []
        self._pesi_tot = DAO.get_pesi_totoli(y_min,y_max)
        self._bestTasso = -1
        self._bestTeam = []

        self.ricorsione([],0,k,validi)

        return self._bestTasso, self._bestTeam



    def ricorsione(self,path,start,k,validi):
        if len(path) == k:
            tasso = self.calcolaTasso(path)
            if tasso > self._bestTasso:
                self._bestTasso = tasso
                self._bestTeam = copy.deepcopy(path)
            return
        for i in range(start,len(validi)):
            node = validi[i]
            if node not in path:
                path.append(node)
                self.ricorsione(path,i+1,k,validi)
                path.pop()


    def calcolaTasso(self,path):
        tasso_tot = 0
        for node in path:
            n_p = self._pesi[node.constructorId]
            n_pTot = self._pesi_tot[node.constructorId]
            tasso_tot += 1 - (n_p / n_pTot)
        return tasso_tot


    def get_years(self):
        return DAO.get_years()















