# NCAS — Núcleo Cognitivo da Aurora Siger

Sistema em Python, via terminal, para **registrar, organizar, consultar e interpretar informações operacionais** de uma colônia espacial fictícia (Aurora Siger). O projeto aplica manipulação de arquivos texto e JSON, álgebra booleana/simplificação lógica, engenharia de prompts e simulação de um assistente de IA, além de uma reflexão sobre ética e diversidade no uso de IA.

> Projeto acadêmico — não há integração real com nenhuma API de IA. As "respostas do assistente" são simuladas localmente por regras e templates de texto.

---

## ✨ Funcionalidades

- **Cadastro e consulta de módulos** da colônia (JSON)
- **Cadastro e consulta de alertas operacionais** (JSON)
- **Registro de manutenção e acesso** em log de texto simples (append)
- **Consulta filtrada** (por prioridade, status ou alertas críticos/urgentes)
- **Regras lógicas com simplificação booleana** (Teorema da Simplificação e De Morgan), com demonstração de equivalência em tempo real
- **Prompts estruturados** (zero-shot, few-shot, saída estruturada em JSON, tradução para linguagem simples)
- **Análise integrada de alerta**: aplica a regra lógica, monta os prompts com os dados reais do alerta e simula a resposta da IA, registrando tudo no histórico de interações
- **Explicação de memória e armazenamento** (fluxo RAM ↔ disco)
- **Reflexão sobre diversidade, ética e responsabilidade no uso de IA**

---

## 🗂️ Estrutura de arquivos

| Arquivo | Formato | Conteúdo |
|---|---|---|
| `codigo_fonte.py` | Python | Código-fonte principal do sistema |
| `modulos_colonia.json` | JSON | Módulos cadastrados (`id`, `nome`, `status`, `responsavel`, `setor`, `data_cadastro`) |
| `alertas.json` | JSON | Alertas operacionais (`id`, `modulo`, `tipo_ocorrencia`, `prioridade`, `data`, `mensagem`, `falha`, `critico`, `consumo_elevado`) |
| `interacoes.json` | JSON | Histórico de interações com o assistente simulado (`id`, `timestamp`, `contexto`, `prompt`, `resposta`) |
| `dados_colonia.json` | JSON | Arquivo genérico de dados (criado se necessário) |
| `registros_colonia.txt` | Texto | Log cronológico simples (`[timestamp] CATEGORIA | mensagem`) |
| `prompts.json` | JSON | Estrutura auxiliar inicializada pelo sistema |
| `gerar_mock.py` | Python | Script auxiliar opcional para gerar dados de teste/demonstração |

**Por que JSON e por que texto puro?**
Dados estruturados com múltiplos campos (módulos, alertas, interações) ficam em JSON, pois precisam ser lidos, filtrados e atualizados por chave. Já os logs (manutenção, acesso) são apenas linhas sequenciais que só precisam ser adicionadas e lidas em ordem — por isso vão para arquivo de texto puro.

---

## ▶️ Como executar

Requer apenas **Python 3** (sem dependências externas).

```bash
python codigo_fonte.py
```

Na primeira execução, o sistema cria automaticamente os arquivos JSON (com estrutura vazia) e o arquivo de texto, caso ainda não existam.

### Gerando dados de exemplo (opcional)

Para já começar com módulos, alertas, interações e logs de exemplo (útil para testar consultas, filtros e a análise de alerta sem precisar cadastrar tudo manualmente):

```bash
python gerar_mock.py
python codigo_fonte.py
```

---

## 🖥️ Menu principal

```
1  - Cadastrar Modulo (JSON)
2  - Cadastrar Alerta (JSON)
3  - Cadastrar Registro de Manutencao (TEXTO)
4  - Cadastrar Multiplos Registros (TEXTO - writelines)
5  - Consultar Registros de Texto (readlines)
6  - Consultar Ultimas Linhas (readlines com slice)
7  - Consultar Dados JSON Completos
8  - Consultar Dados com Filtros
9  - Analisar Alerta (Regra + Prompts + IA Simulada)
10 - Executar Validacao Logica
11 - Exibir Prompts Estruturados
12 - Explicar Memoria e Armazenamento
13 - Reflexao sobre Diversidade e Etica
0  - Sair
```

