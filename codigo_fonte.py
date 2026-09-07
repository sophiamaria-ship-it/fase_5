"""
=======================================================================
 NUCLEO COGNITIVO DA AURORA SIGER (NCAS)
=======================================================================
Sistema de registro, organizacao, consulta e interpretacao de
informacoes operacionais da colonia Aurora Siger.

Conteudos aplicados neste projeto:
 - Manipulacao de arquivos texto e JSON (open, with, modos w/r/a/x/+)
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
ARQUIVO_MODULOS = "modulos_colonia.json"
ARQUIVO_ALERTAS = "alertas.json"
ARQUIVO_INTERACOES = "interacoes.json"
ARQUIVO_PROMPTS = "prompts.json"


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


def ler_ultimas_linhas_texto(n_linhas: int = 5) -> None:
    """Le as ultimas N linhas do arquivo texto usando readlines() e slice."""
    if not os.path.exists(ARQUIVO_TEXTO):
        print("\n[AVISO] Nenhum registro encontrado ainda.")
        return

    with open(ARQUIVO_TEXTO, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
    
    ultimas = linhas[-n_linhas:] if len(linhas) >= n_linhas else linhas
    
    print(f"\n--- ULTIMAS {len(ultimas)} LINHAS DO REGISTRO ---")
    for linha in ultimas:
        print(linha.rstrip("\n"))
    print("--- FIM DOS REGISTROS ---")


def gravar_multiplas_linhas(categoria: str, mensagens: list) -> None:
    """Grava multiplas linhas no arquivo texto usando writelines()."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linhas = []
    for msg in mensagens:
        linha = f"[{timestamp}] {categoria.upper()} | {msg}\n"
        linhas.append(linha)
    
    with open(ARQUIVO_TEXTO, "a", encoding="utf-8") as arquivo:
        arquivo.writelines(linhas)
    print(f"\n[OK] {len(linhas)} registros salvos em registros_colonia.txt")


# -----------------------------------------------------------------
# 3. FUNCOES DE MANIPULACAO DE ARQUIVO JSON
# -----------------------------------------------------------------
def carregar_dados_json(arquivo: str) -> dict:
    """Carrega o dicionario de dados a partir do arquivo JSON."""
    if not os.path.exists(arquivo):
        return {}
    
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados


def salvar_dados_json(arquivo: str, dados: dict) -> None:
    """Salva (sobrescreve) o dicionario de dados no arquivo JSON."""
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def inicializar_arquivos_json() -> None:
    """Inicializa todos os arquivos JSON com estrutura basica se nao existirem."""
    estruturas = {
        ARQUIVO_MODULOS: {"modulos": []},
        ARQUIVO_ALERTAS: {"alertas": []},
        ARQUIVO_INTERACOES: {"interacoes": []},
        ARQUIVO_PROMPTS: {"prompts": []}
    }
    
    for arquivo, estrutura in estruturas.items():
        if not os.path.exists(arquivo):
            salvar_dados_json(arquivo, estrutura)


def proximo_id(lista: list) -> int:
    """Gera um novo id sequencial simples para uma lista de dicionarios."""
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


# 3.1 Modulos da Colonia
def cadastrar_modulo() -> None:
    """Cadastra um novo modulo na estrutura JSON."""
    dados = carregar_dados_json(ARQUIVO_MODULOS)
    
    print("\n--- CADASTRO DE MODULO ---")
    nome = input("Nome do modulo: ").strip()
    status = input("Status (ativo/inativo/manutencao): ").strip().lower()
    responsavel = input("Responsavel: ").strip()
    setor = input("Setor: ").strip()
    
    novo_modulo = {
        "id": proximo_id(dados["modulos"]),
        "nome": nome,
        "status": status,
        "responsavel": responsavel,
        "setor": setor,
        "data_cadastro": datetime.now().strftime("%Y-%m-%d")
    }
    
    dados["modulos"].append(novo_modulo)
    salvar_dados_json(ARQUIVO_MODULOS, dados)
    gravar_registro_texto("MODULO", f"Novo modulo cadastrado: {nome} ({setor})")
    print("\n[OK] Modulo cadastrado com sucesso")


# 3.2 Alertas Operacionais
def cadastrar_alerta() -> None:
    """Cadastra um novo alerta operacional na estrutura JSON."""
    dados = carregar_dados_json(ARQUIVO_ALERTAS)
    
    print("\n--- CADASTRO DE ALERTA OPERACIONAL ---")
    modulo = input("Modulo afetado: ").strip()
    tipo_ocorrencia = input("Tipo de ocorrencia: ").strip()
    prioridade = input("Prioridade (baixa/media/alta/critica): ").strip().lower()
    mensagem = input("Mensagem resumida: ").strip()
    falha = input("Houve falha? (s/n): ").strip().lower() == "s"
    critico = input("E critico? (s/n): ").strip().lower() == "s"
    consumo_elevado = input("Consumo elevado? (s/n): ").strip().lower() == "s"
    
    novo_alerta = {
        "id": proximo_id(dados["alertas"]),
        "modulo": modulo,
        "tipo_ocorrencia": tipo_ocorrencia,
        "prioridade": prioridade,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "mensagem": mensagem,
        "falha": falha,
        "critico": critico,
        "consumo_elevado": consumo_elevado
    }
    
    dados["alertas"].append(novo_alerta)
    salvar_dados_json(ARQUIVO_ALERTAS, dados)
    gravar_registro_texto("ALERTA", f"Novo alerta no modulo {modulo} ({prioridade})")
    print("\n[OK] Alerta cadastrado com sucesso")


