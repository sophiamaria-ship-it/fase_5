"""
=======================================================================
 NUCLEO COGNITIVO DA AURORA SIGER (NCAS)
=======================================================================
Sistema de registro, organizacao, consulta e interpretacao de
informacoes operacionais da colonia Aurora Siger.

Conteudos aplicados neste projeto:
 - Manipulacao de arquivos texto e JSON (open, with, modos w/r/a)
 - Metodos read(), readline(), readlines(), writelines()
 - Dicionarios em Python
 - Algebra booleana / Teoremas de simplificacao e De Morgan
 - Engenharia de prompts (zero-shot, few-shot, structured output)
 - Simulacao de resposta de assistente inteligente (sem API real)
 - Reflexao sobre diversidade, etica e responsabilidade no uso de IA

Autor: Equipe NCAS
=======================================================================
"""

import json
import os
from datetime import datetime

# -----------------------------------------------------------------
# 1. CONSTANTES E CAMINHOS DOS ARQUIVOS
# -----------------------------------------------------------------
# Justificativa da escolha de formato:
#   - Dados ESTRUTURADOS (modulos, alertas, solicitacoes, historico de
#     respostas) sao guardados em JSON, pois possuem varios campos
#     (chave/valor) que precisam ser lidos, filtrados e atualizados
#     de forma organizada pelo programa.
#   - Dados de REGISTRO SIMPLES e cronologico (logs de manutencao e
#     logs de acesso) sao guardados em TEXTO puro, pois sao apenas
#     linhas sequenciais que so precisam ser acrescentadas (append)
#     e lidas em ordem, sem necessidade de estrutura de chaves.
ARQUIVO_JSON = "dados_colonia.json"
ARQUIVO_TEXTO = "registros_colonia.txt"


# -----------------------------------------------------------------
# 2. FUNCOES DE MANIPULACAO DE ARQUIVO TEXTO
# -----------------------------------------------------------------
def gravar_registro_texto(categoria: str, mensagem: str) -> None:
    """Adiciona uma nova linha de registro no arquivo texto (modo 'a')."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] {categoria.upper()} | {mensagem}\n"
    # Modo 'a' (append): preserva o historico ja existente no arquivo.
    with open(ARQUIVO_TEXTO, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)
    print("\n[OK] Registro salvo em registros_colonia.txt")


def ler_registros_texto() -> None:
    """Le e exibe todo o conteudo do arquivo texto usando readlines()."""
    if not os.path.exists(ARQUIVO_TEXTO):
        print("\n[AVISO] Nenhum registro encontrado ainda.")
        return

    with open(ARQUIVO_TEXTO, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    print("\n--- REGISTROS DA COLONIA ---")
    for linha in linhas:
        print(linha.rstrip("\n"))
    print("--- FIM DOS REGISTROS ---")


# -----------------------------------------------------------------
# 3. FUNCOES DE MANIPULACAO DE ARQUIVO JSON
# -----------------------------------------------------------------
def carregar_dados_json() -> dict:
    """Carrega o dicionario de dados a partir do arquivo JSON.

    Se o arquivo nao existir, cria uma estrutura vazia padrao.
    """
    if not os.path.exists(ARQUIVO_JSON):
        estrutura_padrao = {
            "modulos": [],
            "alertas": [],
            "solicitacoes": [],
            "historico_respostas": []
        }
        salvar_dados_json(estrutura_padrao)
        return estrutura_padrao

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados


def salvar_dados_json(dados: dict) -> None:
    """Salva (sobrescreve) o dicionario de dados no arquivo JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def proximo_id(lista: list) -> int:
    """Gera um novo id sequencial simples para uma lista de dicionarios."""
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def cadastrar_alerta() -> None:
    """Cadastra um novo alerta operacional na estrutura JSON."""
    dados = carregar_dados_json()

    print("\n--- CADASTRO DE ALERTA OPERACIONAL ---")
    modulo = input("Modulo afetado: ").strip()
    tipo_ocorrencia = input("Tipo de ocorrencia: ").strip()
    prioridade = input("Prioridade (baixa/media/alta): ").strip().lower()
    mensagem = input("Mensagem resumida: ").strip()
    falha = input("Houve falha? (s/n): ").strip().lower() == "s"
    critico = input("E critico? (s/n): ").strip().lower() == "s"

    novo_alerta = {
        "id": proximo_id(dados["alertas"]),
        "modulo": modulo,
        "tipo_ocorrencia": tipo_ocorrencia,
        "prioridade": prioridade,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "mensagem": mensagem,
        "falha": falha,
        "critico": critico
    }

    dados["alertas"].append(novo_alerta)
    salvar_dados_json(dados)
    gravar_registro_texto("ALERTA", f"Novo alerta cadastrado no modulo {modulo} ({prioridade}).")
    print("\n[OK] Alerta cadastrado com sucesso em dados_colonia.json")