A opção **10** abre um submenu com 5 validações lógicas (alerta crítico, alerta geral, bloqueio de operação/De Morgan, priorização de atendimento e explicação das regras).

---

## 🧮 Regras lógicas implementadas

| Regra | Expressão original | Simplificação | Teorema |
|---|---|---|---|
| Alerta crítico | `(FALHA ∧ CRÍTICO) ∨ (FALHA ∧ ¬CRÍTICO)` | `ALERTA = FALHA` | Simplificação/Absorção (A·B + A·B' = A) |
| Alerta geral | `(FALHA ∧ CRÍTICO) ∨ CONSUMO_ELEVADO` | Não simplificável (termos independentes) | — |
| Bloqueio de operação | `¬(AUTORIZADO ∧ MÓDULO_ATIVO)` | `¬AUTORIZADO ∨ ¬MÓDULO_ATIVO` | De Morgan |
| Priorização de atendimento | `(URGENTE ∧ ESSENCIAL) ∨ (URGENTE ∧ DISPONÍVEL)` | `URGENTE ∧ (ESSENCIAL ∨ DISPONÍVEL)` | Fatoração/Absorção |

Cada regra é executada com a expressão original e a simplificada lado a lado, verificando em tempo real se os resultados são equivalentes.

---

## 🤖 Prompts estruturados

O sistema define 4 templates de prompt (usados na função `analisar_alerta_operacional()` e listados na opção 11):

1. **Zero-shot** — resume um alerta operacional sem exemplos prévios.
2. **Few-shot** — classifica uma solicitação em `URGENTE`, `ROTINA` ou `INFORMATIVA` a partir de 3 exemplos.
3. **Saída estruturada** — gera uma resposta em JSON com `modulo`, `nivel_risco`, `recomendacao`, `prioridade`, `data_estimada` e `acao_imediata`.
4. **Linguagem simples** — traduz um registro técnico para linguagem acessível a qualquer tripulante.

As respostas são **simuladas localmente** (função `simular_resposta_ia`), com regras baseadas em palavras-chave — não há chamada a nenhuma API externa.

---

## 💾 Memória e armazenamento

O sistema usa `with open()` em todas as operações de arquivo (garantindo fechamento automático), e segue o fluxo:

```
Cadastro:  Entrada do usuário → dicionário em RAM → write()/json.dump() → disco
Consulta:  Requisição → read()/json.load() → disco → dicionário em RAM → exibição
```

Mais detalhes (RAM vs. disco, modos de abertura `r`/`w`/`a`, barramentos) são explicados pela própria opção **12** do menu.

---

## 🌍 Ética e responsabilidade

O projeto inclui uma reflexão (opção **13**) sobre:
- Riscos de respostas enviesadas e como o NCAS mitiga isso com critérios objetivos (falha, criticidade, consumo);
- Importância da diversidade nas equipes de desenvolvimento;
- Uso de linguagem neutra e não discriminatória;
- Necessidade de supervisão humana em decisões críticas — o NCAS é um **assistente**, não um tomador de decisão final.

---

## 📚 Conteúdos aplicados

- Manipulação de arquivos texto e JSON (`open`, `with`, modos `w`/`r`/`a`/`x`/`+`)
- Métodos `read()`, `readline()`, `readlines()`, `writelines()`
- Dicionários em Python
- Álgebra booleana / Teoremas de simplificação e De Morgan
- Engenharia de prompts (zero-shot, few-shot, structured output)
- Simulação de resposta de assistente inteligente (sem API real)
- Reflexão sobre diversidade, ética e responsabilidade no uso de IA

---

## 👥 Autor

Equipe NCAS