# 3.3 Interacoes do Assistente
def registrar_interacao(prompt: str, resposta: dict, contexto: str = "") -> None:
    """Registra uma interacao do assistente no arquivo JSON."""
    dados = carregar_dados_json(ARQUIVO_INTERACOES)
    
    interacao = {
        "id": proximo_id(dados["interacoes"]) if dados["interacoes"] else 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "contexto": contexto,
        "prompt": prompt,
        "resposta": resposta
    }
    
    dados["interacoes"].append(interacao)
    salvar_dados_json(ARQUIVO_INTERACOES, dados)


# -----------------------------------------------------------------
# 4. REGRAS LOGICAS E SIMPLIFICACAO BOOLEANA
# -----------------------------------------------------------------
"""
REGRA 1 - Geracao de alerta critico
    Original : ALERTA = (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)
    Simplificada (Teorema da Simplificacao / Absorcao):
        A.B + A.B' = A
    Aplicando: FALHA.CRITICO + FALHA.(NOT CRITICO) = FALHA
    Logo: ALERTA = FALHA
    Ou seja, o resultado depende apenas da existencia de falha,
    independentemente do valor de CRITICO. A simplificacao mantem o
    mesmo resultado logico porque, nos dois casos possiveis de
    CRITICO (verdadeiro ou falso), a saida so e verdadeira quando
    FALHA e verdadeira.

REGRA 2 - Gerar alerta se houver falha critica OU consumo elevado
    Original : ALERTA_GERAL = (FALHA AND CRITICO) OR CONSUMO_ELEVADO
    Simplificada: Nao e possivel simplificar usando De Morgan ou 
    Simplificacao direta, pois nao ha termos comuns.

REGRA 3 - Bloqueio de operacao (demonstracao de De Morgan)
    Original: BLOQUEAR = NOT (AUTORIZADO AND MODULO_ATIVO)
    Por De Morgan: NOT (A AND B) = (NOT A) OR (NOT B)
    Logo: BLOQUEAR = (NOT AUTORIZADO) OR (NOT MODULO_ATIVO)
"""
def verificar_alerta_critico(falha: bool, critico: bool) -> bool:
    """Regra simplificada: ALERTA = FALHA."""
    alerta_original = (falha and critico) or (falha and not critico)
    alerta_simplificado = falha
    
    # Demonstracao de que a simplificacao mantem o mesmo resultado
    print("\n[Demonstracao da simplificacao]")
    print(f"Original: (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO) = {alerta_original}")
    print(f"Simplificado: FALHA = {alerta_simplificado}")
    
    # Verificacao de equivalencia
    if alerta_original == alerta_simplificado:
        print("✓ A simplificacao mantem o mesmo resultado logico")
    else:
        print("✗ ATENCAO: Os resultados nao sao equivalentes!")
    
    return alerta_simplificado


def verificar_alerta_geral(falha: bool, critico: bool, consumo_elevado: bool) -> bool:
    """Regra: ALERTA_GERAL = (FALHA AND CRITICO) OR CONSUMO_ELEVADO."""
    return (falha and critico) or consumo_elevado


def bloquear_operacao(autorizado: bool, modulo_ativo: bool) -> bool:
    """Bloqueio usando De Morgan: BLOQUEAR = NOT (AUTORIZADO AND MODULO_ATIVO)."""
    bloqueio_original = not (autorizado and modulo_ativo)
    bloqueio_de_morgan = (not autorizado) or (not modulo_ativo)
    
    # Demonstracao de De Morgan
    print("\n[Demonstracao de De Morgan]")
    print(f"Original: NOT (AUTORIZADO AND MODULO_ATIVO) = {bloqueio_original}")
    print(f"De Morgan: (NOT AUTORIZADO) OR (NOT MODULO_ATIVO) = {bloqueio_de_morgan}")
    
    # Verificacao de equivalencia
    if bloqueio_original == bloqueio_de_morgan:
        print("✓ Aplicacao de De Morgan correta")
    else:
        print("✗ ATENCAO: Os resultados nao sao equivalentes!")
    
    return bloqueio_de_morgan


