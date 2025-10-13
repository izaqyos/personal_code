import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

DG = nx.DiGraph()
DG.add_edges_from(
    [('Site1', 'Role1'), ('Site2', 'Role1'), ('Site3', 'Role2'), ('Role1', 'Bussiness-App1'),('Role1', 'Bussiness-App2'), ('Role2', 'Bussiness-App2') , ('Role2', 'Bussiness-App3'), ('Catalog2', 'Catalog2'), ('Catalog1', 'Bussiness-App1'), ('Group1', 'Group1'), ('Group2', 'Bussiness-App3')])


nx.draw(DG, with_labels = True, font_weight='bold')
plt.show()