def cadastrar_solicitacao() -> None:
    """Cadastra uma nova solicitacao da tripulacao na estrutura JSON."""
    dados = carregar_dados_json()

    print("\n--- CADASTRO DE SOLICITACAO DA TRIPULACAO ---")
    tripulante = input("Nome do tripulante: ").strip()
    setor = input("Setor: ").strip()
    urgente = input("E urgente? (s/n): ").strip().lower() == "s"
    descricao = input("Descricao da solicitacao: ").strip()

    nova_solicitacao = {
        "id": proximo_id(dados["solicitacoes"]),
        "tripulante": tripulante,
        "setor": setor,
        "urgente": urgente,
        "descricao": descricao,
        "data": datetime.now().strftime("%Y-%m-%d")
    }

    dados["solicitacoes"].append(nova_solicitacao)
    salvar_dados_json(dados)
    gravar_registro_texto("SOLICITACAO", f"Nova solicitacao de {tripulante} ({setor}).")
    print("\n[OK] Solicitacao cadastrada com sucesso em dados_colonia.json")


def consultar_dados_json() -> None:
    """Exibe de forma organizada os dados armazenados em JSON."""
    dados = carregar_dados_json()

    print("\n--- MODULOS DA COLONIA ---")
    for modulo in dados["modulos"]:
        print(f"[{modulo['id']}] {modulo['nome']} | status: {modulo['status']} | resp.: {modulo['responsavel']}")

    print("\n--- ALERTAS OPERACIONAIS ---")
    for alerta in dados["alertas"]:
        print(f"[{alerta['id']}] {alerta['modulo']} | {alerta['tipo_ocorrencia']} | "
              f"prioridade: {alerta['prioridade']} | critico: {alerta['critico']}")

    print("\n--- SOLICITACOES DA TRIPULACAO ---")
    for solicitacao in dados["solicitacoes"]:
        print(f"[{solicitacao['id']}] {solicitacao['tripulante']} ({solicitacao['setor']}) | "
              f"urgente: {solicitacao['urgente']}")


# -----------------------------------------------------------------
# 4. REGRAS LOGICAS E SIMPLIFICACAO BOOLEANA
# -----------------------------------------------------------------
# REGRA 1 - Geracao de alerta critico
#   Original : ALERTA = (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)
#   Simplificada (Teorema da Simplificacao / Absorcao):
#       A.B + A.B' = A
#   Aplicando: FALHA.CRITICO + FALHA.(NOT CRITICO) = FALHA
#   Logo: ALERTA = FALHA
#   Ou seja, o resultado depende apenas da existencia de falha,
#   independentemente do valor de CRITICO. A simplificacao mantem o
#   mesmo resultado logico porque, nos dois casos possiveis de
#   CRITICO (verdadeiro ou falso), a saida so e verdadeira quando
#   FALHA e verdadeira.
def verificar_alerta(falha: bool, critico: bool) -> bool:
    """Regra simplificada: ALERTA = FALHA."""
    alerta_original = (falha and critico) or (falha and not critico)
    alerta_simplificado = falha
    assert alerta_original == alerta_simplificado, "Simplificacao invalida!"
    return alerta_simplificado


# REGRA 2 - Liberacao de consulta ao sistema
#   LIBERAR_CONSULTA = AUTORIZADO AND MODULO_ATIVO
def liberar_consulta(autorizado: bool, modulo_ativo: bool) -> bool:
    return autorizado and modulo_ativo