# 4.1 Regra para priorizar atendimento
def priorizar_atendimento(urgente: bool, setor_essencial: bool, disponibilidade: bool) -> bool:
    """
    Priorizar atendimento se (pedido URGENTE AND setor_ESSENCIAL) OR 
    (pedido URGENTE AND disponibilidade_TRUE)
    
    Simplificacao por absorcao: 
    URGENTE AND (ESSENCIAL OR DISPONIVEL)
    """
    prioridade_original = (urgente and setor_essencial) or (urgente and disponibilidade)
    prioridade_simplificada = urgente and (setor_essencial or disponibilidade)
    
    print("\n[Demonstracao da simplificacao - Priorizacao]")
    print(f"Original: (URGENTE AND ESSENCIAL) OR (URGENTE AND DISPONIVEL) = {prioridade_original}")
    print(f"Simplificado: URGENTE AND (ESSENCIAL OR DISPONIVEL) = {prioridade_simplificada}")
    
    if prioridade_original == prioridade_simplificada:
        print("✓ A simplificacao mantem o mesmo resultado logico")
    else:
        print("✗ ATENCAO: Os resultados nao sao equivalentes!")
    
    return prioridade_simplificada


def executar_validacao_logica() -> None:
    """Menu para testar as regras logicas do sistema."""
    print("\n--- VALIDACAO LOGICA ---")
    print("1 - Verificar alerta critico (Simplificacao: ALERTA = FALHA)")
    print("2 - Verificar alerta geral ((FALHA AND CRITICO) OR CONSUMO)")
    print("3 - Verificar bloqueio de operacao (De Morgan)")
    print("4 - Verificar priorizacao de atendimento")
    print("5 - Explicacao das regras e simplificacoes")
    opcao = input("Escolha uma opcao: ").strip()
    
    if opcao == "1":
        falha = input("Houve falha? (s/n): ").strip().lower() == "s"
        critico = input("E critico? (s/n): ").strip().lower() == "s"
        resultado = verificar_alerta_critico(falha, critico)
        print(f"\nResultado -> ALERTA_CRITICO = {resultado}")
    
    elif opcao == "2":
        falha = input("Houve falha? (s/n): ").strip().lower() == "s"
        critico = input("E critico? (s/n): ").strip().lower() == "s"
        consumo = input("Consumo elevado? (s/n): ").strip().lower() == "s"
        resultado = verificar_alerta_geral(falha, critico, consumo)
        print(f"\nResultado -> ALERTA_GERAL = {resultado}")
    
    elif opcao == "3":
        autorizado = input("Usuario autorizado? (s/n): ").strip().lower() == "s"
        ativo = input("Modulo ativo? (s/n): ").strip().lower() == "s"
        resultado = bloquear_operacao(autorizado, ativo)
        print(f"\nResultado -> BLOQUEAR_OPERACAO = {resultado}")
    
    elif opcao == "4":
        urgente = input("Solicitacao urgente? (s/n): ").strip().lower() == "s"
        essencial = input("Setor essencial? (s/n): ").strip().lower() == "s"
        disponivel = input("Disponivel para atendimento? (s/n): ").strip().lower() == "s"
        resultado = priorizar_atendimento(urgente, essencial, disponivel)
        print(f"\nResultado -> PRIORIZAR_ATENDIMENTO = {resultado}")
    
    elif opcao == "5":
        explicar_regras()
    else:
        print("\n[AVISO] Opcao invalida.")


def explicar_regras() -> None:
    """Exibe explicacao detalhada das regras e simplificacoes."""
    texto = """
--- EXPLICACAO DAS REGRAS LOGICAS E SIMPLIFICACOES ---

REGRA 1: Alerta Critico
    Expressao original: ALERTA = (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)
    Simplificacao: ALERTA = FALHA
    Teorema utilizado: A.B + A.B' = A (Teorema da Simplificacao/Absorcao)
    Por que funciona: 
        - Se FALHA = False, ambas as partes da expressao original sao False
        - Se FALHA = True, a expressao se reduz a CRITICO OR NOT CRITICO = True
    Portanto, o resultado depende apenas de FALHA.

REGRA 2: Alerta Geral
    Expressao: ALERTA_GERAL = (FALHA AND CRITICO) OR CONSUMO_ELEVADO
    Nao simplificavel: Os termos (FALHA AND CRITICO) e CONSUMO_ELEVADO
    sao independentes. Nao ha termos comuns para fatoracao.

REGRA 3: Bloqueio de Operacao (De Morgan)
    Expressao original: BLOQUEAR = NOT (AUTORIZADO AND MODULO_ATIVO)
    Aplicacao de De Morgan: NOT (A AND B) = (NOT A) OR (NOT B)
    Resultado: BLOQUEAR = (NOT AUTORIZADO) OR (NOT MODULO_ATIVO)
    Significado: A operacao e bloqueada se o usuario nao for autorizado
    OU se o modulo nao estiver ativo.

REGRA 4: Priorizacao de Atendimento
    Expressao original: PRIORIZAR = (URGENTE AND ESSENCIAL) OR (URGENTE AND DISPONIVEL)
    Simplificacao por fatoracao: PRIORIZAR = URGENTE AND (ESSENCIAL OR DISPONIVEL)
    Significado: Priorizamos atendimento se for URGENTE e (o setor for ESSENCIAL
    ou estiver DISPONIVEL para atendimento).
"""
    print(texto)


