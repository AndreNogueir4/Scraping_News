import json
import os
import importlib
import webbrowser

def carregar_sites():
    if not os.path.exists('sites.json'):
        return []
    with open('sites.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def salvar_sites(sites):
    with open('sites.json', 'w', encoding='utf-8') as file:
        json.dump(sites, file, indent=4, ensure_ascii=False)

def salvar_sugestoes(sugestoes):
    with open('sugestoes.json', 'w', encoding='utf-8') as file:
        json.dump(sugestoes, file, indent=4, ensure_ascii=False)

def carregar_sugestoes():
    if not os.path.exists('sugestoes.json'):
        return []
    with open('sugestoes.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def adicionar_site(nome, modulo):
    sites = carregar_sites()
    sites.append({"nome": nome, "modulo": modulo})
    salvar_sites(sites)

    salvar_como_sugestao = input("Deseja salvar este site como sugestao? (s/n): ").strip().lower()
    if salvar_como_sugestao == 's':
        sugestoes = carregar_sugestoes()
        sugestoes.append({"nome": nome, "modulo": modulo})
        salvar_sugestoes(sugestoes)

def remover_site(nome):
    sites = carregar_sites()
    sites = [site for site in sites if site['nome'] != nome]
    salvar_sites(sites)

def menu():
    while True:
        print("\nMenu:")
        print("1. Listar sites")
        print("2. Adicionar site")
        print("3. Remover site")
        print("4. Exibir notícias")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_sites()
        elif opcao == '2':
            nome = input("Nome do site: ")
            modulo = input("Nome do módulo (ex: scraping_globo.scrape_globo): ")
            adicionar_site(nome, modulo)
        elif opcao == '3':
            nome = input("Nome do site para remover: ")
            remover_site(nome)
        elif opcao == '4':
            exibir_noticias()
        elif opcao == '5':
            break
        else:
            print("Opção inválida!")

def listar_sites():
    sites = carregar_sites()
    for site in sites:
        print(f"{site['nome']}")

def exibir_noticias():
    sites = carregar_sites()
    todas_noticias = []

    for site in sites:
        try:
            modulo = importlib.import_module(site['modulo'])
            noticias = modulo.scrape()
            todas_noticias.extend(noticias)
        except Exception as e:
            print(f"Erro ao exibir noticias de {site['nome']}: {e}")

    if not todas_noticias:
        print("Nenhuma noticia disponivel")
        return

    todas_noticias.sort(key=lambda x: x['data'], reverse=True)
    pagina = 0
    noticias_por_pagina = 20
    total_paginas = (len(todas_noticias) + noticias_por_pagina - 1) // noticias_por_pagina

    while True:
        inicio = pagina * noticias_por_pagina
        fim = inicio + noticias_por_pagina
        noticias_pagina = todas_noticias[inicio:fim]

        print(f"\nPagina {pagina + 1}/{total_paginas}")
        for index, noticia in enumerate(noticias_pagina, start=inicio + 1):
            print(f"{index}. {noticia['titulo']} (Data: {noticia['data']}, Hora: {noticia['hora']}, Portal: {noticia['portal']})")
            print("-" * 100)

        print("\nP: Proxima pagina | V: Pagina anterior | E: Escolher noticia | S: Voltar Menu")
        opcao = input("Escolha uma opcao: ").strip().upper()

        if opcao == 'P' and pagina < total_paginas - 1:
            pagina += 1
        elif opcao == 'V' and pagina > 0:
            pagina -= 1
        elif opcao == 'E':
            num_noticia = int(input("Digite o numero da noticia: "))
            if 1 <= num_noticia <= len(todas_noticias):
                noticia_selecionada = todas_noticias[num_noticia - 1]
                webbrowser.open(noticia_selecionada['link'])
            else:
                print("Numero invalido")
        elif opcao == 'S':
            break
        else:
            print("Opcao invalida!!")

if __name__ == "__main__":
    menu()