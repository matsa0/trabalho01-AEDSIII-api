import requests
from weighted_graph import Graph

g = Graph()

#ler a api que contém os id's das votações
response_id_votes = requests.get("https://dadosabertos.camara.leg.br/api/v2/votacoes?ordem=DESC&ordenarPor=dataHoraRegistro&dataInicio=2022-01-01")
data_id_votes = response_id_votes.json()

votes_per_deputado = {}

for item in data_id_votes['dados']:
    id = item['id']
    #passar o id percorrido na api dos votos
    response_votes = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{id}/votos")
    data_votes = response_votes.json()

    votes = {}
    #percorrer a api dos votos pegando o nome e o tipo do voto
    for item2 in data_votes['dados']:
        name = item2['deputado_']['nome']
        vote = item2['tipoVoto']
        g.add_node(name)

        for key, value in votes.items(): #key = name, value = vote ###items() percorre pares chave-valor
            if value['voto'] == vote:
                if g.there_is_edge(name, key):
                    g.increment_edge_weight(name, key)
                    g.increment_edge_weight(key, name)
                else:
                    g.add_edge(name, key, 1)
                    g.add_edge(key, name, 1)
        votes[name] = {'voto': vote}

        #verificar quantas votações cada deputado participou
        if name not in votes_per_deputado:
            votes_per_deputado[name] = 1        
        else:
            votes_per_deputado[name] += 1

#escrita do grafo
with open("graph.txt", 'w', encoding="utf-8") as file:
    file.write(f"{g.node_count} {g.edge_count}\n")
    for node1 in g.adj_list:
        for node2, weight in g.adj_list[node1].items():
            node1_formatted = node1.replace(" ", "_")
            node2_formatted = node2.replace(" ", "_")
            file.write(f"{node1_formatted} {node2_formatted} {weight}\n")

#escrita dos votos
with open("votes.txt", 'w', encoding="utf-8") as file:
    for name, count in votes_per_deputado.items():
        name_formated = name.replace(" ", "_")
        file.write(f"{name_formated} {count}\n")