# -----------------------------------------------------------------
# 5. ENGENHARIA DE PROMPTS E SIMULACAO DE IA GENERATIVA
# -----------------------------------------------------------------
# Nao ha integracao real com API de IA (opcional segundo o enunciado).
# As respostas sao simuladas localmente por meio de templates de
# texto, preservando a logica e a estrutura de um prompt real.

# 5.1 Prompts Estruturados
PROMPTS = {
    "zero_shot": {
        "nome": "Resumo de Alerta Operacional",
        "template": (
            "Voce e o assistente do Nucleo Cognitivo da Aurora Siger. "
            "Resuma o alerta operacional a seguir em ate 2 frases, "
            "destacando o modulo afetado e o nivel de risco.\n\n"
            "Alerta: {alerta_mensagem}"
        ),
        "descricao": "Prompt zero-shot para resumir alertas sem exemplos previos"
    },
    "few_shot": {
        "nome": "Classificacao de Solicitacao",
        "template": (
            "Classifique a solicitacao da tripulacao em uma das categorias: "
            "URGENTE, ROTINA ou INFORMATIVA.\n\n"
            "Exemplo 1:\n"
            "Solicitacao: 'Vazamento de oxigenio no modulo 2 - risco imediato'\n"
            "Categoria: URGENTE\n\n"
            "Exemplo 2:\n"
            "Solicitacao: 'Relatorio semanal de consumo de agua'\n"
            "Categoria: ROTINA\n\n"
            "Exemplo 3:\n"
            "Solicitacao: 'Comunicado sobre treinamento de novos tripulantes'\n"
            "Categoria: INFORMATIVA\n\n"
            "Agora classifique:\n"
            "Solicitacao: '{solicitacao_descricao}'\n"
            "Categoria:"
        ),
        "descricao": "Prompt few-shot com 3 exemplos para classificar solicitacoes"
    },
    "saida_estruturada": {
        "nome": "Resposta Estruturada em JSON",
        "template": (
            "Gere uma resposta padronizada ao centro de controle em formato JSON, "
            "com os campos: modulo, nivel_risco, recomendacao, prioridade, "
            "data_estimada, e acao_imediata, a partir do seguinte alerta:\n\n"
            "Modulo: {modulo}\n"
            "Tipo: {tipo}\n"
            "Prioridade: {prioridade}\n"
            "Mensagem: {mensagem}\n\n"
            "Responda apenas com um objeto JSON valido."
        ),
        "descricao": "Prompt para gerar saida estruturada em JSON com campos especificos"
    },
    "linguagem_simples": {
        "nome": "Traducao para Linguagem Simples",
        "template": (
            "Transforme o seguinte registro tecnico em linguagem simples "
            "e compreensivel para todos os tripulantes:\n\n"
            "Registro tecnico: {registro_tecnico}\n\n"
            "Versao em linguagem simples:"
        ),
        "descricao": "Prompt para traduzir jargao tecnico em linguagem acessivel"
    }
}


def exibir_prompts() -> None:
    """Exibe os prompts estruturados criados pela equipe."""
    print("\n--- PROMPTS ESTRUTURADOS DO NCAS ---")
    print("\n" + "="*60)
    
    # Zero-shot
    print("\n[ZERO-SHOT]")
    print(f"Nome: {PROMPTS['zero_shot']['nome']}")
    print(f"Descricao: {PROMPTS['zero_shot']['descricao']}")
    print(f"Template:\n{PROMPTS['zero_shot']['template']}")
    
    # Few-shot
    print("\n" + "="*60)
    print("\n[FEW-SHOT]")
    print(f"Nome: {PROMPTS['few_shot']['nome']}")
    print(f"Descricao: {PROMPTS['few_shot']['descricao']}")
    print(f"Template:\n{PROMPTS['few_shot']['template']}")
    
    # Saida Estruturada
    print("\n" + "="*60)
    print("\n[SAIDA ESTRUTURADA]")
    print(f"Nome: {PROMPTS['saida_estruturada']['nome']}")
    print(f"Descricao: {PROMPTS['saida_estruturada']['descricao']}")
    print(f"Template:\n{PROMPTS['saida_estruturada']['template']}")
    
    # Linguagem Simples
    print("\n" + "="*60)
    print("\n[LINGUAGEM SIMPLES]")
    print(f"Nome: {PROMPTS['linguagem_simples']['nome']}")
    print(f"Descricao: {PROMPTS['linguagem_simples']['descricao']}")
    print(f"Template:\n{PROMPTS['linguagem_simples']['template']}")
    
    print("\n" + "="*60)