# REGRA 3 - Bloqueio de operacao (demonstracao de De Morgan)
#   BLOQUEAR = NOT (AUTORIZADO AND MODULO_ATIVO)
#   Por De Morgan: NOT (A AND B) = (NOT A) OR (NOT B)
#   Logo: BLOQUEAR = (NOT AUTORIZADO) OR (NOT MODULO_ATIVO)
def bloquear_operacao(autorizado: bool, modulo_ativo: bool) -> bool:
    bloqueio_original = not (autorizado and modulo_ativo)
    bloqueio_de_morgan = (not autorizado) or (not modulo_ativo)
    assert bloqueio_original == bloqueio_de_morgan, "De Morgan invalido!"
    return bloqueio_de_morgan


def executar_validacao_logica() -> None:
    """Menu auxiliar para testar as regras logicas do sistema."""
    print("\n--- VALIDACAO LOGICA ---")
    print("1 - Verificar se um alerta e critico (ALERTA = FALHA)")
    print("2 - Verificar liberacao de consulta (AUTORIZADO AND ATIVO)")
    print("3 - Verificar bloqueio de operacao (De Morgan)")
    opcao = input("Escolha uma opcao: ").strip()

    if opcao == "1":
        falha = input("Houve falha? (s/n): ").strip().lower() == "s"
        critico = input("E critico? (s/n): ").strip().lower() == "s"
        resultado = verificar_alerta(falha, critico)
        print(f"\nResultado -> ALERTA = {resultado}")
    elif opcao == "2":
        autorizado = input("Usuario autorizado? (s/n): ").strip().lower() == "s"
        ativo = input("Modulo ativo? (s/n): ").strip().lower() == "s"
        resultado = liberar_consulta(autorizado, ativo)
        print(f"\nResultado -> LIBERAR_CONSULTA = {resultado}")
    elif opcao == "3":
        autorizado = input("Usuario autorizado? (s/n): ").strip().lower() == "s"
        ativo = input("Modulo ativo? (s/n): ").strip().lower() == "s"
        resultado = bloquear_operacao(autorizado, ativo)
        print(f"\nResultado -> BLOQUEAR_OPERACAO = {resultado}")
    else:
        print("\n[AVISO] Opcao invalida.")


# -----------------------------------------------------------------
# 5. ENGENHARIA DE PROMPTS E SIMULACAO DE IA GENERATIVA
# -----------------------------------------------------------------
# Nao ha integracao real com API de IA (opcional segundo o enunciado).
# As respostas sao simuladas localmente por meio de templates de
# texto, preservando a logica e a estrutura de um prompt real.
PROMPTS = {
    "zero_shot": (
        "Voce e o assistente do Nucleo Cognitivo da Aurora Siger. "
        "Resuma o alerta operacional a seguir em ate 2 frases, "
        "destacando o modulo afetado e o nivel de risco.\n"
        "Alerta: {alerta}"
    ),
    "few_shot": (
        "Classifique a solicitacao da tripulacao em uma das categorias: "
        "URGENTE, ROTINA ou INFORMATIVA.\n\n"
        "Exemplo 1:\n"
        "Solicitacao: 'Vazamento de oxigenio no modulo 2'\n"
        "Categoria: URGENTE\n\n"
        "Exemplo 2:\n"
        "Solicitacao: 'Relatorio semanal de consumo de agua'\n"
        "Categoria: ROTINA\n\n"
        "Agora classifique:\n"
        "Solicitacao: '{solicitacao}'\n"
        "Categoria:"
    ),
    "saida_estruturada": (
        "Gere uma resposta padronizada ao centro de controle em formato JSON, "
        "com os campos: modulo, nivel_risco e recomendacao, a partir do "
        "seguinte alerta: {alerta}\n"
        "Responda apenas com um objeto JSON valido."
    )
}


def exibir_prompts() -> None:
    """Exibe os prompts estruturados criados pela equipe."""
    print("\n--- PROMPTS ESTRUTURADOS DO NCAS ---")
    print("\n[ZERO-SHOT]\n" + PROMPTS["zero_shot"])
    print("\n[FEW-SHOT]\n" + PROMPTS["few_shot"])
    print("\n[SAIDA ESTRUTURADA]\n" + PROMPTS["saida_estruturada"])


