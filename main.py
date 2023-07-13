import requests
from weighted_graph import Graph

g = Graph()

response_id_votes = requests.get("https://dadosabertos.camara.leg.br/api/v2/votacoes?ordem=DESC&ordenarPor=dataHoraRegistro")
data_id_votes = response_id_votes.json()

votes_per_deputado = {}

for item in data_id_votes['dados']:
    id = item['id']

    response_votes = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{id}/votos")
    data_votes = response_votes.json()

    votes = {}

    for item2 in data_votes['dados']:
        name = item2['deputado_']['nome']
        vote = item2['tipoVoto']
        g.add_node(name)

        for key, value in votes.items():
            if value['voto'] == vote:
                if g.there_is_edge(name, key):
                    g.increment_edge_weight(name, key)
                else:
                    g.add_edge(name, key, 1)
        votes[name] = {'voto': vote}

        if name not in votes_per_deputado:
            votes_per_deputado[name] = 0
        else:
            votes_per_deputado[name] += 1

with open("graph.txt", 'w', encoding="utf-8") as file:
    file.write(f"{g.node_count} {g.edge_count}\n")
    for node1 in g.adj_list:
        for node2, weight in g.adj_list[node1].items():
            file.write(f"{node1} {node2} {weight}\n")

with open("votes.txt", 'w', encoding="utf-8") as file:
    for name, count in votes_per_deputado.items():
        file.write(f"{name} {count}\n")