def simular_resposta_ia(tipo_prompt: str, **kwargs) -> dict:
    """Simula localmente a resposta do assistente inteligente."""
    
    if tipo_prompt == "zero_shot":
        # Simula classificacao de alerta
        mensagem = kwargs.get('alerta_mensagem', 'Alerta nao especificado')
        
        # Regras simuladas para resposta
        if 'critico' in mensagem.lower() or 'falha' in mensagem.lower():
            nivel_risco = "ALTO"
            recomendacao = "Acionar equipe de emergencia imediatamente"
        elif 'atencao' in mensagem.lower() or 'manutencao' in mensagem.lower():
            nivel_risco = "MEDIO"
            recomendacao = "Agendar verificacao tecnica"
        else:
            nivel_risco = "BAIXO"
            recomendacao = "Monitorar e documentar ocorrencia"
        
        return {
            "tipo": "zero_shot",
            "resumo": f"Alerta detectado: {mensagem[:50]}...",
            "nivel_risco": nivel_risco,
            "recomendacao": recomendacao,
            "modulo_afetado": kwargs.get('modulo', 'Nao especificado')
        }
    
    elif tipo_prompt == "few_shot":
        # Simula classificacao de solicitacao
        descricao = kwargs.get('solicitacao_descricao', '')
        descricao_lower = descricao.lower()
        
        if any(palavra in descricao_lower for palavra in ['vazamento', 'falha', 'risco', 'urgente']):
            categoria = "URGENTE"
        elif any(palavra in descricao_lower for palavra in ['relatorio', 'consumo', 'verificacao']):
            categoria = "ROTINA"
        else:
            categoria = "INFORMATIVA"
        
        return {
            "tipo": "few_shot",
            "categoria": categoria,
            "classificacao": f"Solicitacao classificada como {categoria}",
            "justificativa": f"Baseado na analise do conteudo: '{descricao[:30]}...'"
        }
    
    elif tipo_prompt == "saida_estruturada":
        # Simula saida JSON estruturada
        modulo = kwargs.get('modulo', 'Nao especificado')
        prioridade = kwargs.get('prioridade', 'media')
        mensagem = kwargs.get('mensagem', '')
        
        nivel_risco_map = {
            'critica': 'CRITICO',
            'alta': 'ALTO',
            'media': 'MEDIO',
            'baixa': 'BAIXO'
        }
        
        return {
            "tipo": "saida_estruturada",
            "resposta": {
                "modulo": modulo,
                "nivel_risco": nivel_risco_map.get(prioridade, 'MEDIO'),
                "recomendacao": f"Para o modulo {modulo}, recomenda-se verificacao tecnica imediata",
                "prioridade": prioridade,
                "data_estimada": datetime.now().strftime("%Y-%m-%d"),
                "acao_imediata": "Isolar modulo e acionar equipe" if prioridade == 'critica' else "Monitorar modulo"
            }
        }
    
    elif tipo_prompt == "linguagem_simples":
        # Simula traducao para linguagem simples
        registro = kwargs.get('registro_tecnico', '')
        
        # Simula traducao removendo jargao
        traducao = registro.replace('falha critica', 'problema grave')
        traducao = traducao.replace('consumo elevado', 'gasto alto de energia')
        traducao = traducao.replace('manutencao preventiva', 'verificacao de rotina')
        traducao = traducao.replace('parametros', 'medidas')
        traducao = traducao.replace('sistema operacional', 'sistema que esta rodando')
        
        return {
            "tipo": "linguagem_simples",
            "original": registro,
            "traducao": traducao,
            "nivel_complexidade": "Nivel 1 - Compreensivel para todos"
        }
    
    else:
        return {"erro": "Tipo de prompt nao reconhecido"}