def simular_resposta_ia(tipo_alerta_critico: bool, modulo: str, mensagem: str) -> dict:
    """Simula localmente a resposta de um assistente inteligente.

    Nao chama nenhuma API externa: apenas aplica regras simples sobre
    o texto de entrada para compor uma saida estruturada em JSON,
    imitando o comportamento de um LLM guiado por prompt.
    """
    nivel_risco = "alto" if tipo_alerta_critico else "moderado"
    recomendacao = (
        "Acionar equipe de manutencao imediatamente e isolar o modulo."
        if tipo_alerta_critico else
        "Monitorar o modulo e agendar verificacao na proxima janela de manutencao."
    )

    resposta = {
        "modulo": modulo,
        "nivel_risco": nivel_risco,
        "recomendacao": recomendacao,
        "resumo": f"Alerta em {modulo}: {mensagem}"
    }
    return resposta


def registrar_historico_resposta(prompt_usado: str, resposta: dict) -> None:
    """Salva a interacao simulada (prompt + resposta) no historico em JSON."""
    dados = carregar_dados_json()
    entrada = {
        "id": proximo_id(dados["historico_respostas"]) if dados["historico_respostas"] else 1,
        "prompt_usado": prompt_usado,
        "resposta": resposta,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    dados["historico_respostas"].append(entrada)
    salvar_dados_json(dados)


def analisar_alerta_operacional() -> None:
    """Funcionalidade principal de demonstracao integrada do sistema.

    Fluxo: carrega alerta salvo em JSON -> aplica regra booleana
    simplificada -> monta prompt estruturado -> simula resposta de IA
    -> grava historico da interacao.
    """
    dados = carregar_dados_json()

    if not dados["alertas"]:
        print("\n[AVISO] Nao ha alertas cadastrados.")
        return

    print("\n--- ALERTAS DISPONIVEIS ---")
    for alerta in dados["alertas"]:
        print(f"[{alerta['id']}] {alerta['modulo']} - {alerta['tipo_ocorrencia']}")

    try:
        id_escolhido = int(input("\nDigite o id do alerta a analisar: "))
    except ValueError:
        print("\n[AVISO] Id invalido.")
        return

    alerta = next((a for a in dados["alertas"] if a["id"] == id_escolhido), None)
    if alerta is None:
        print("\n[AVISO] Alerta nao encontrado.")
        return

    # 1) Aplica a regra logica simplificada (ALERTA = FALHA)
    e_alerta = verificar_alerta(alerta["falha"], alerta["critico"])
    print(f"\n[REGRA LOGICA] ALERTA = FALHA -> resultado: {e_alerta}")

    # 2) Monta o prompt estruturado com os dados do alerta
    prompt_montado = PROMPTS["saida_estruturada"].format(alerta=alerta["mensagem"])
    print("\n[PROMPT UTILIZADO]\n" + prompt_montado)

    # 3) Simula a resposta do assistente inteligente
    resposta = simular_resposta_ia(alerta["critico"], alerta["modulo"], alerta["mensagem"])
    print("\n[RESPOSTA SIMULADA DO ASSISTENTE]")
    print(json.dumps(resposta, indent=4, ensure_ascii=False))

    # 4) Registra a interacao no historico (JSON) e no log (texto)
    registrar_historico_resposta(prompt_montado, resposta)
    gravar_registro_texto("ANALISE_ALERTA", f"Alerta {alerta['id']} do modulo {alerta['modulo']} analisado pelo NCAS.")


# -----------------------------------------------------------------
# 6. MEMORIA, ARMAZENAMENTO E FLUXO DE DADOS (explicacao textual)
# -----------------------------------------------------------------
def explicar_memoria_armazenamento() -> None:
    texto = """
--- MEMORIA, ARMAZENAMENTO E FLUXO DE DADOS NO NCAS ---
Mesmo trabalhando apenas com Python e arquivos texto/JSON, os dados
do sistema nao existem "soltos" no computador. Quando o NCAS cadastra
um alerta, o dicionario em Python fica temporariamente na MEMORIA RAM
(memoria volatil, rapida, usada durante a execucao). Ao chamar
salvar_dados_json(), o conteudo e convertido em texto (JSON) e
gravado fisicamente no ARMAZENAMENTO (disco), por meio de uma
operacao de ESCRITA (write). Esse dado passa a existir de forma
persistente mesmo apos o programa ser encerrado.
Quando o sistema e reaberto e chamamos carregar_dados_json(), ocorre
uma operacao de LEITURA (read): o dado sai do armazenamento em disco,
e transportado pelo barramento do computador ate a memoria RAM, e so
entao pode ser processado novamente pelo Python. Esse ciclo
escrita -> armazenamento -> leitura -> memoria -> processamento
representa o FLUXO DE INFORMACOES do nucleo cognitivo da colonia.
"""
    print(texto)


# -----------------------------------------------------------------
# 7. DIVERSIDADE, ETICA E RESPONSABILIDADE NO USO DA IA
# -----------------------------------------------------------------
def exibir_reflexao_etica() -> None:
    texto = """
--- DIVERSIDADE, ETICA E RESPONSABILIDADE NO NCAS ---
O Nucleo Cognitivo da Aurora Siger simula respostas de um assistente
inteligente para apoiar decisoes da colonia. Por isso, a equipe
reconhece riscos importantes: um sistema treinado com dados pouco
diversos pode gerar respostas enviesadas, priorizando indevidamente
certos modulos, setores ou grupos de tripulantes. A diversidade no
desenvolvimento (de quem programa, testa e revisa o sistema) ajuda a
identificar pontos cegos antes que causem danos reais.
O NCAS evita linguagem discriminatoria em suas respostas simuladas e
trata todas as solicitacoes da tripulacao com os mesmos criterios
objetivos (urgencia, setor, criticidade), nunca com base em quem fez
o pedido. Alem disso, mesmo com respostas automatizadas, a decisao
final sobre acoes criticas (isolar um modulo, bloquear uma operacao)
deve permanecer sob responsabilidade humana, cabendo ao sistema
apenas recomendar e organizar informacoes, nunca substituir o
julgamento da equipe da colonia.
"""
    print(texto)


# -----------------------------------------------------------------
# 8. MENU PRINCIPAL DO SISTEMA
# -----------------------------------------------------------------
def exibir_menu() -> None:
    print("\n=====================================================")
    print(" NUCLEO COGNITIVO DA AURORA SIGER (NCAS)")
    print("=====================================================")
    print("1 - Cadastrar registro de manutencao (texto)")
    print("2 - Cadastrar alerta operacional (JSON)")
    print("3 - Cadastrar solicitacao da tripulacao (JSON)")
    print("4 - Consultar registros salvos (texto)")
    print("5 - Consultar dados salvos (JSON)")
    print("6 - Analisar alerta operacional (regra + prompt + IA simulada)")
    print("7 - Executar validacao logica")
    print("8 - Exibir prompts estruturados")
    print("9 - Explicar memoria e armazenamento")
    print("10 - Reflexao sobre diversidade e etica")
    print("0 - Sair")


def main() -> None:
    # Garante que os arquivos existam desde o primeiro uso.
    carregar_dados_json()
    if not os.path.exists(ARQUIVO_TEXTO):
        open(ARQUIVO_TEXTO, "a", encoding="utf-8").close()

    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opcao: ").strip()

        if opcao == "1":
            modulo = input("Modulo: ").strip()
            descricao = input("Descricao da manutencao: ").strip()
            gravar_registro_texto("MANUTENCAO", f"Modulo {modulo} | {descricao}")
        elif opcao == "2":
            cadastrar_alerta()
        elif opcao == "3":
            cadastrar_solicitacao()
        elif opcao == "4":
            ler_registros_texto()
        elif opcao == "5":
            consultar_dados_json()
        elif opcao == "6":
            analisar_alerta_operacional()
        elif opcao == "7":
            executar_validacao_logica()
        elif opcao == "8":
            exibir_prompts()
        elif opcao == "9":
            explicar_memoria_armazenamento()
        elif opcao == "10":
            exibir_reflexao_etica()
        elif opcao == "0":
            print("\nEncerrando o Nucleo Cognitivo da Aurora Siger. Ate logo!")
            break
        else:
            print("\n[AVISO] Opcao invalida, tente novamente.")


if __name__ == "__main__":
    main()
