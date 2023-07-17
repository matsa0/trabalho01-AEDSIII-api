import requests

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = {}
            self.node_count += 1

    def add_edge(self, node1, node2, weight):
        if node1 not in self.adj_list:
            self.add_node(node1)
        if node2 not in self.adj_list:
            self.add_node(node2)
        self.adj_list[node1][node2] = weight
        self.edge_count += 1

    def there_is_edge(self, node1, node2):
        if node1 in self.adj_list and node2 in self.adj_list[node1]:
            return True
        return False

    def increment_edge_weight(self, node1, node2):
        if self.there_is_edge(node1, node2):
            self.adj_list[node1][node2] += 1
        else:
            print(f"ERROR! There is no edge between {node1} and {node2}")

    def read_api_votes(self, api_link):
        response_id_votes = requests.get(api_link)
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
                self.add_node(name)

                for key, value in votes.items():
                    if value['voto'] == vote:
                        if self.there_is_edge(name, key):
                            self.increment_edge_weight(name, key)
                            self.increment_edge_weight(key, name)
                        else:
                            self.add_edge(name, key, 1)
                            self.add_edge(key, name, 1)
                votes[name] = {'voto': vote}

                if name not in votes_per_deputado:
                    votes_per_deputado[name] = 1
                else:
                    votes_per_deputado[name] += 1

        return votes_per_deputado

    def write_graph_file(self, filename):
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(f"{self.node_count} {self.edge_count}\n")
            for node1 in self.adj_list:
                for node2, weight in self.adj_list[node1].items():
                    node1_formatted = node1.replace(" ", "_")
                    node2_formatted = node2.replace(" ", "_")
                    file.write(f"{node1_formatted} {node2_formatted} {weight}\n")

    def write_votes_file(self, filename, votes_per_deputado):
        with open(filename, 'w', encoding="utf-8") as file:
            for name, count in votes_per_deputado.items():
                name_formatted = name.replace(" ", "_")
                file.write(f"{name_formatted} {count}\n")






    def __str__(self):
        output = ""
        for node in self.adj_list:
            output += str(node) + " -> "
            neighbors = self.adj_list[node]
            for neighbor, weight in neighbors.items():
                output += f"{neighbor} {weight}, "
            output = output.rstrip(", ") + "\n"
        return output