def analisar_alerta_operacional() -> None:
    """Funcionalidade principal integrada do sistema."""
    dados = carregar_dados_json(ARQUIVO_ALERTAS)
    
    if not dados.get("alertas"):
        print("\n[AVISO] Nao ha alertas cadastrados.")
        return
    
    print("\n--- ALERTAS DISPONIVEIS ---")
    for alerta in dados["alertas"]:
        print(f"[{alerta['id']}] {alerta['modulo']} - {alerta['tipo_ocorrencia']} | {alerta['prioridade']}")
    
    try:
        id_escolhido = int(input("\nDigite o id do alerta a analisar: "))
    except ValueError:
        print("\n[AVISO] Id invalido.")
        return
    
    alerta = next((a for a in dados["alertas"] if a["id"] == id_escolhido), None)
    if alerta is None:
        print("\n[AVISO] Alerta nao encontrado.")
        return
    
    print(f"\n--- ANALISANDO ALERTA {id_escolhido} ---")
    print(f"Modulo: {alerta['modulo']}")
    print(f"Tipo: {alerta['tipo_ocorrencia']}")
    print(f"Prioridade: {alerta['prioridade']}")
    print(f"Mensagem: {alerta['mensagem']}")
    print(f"Falha: {alerta['falha']}")
    print(f"Critico: {alerta['critico']}")
    print(f"Consumo elevado: {alerta.get('consumo_elevado', False)}")
    
    # 1) Aplica regra logica simplificada
    alerta_critico = verificar_alerta_critico(alerta["falha"], alerta["critico"])
    alerta_geral = verificar_alerta_geral(alerta["falha"], alerta["critico"], alerta.get('consumo_elevado', False))
    
    print(f"\n[REGRA SIMPLIFICADA] ALERTA_CRITICO = {alerta_critico}")
    print(f"[REGRA GERAL] ALERTA_GERAL = {alerta_geral}")
    
    # 2) Simula resposta com diferentes prompts
    print("\n--- SIMULACAO DE RESPOSTAS COM PROMPTS ---")
    
    # Zero-shot
    print("\n[ZERO-SHOT PROMPT]")
    prompt_zs = PROMPTS["zero_shot"]["template"].format(
        alerta_mensagem=f"{alerta['modulo']}: {alerta['mensagem']}"
    )
    print(f"Prompt:\n{prompt_zs}")
    resposta_zs = simular_resposta_ia("zero_shot", 
                                      alerta_mensagem=alerta['mensagem'],
                                      modulo=alerta['modulo'])
    print(f"Resposta:\n{json.dumps(resposta_zs, indent=2, ensure_ascii=False)}")
    
    # Few-shot
    print("\n[FEW-SHOT PROMPT]")
    prompt_fs = PROMPTS["few_shot"]["template"].format(
        solicitacao_descricao=f"{alerta['modulo']}: {alerta['tipo_ocorrencia']}"
    )
    print(f"Prompt:\n{prompt_fs}")
    resposta_fs = simular_resposta_ia("few_shot", 
                                      solicitacao_descricao=f"{alerta['tipo_ocorrencia']}: {alerta['mensagem']}")
    print(f"Resposta:\n{json.dumps(resposta_fs, indent=2, ensure_ascii=False)}")
    
    # Saida Estruturada
    print("\n[SAIDA ESTRUTURADA PROMPT]")
    prompt_se = PROMPTS["saida_estruturada"]["template"].format(
        modulo=alerta['modulo'],
        tipo=alerta['tipo_ocorrencia'],
        prioridade=alerta['prioridade'],
        mensagem=alerta['mensagem']
    )
    print(f"Prompt:\n{prompt_se}")
    resposta_se = simular_resposta_ia("saida_estruturada",
                                      modulo=alerta['modulo'],
                                      prioridade=alerta['prioridade'],
                                      mensagem=alerta['mensagem'])
    print(f"Resposta:\n{json.dumps(resposta_se['resposta'], indent=2, ensure_ascii=False)}")
    
    # Registrar interacoes
    registrar_interacao(prompt_zs, resposta_zs, "zero_shot")
    registrar_interacao(prompt_fs, resposta_fs, "few_shot")
    registrar_interacao(prompt_se, resposta_se['resposta'], "saida_estruturada")
    
    gravar_registro_texto("ANALISE_ALERTA", f"Alerta {alerta['id']} do modulo {alerta['modulo']} analisado")


# -----------------------------------------------------------------
# 6. MEMORIA, ARMAZENAMENTO E FLUXO DE DADOS
# -----------------------------------------------------------------
def explicar_memoria_armazenamento() -> None:
    texto = """
--- MEMORIA, ARMAZENAMENTO E FLUXO DE DADOS NO NCAS ---

Como o NCAS utiliza armazenamento e acesso aos dados:

1. MEMORIA RAM (Volatil):
   - Durante a execucao, os dados sao carregados da memoria de 
     massa (disco) para a RAM através das funcoes carregar_dados_json().
   - Os dicionarios Python ficam armazenados na memoria RAM 
     enquanto o programa esta rodando.
   - A RAM e rapida mas volatil - ao desligar o computador, 
     os dados sao perdidos se nao forem salvos.

2. ARMAZENAMENTO (Disco - Persistente):
   - Arquivos JSON e TXT ficam armazenados fisicamente no disco 
     (HD ou SSD).
   - Dados em disco sao persistentes - mantem-se mesmo apos o 
     programa ser encerrado.
   - Os arquivos sao abertos em diferentes modos:
     * 'r' (read) - leitura de dados existentes
     * 'w' (write) - escrita/sobrescrita de dados
     * 'a' (append) - adicao ao final do arquivo

3. FLUXO DE DADOS:
   Cadastro: Entrada do usuario → Dicionario em RAM → 
             Escrita (write) → Arquivo em disco → Confirmacao
   
   Consulta: Requisicao → Leitura (read) → Arquivo em disco → 
             Dicionario em RAM → Exibicao
   
   Acesso: Dicionario → JSON → Disco
   Leitura: Disco → JSON → Dicionario

4. BARRAMENTOS:
   - Dados trafegam pelos barramentos do computador durante a 
     leitura/escrita entre RAM e disco.
   - A velocidade de acesso varia conforme o tipo de barramento 
     (SATA, PCIe, etc.)

5. GERENCIADOR DE CONTEXTO (with):
   - Utilizamos 'with open()' para garantir que os arquivos sejam 
     fechados automaticamente apos o uso.
   - Isso previne vazamento de memoria e corrupcao de dados.

6. EXEMPLO PRATICO NO NCAS:
   a) Usuario cadastra alerta → dados em RAM
   b) Chamada salvar_dados_json() → escrita no disco
   c) Programa encerra → dados persistem no disco
   d) Nova execucao → carregar_dados_json() → leitura do disco para RAM

Este fluxo garante que todas as informacoes da colonia Aurora Siger 
sejam preservadas e acessiveis quando necessario.
"""
    print(texto)


