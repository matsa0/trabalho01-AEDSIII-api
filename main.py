from weighted_graph import Graph

g = Graph()
#"https://dadosabertos.camara.leg.br/api/v2/votacoes?ordem=DESC&ordenarPor=dataHoraRegistro&dataInicio=2022-01-01"
try:
    api_link = input("Informe o link da api com as votações > ")
    print("Processando...")

    votes_per_deputado = g.read_api_votes(api_link)
    g.write_graph_file("graph.txt")
    g.write_votes_file("votes.txt", votes_per_deputado)

    print("O grafo foi escrito nos arquivos: ")
    print("\tgraph.txt")
    print("\tvotes.txt")
except Exception as e:
    print(f"Erro ao processar a API > {str(e)}")