# -----------------------------------------------------------------
# 7. DIVERSIDADE, ETICA E RESPONSABILIDADE NO USO DA IA
# -----------------------------------------------------------------
def exibir_reflexao_etica() -> None:
    texto = """
--- DIVERSIDADE, ETICA E RESPONSABILIDADE NO NCAS ---

1. RISCOS DE RESPOSTAS ENVIESADAS:
   - Se treinado com dados nao representativos, o sistema pode 
     priorizar indevidamente certos modulos ou setores.
   - Exemplo: Priorizar sempre o modulo 1 sem considerar que o 
     modulo 2 tambem tem necessidades urgentes.
   - O NCAS mitiga isso usando regras objetivas baseadas em 
     dados (falha, criticidade, consumo) e nao em preferencias.

2. IMPORTANCIA DA DIVERSIDADE NO DESENVOLVIMENTO:
   - Equipes diversas identificam mais pontos cegos.
   - Diferentes perspectivas levam a sistemas mais justos e 
     abrangentes.
   - A diversidade inclui genero, etnia, habilidades tecnicas 
     e experiencias profissionais.

3. LINGUAGEM DISCRIMINATORIA:
   - O NCAS utiliza linguagem neutra e tecnica.
   - Todas as solicitacoes sao tratadas com os mesmos criterios 
     objetivos.
   - Nao ha associacao de caracteristicas pessoais com 
     competencia ou prioridade.

4. IMPACTOS SOCIAIS DE DECISOES AUTOMATIZADAS:
   - Decisoes criticas (isolar modulo, bloquear operacao) 
     permanecem sob responsabilidade humana.
   - O sistema atua como assistente, nao como tomador de decisoes 
     finais.
   - Recomendacoes sao claras e auditaveis.

5. RESPONSABILIDADE HUMANA NO USO DE IA GENERATIVA:
   - O NCAS simula IA, deixando claro que as respostas sao 
     baseadas em regras predefinidas.
   - Em sistemas reais, e essencial ter supervisao humana.
   - A transparencia e a explicabilidade sao fundamentais.

6. RACISMO ESTRUTURAL E IA:
   - Sistemas podem perpetuar vieses raciais se treinados com 
     dados historicos tendenciosos.
   - No NCAS, evitamos qualquer associacao entre caracteristicas 
     pessoais e capacidades tecnicas.
   - Tratamento igualitario e baseado apenas em criterios 
     operacionais objetivos.

7. COMPROMISSO DO NCAS:
   - Transparencia nas decisoes
   - Igualdade no tratamento de solicitacoes
   - Supervisao humana em decisoes criticas
   - Auditoria regular das regras e decisoes
   - Melhoria continua baseada em feedback

"Desenvolvemos o NCAS para apoiar, nao substituir, o julgamento 
humano. A tecnologia deve servir a todos da colonia com equidade, 
transparencia e responsabilidade."
"""
    print(texto)


# -----------------------------------------------------------------
# 8. CONSULTAS E EXIBICAO DE DADOS
# -----------------------------------------------------------------
def consultar_dados_completos() -> None:
    """Exibe todos os dados organizados dos arquivos JSON."""
    print("\n--- CONSULTA COMPLETA DE DADOS ---")
    
    # Modulos
    dados_modulos = carregar_dados_json(ARQUIVO_MODULOS)
    print("\n--- MODULOS DA COLONIA ---")
    if dados_modulos.get("modulos"):
        for modulo in dados_modulos["modulos"]:
            print(f"[{modulo['id']}] {modulo['nome']} | Status: {modulo['status']} | "
                  f"Responsavel: {modulo['responsavel']} | Setor: {modulo['setor']}")
    else:
        print("Nenhum modulo cadastrado.")
    
    # Alertas
    dados_alertas = carregar_dados_json(ARQUIVO_ALERTAS)
    print("\n--- ALERTAS OPERACIONAIS ---")
    if dados_alertas.get("alertas"):
        for alerta in dados_alertas["alertas"]:
            print(f"[{alerta['id']}] {alerta['modulo']} | {alerta['tipo_ocorrencia']} | "
                  f"Prioridade: {alerta['prioridade']} | Falha: {alerta['falha']} | "
                  f"Critico: {alerta['critico']}")
    else:
        print("Nenhum alerta cadastrado.")
    
    # Interacoes
    dados_interacoes = carregar_dados_json(ARQUIVO_INTERACOES)
    print("\n--- INTERACOES DO ASSISTENTE ---")
    if dados_interacoes.get("interacoes"):
        for interacao in dados_interacoes["interacoes"][-5:]:  # Ultimas 5
            print(f"[{interacao['id']}] {interacao['timestamp']} | {interacao['contexto']}")
    else:
        print("Nenhuma interacao registrada.")


def consultar_filtrado() -> None:
    """Consulta dados com filtros."""
    print("\n--- CONSULTA FILTRADA ---")
    print("1 - Alertas por prioridade")
    print("2 - Modulos por status")
    print("3 - Solicitacoes urgentes")
    opcao = input("Escolha uma opcao: ").strip()
    
    if opcao == "1":
        prioridade = input("Prioridade (baixa/media/alta/critica): ").strip().lower()
        dados = carregar_dados_json(ARQUIVO_ALERTAS)
        filtrados = [a for a in dados.get("alertas", []) if a["prioridade"] == prioridade]
        
        print(f"\n--- ALERTAS COM PRIORIDADE {prioridade.upper()} ---")
        for alerta in filtrados:
            print(f"[{alerta['id']}] {alerta['modulo']} - {alerta['tipo_ocorrencia']}")
    
    elif opcao == "2":
        status = input("Status (ativo/inativo/manutencao): ").strip().lower()
        dados = carregar_dados_json(ARQUIVO_MODULOS)
        filtrados = [m for m in dados.get("modulos", []) if m["status"] == status]
        
        print(f"\n--- MODULOS COM STATUS {status.upper()} ---")
        for modulo in filtrados:
            print(f"[{modulo['id']}] {modulo['nome']} - Responsavel: {modulo['responsavel']}")
    
    elif opcao == "3":
        # Simulando solicitacoes urgentes (usando alertas criticos)
        dados = carregar_dados_json(ARQUIVO_ALERTAS)
        filtrados = [a for a in dados.get("alertas", []) if a["critico"]]
        
        print("\n--- SOLICITACOES URGENTES (ALERTAS CRITICOS) ---")
        for alerta in filtrados:
            print(f"[{alerta['id']}] {alerta['modulo']} - {alerta['tipo_ocorrencia']} | {alerta['mensagem']}")
    
    else:
        print("\n[AVISO] Opcao invalida.")


# -----------------------------------------------------------------
# 9. MENU PRINCIPAL DO SISTEMA
# -----------------------------------------------------------------
def exibir_menu() -> None:
    print("\n" + "="*60)
    print(" NUCLEO COGNITIVO DA AURORA SIGER (NCAS)")
    print("="*60)
    print("1 - Cadastrar Modulo (JSON)")
    print("2 - Cadastrar Alerta (JSON)")
    print("3 - Cadastrar Registro de Manutencao (TEXTO)")
    print("4 - Cadastrar Multiplos Registros (TEXTO - writelines)")
    print("5 - Consultar Registros de Texto (readlines)")
    print("6 - Consultar Ultimas Linhas (readlines com slice)")
    print("7 - Consultar Dados JSON Completos")
    print("8 - Consultar Dados com Filtros")
    print("9 - Analisar Alerta (Regra + Prompts + IA Simulada)")
    print("10 - Executar Validacao Logica")
    print("11 - Exibir Prompts Estruturados")
    print("12 - Explicar Memoria e Armazenamento")
    print("13 - Reflexao sobre Diversidade e Etica")
    print("0 - Sair")
    print("-"*60)


def main() -> None:
    """Funcao principal do sistema."""
    # Inicializa arquivos
    inicializar_arquivos_json()
    if not os.path.exists(ARQUIVO_TEXTO):
        open(ARQUIVO_TEXTO, "a", encoding="utf-8").close()
    
    print("\n=== NUCLEO COGNITIVO DA AURORA SIGER ===")
    print("Sistema iniciado com sucesso!")
    
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opcao: ").strip()
        
        if opcao == "1":
            cadastrar_modulo()
        
        elif opcao == "2":
            cadastrar_alerta()
        
        elif opcao == "3":
            modulo = input("Modulo: ").strip()
            descricao = input("Descricao da manutencao: ").strip()
            gravar_registro_texto("MANUTENCAO", f"Modulo {modulo} | {descricao}")
        
        elif opcao == "4":
            categoria = input("Categoria: ").strip()
            print("Digite as mensagens (digite 'FIM' para terminar):")
            mensagens = []
            while True:
                msg = input("> ").strip()
                if msg.upper() == "FIM":
                    break
                if msg:
                    mensagens.append(msg)
            if mensagens:
                gravar_multiplas_linhas(categoria, mensagens)
            else:
                print("\n[AVISO] Nenhuma mensagem registrada.")
        
        elif opcao == "5":
            ler_registros_texto()
        
        elif opcao == "6":
            try:
                n = int(input("Numero de ultimas linhas: "))
            except ValueError:
                n = 5
            ler_ultimas_linhas_texto(n)
        
        elif opcao == "7":
            consultar_dados_completos()
        
        elif opcao == "8":
            consultar_filtrado()
        
        elif opcao == "9":
            analisar_alerta_operacional()
        
        elif opcao == "10":
            executar_validacao_logica()
        
        elif opcao == "11":
            exibir_prompts()
        
        elif opcao == "12":
            explicar_memoria_armazenamento()
        
        elif opcao == "13":
            exibir_reflexao_etica()
        
        elif opcao == "0":
            print("\nEncerrando o Nucleo Cognitivo da Aurora Siger.")
            print("Dados salvos com sucesso. Ate logo!")
            break
        
        else:
            print("\n[AVISO] Opcao invalida, tente novamente.")


if __name__ == "__main__":
    main()