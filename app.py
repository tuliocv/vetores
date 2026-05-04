import csv
import random
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict

import pandas as pd
import streamlit as st

# ============================================================
# 🍄 SUPER VECTOR BROS — App didático para aula de Vetores Java
# ============================================================

st.set_page_config(
    page_title="Super Vector Bros | Vetores em Java",
    page_icon="🍄",
    layout="wide"
)

# -----------------------------
# CSS / identidade visual
# -----------------------------
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #f7fbff 0%, #fffdf4 100%); }
    .big-title { font-size: 2.2rem; font-weight: 900; margin-bottom: .2rem; }
    .subtitle { font-size: 1.1rem; color: #444; margin-bottom: 1rem; }
    .card {
        background: white; border: 3px solid #222; border-radius: 18px;
        padding: 22px; box-shadow: 6px 6px 0px #222; margin: 12px 0;
    }
    .question-card {
        background: #ffffff; border: 3px solid #e74c3c; border-radius: 18px;
        padding: 24px; box-shadow: 6px 6px 0px #222; margin: 12px 0;
    }
    .concept-pill {
        display: inline-block; padding: 5px 10px; border-radius: 999px;
        background: #f1c40f; color: #111; font-weight: 800; margin-right: 8px;
        border: 2px solid #222;
    }
    .level-pill {
        display: inline-block; padding: 5px 10px; border-radius: 999px;
        background: #e74c3c; color: white; font-weight: 800; border: 2px solid #222;
    }
    .code-box {
        background: #111827; color: #e5e7eb; border-radius: 12px; padding: 14px;
        font-family: Consolas, Monaco, monospace; white-space: pre-wrap; border: 3px solid #222;
    }
    div.stButton > button {
        border-radius: 10px; min-height: 3.1rem; font-weight: 900;
        border: 2px solid #222; box-shadow: 3px 3px 0px #222;
    }
    [data-testid="stMetricValue"] { font-weight: 900; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Persistência
# -----------------------------
DATA_DIR = Path("data_super_vector_bros")
DATA_DIR.mkdir(parents=True, exist_ok=True)
RANKING_FILE = DATA_DIR / "ranking.csv"
RESPONSES_FILE = DATA_DIR / "respostas.csv"

RANKING_COLUMNS = ["ts", "turma", "nome", "heroi", "modo", "acertos", "total", "pontos", "percentual"]
RESPONSE_COLUMNS = [
    "ts", "turma", "nome", "heroi", "modo", "question_id", "nivel", "conceito",
    "escolha", "resposta", "acertou", "tempo_seg", "pontos_questao"
]

def ensure_csv(path: Path, columns: list[str]) -> None:
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(columns)

ensure_csv(RANKING_FILE, RANKING_COLUMNS)
ensure_csv(RESPONSES_FILE, RESPONSE_COLUMNS)

# -----------------------------
# Tema e fases
# -----------------------------
HEROES = {
    "Encanador Vermelho": "🔴",
    "Encanador Verde": "🟢",
    "Princesa do Código": "💖",
    "Cogumelo Tutor": "🍄",
    "Dinossauro Dev": "🦖",
    "Casco Desafiador": "🐢",
}

WORLDS = {
    "Conceito": "🍄 Mundo 1-1: Planície dos Conceitos",
    "Índice": "🧱 Mundo 1-2: Tijolos dos Índices",
    "Declaração": "⭐ Mundo 2-1: Estrela da Sintaxe",
    "Percurso": "🪙 Mundo 2-2: Moedas do for e length",
    "Boletim": "🏁 Mundo 3-1: Boletim da Turma",
    "Erros": "🐢 Mundo 4-1: Cascos dos Bugs",
    "Desafio": "🏰 Castelo Final: Mestre dos Vetores",
}

MODES = {
    "Aula guiada": {
        "desc": "Sequência didática alinhada aos slides: conceito → índice → for → boletim.",
        "question_ids": [
            "C01", "I01", "I02", "D01", "P01", "P02", "B01", "B02", "E01", "B03"
        ],
    },
    "Treino adaptativo": {
        "desc": "Questões misturadas por conceito, com feedback formativo imediato.",
        "question_ids": "ALL_RANDOM_15",
    },
    "Desafio final": {
        "desc": "Mais difícil: maior média, busca, troca e leitura cuidadosa de código.",
        "question_ids": ["B03", "B04", "E01", "E02", "X01", "X02", "X03", "X04", "X05", "X06"],
    },
}

# -----------------------------
# Banco de questões didático
# Cada questão tem objetivo e feedback por alternativa.
# -----------------------------
QUESTIONS = [
    {
        "id": "C01", "level": "Fácil", "concept": "Conceito",
        "objective": "Reconhecer vetor como estrutura homogênea e unidimensional.",
        "prompt": "Em Java, um vetor é mais adequado quando queremos:",
        "code": "double nota1 = 7.0;\ndouble nota2 = 5.0;\ndouble nota3 = 4.9;\n// E se fossem 100 alunos?",
        "options": [
            "Guardar vários valores do mesmo tipo usando um único nome",
            "Guardar qualquer tipo de dado misturado na mesma posição",
            "Criar uma tabela com linhas e colunas",
            "Substituir todos os comandos if do programa",
        ],
        "answer": "Guardar vários valores do mesmo tipo usando um único nome",
        "feedback": {
            "Guardar vários valores do mesmo tipo usando um único nome": "✅ Exato. O vetor reúne vários elementos do mesmo tipo sob um mesmo identificador.",
            "Guardar qualquer tipo de dado misturado na mesma posição": "❌ Vetores nativos são homogêneos: todos os elementos são do mesmo tipo.",
            "Criar uma tabela com linhas e colunas": "❌ Isso será matriz, assunto da próxima aula. Vetor é uma estrutura em uma dimensão.",
            "Substituir todos os comandos if do programa": "❌ Vetores armazenam dados; decisões continuam sendo feitas com if, else if e else.",
        },
        "tip": "Pense no vetor como uma fileira de gavetas do mesmo tipo.",
    },
    {
        "id": "C02", "level": "Fácil", "concept": "Conceito",
        "objective": "Diferenciar variável simples de vetor.",
        "prompt": "Qual alternativa representa melhor a diferença entre variável simples e vetor?",
        "options": [
            "Variável simples guarda um valor; vetor guarda vários valores do mesmo tipo",
            "Variável simples guarda texto; vetor guarda somente números",
            "Variável simples usa índice; vetor não usa índice",
            "Não há diferença prática entre variável e vetor",
        ],
        "answer": "Variável simples guarda um valor; vetor guarda vários valores do mesmo tipo",
        "feedback": {
            "Variável simples guarda um valor; vetor guarda vários valores do mesmo tipo": "✅ Perfeito. Essa é a principal motivação do uso de vetores.",
            "Variável simples guarda texto; vetor guarda somente números": "❌ Existem vetores de int, double, String, boolean e outros tipos.",
            "Variável simples usa índice; vetor não usa índice": "❌ É o contrário: vetor usa índice para acessar seus elementos.",
            "Não há diferença prática entre variável e vetor": "❌ Há diferença importante: vetor organiza vários elementos.",
        },
        "tip": "Um vetor evita criar nota1, nota2, nota3...",
    },
    {
        "id": "I01", "level": "Fácil", "concept": "Índice",
        "objective": "Identificar o primeiro índice de um vetor em Java.",
        "prompt": "Qual é o índice do primeiro elemento de um vetor em Java?",
        "options": ["0", "1", "-1", "length"],
        "answer": "0",
        "feedback": {
            "0": "✅ Isso. Em Java, a contagem dos índices começa em zero.",
            "1": "❌ Essa é a contagem humana comum, mas em Java o primeiro índice é 0.",
            "-1": "❌ Índices negativos não acessam posições válidas em vetores Java.",
            "length": "❌ length é a quantidade de elementos, não o primeiro índice.",
        },
        "tip": "Humano costuma contar do 1; Java conta do 0.",
    },
    {
        "id": "I02", "level": "Fácil", "concept": "Índice",
        "objective": "Distinguir índice e conteúdo.",
        "prompt": "Qual será a saída do código?",
        "code": "int[] valores = {4, 8, 15, 16, 23, 42};\nSystem.out.println(valores[4]);",
        "options": ["4", "23", "42", "Erro"],
        "answer": "23",
        "feedback": {
            "4": "❌ 4 é o conteúdo do índice 0, não o resultado de valores[4].",
            "23": "✅ Correto. valores[4] significa: conteúdo armazenado no índice 4.",
            "42": "❌ 42 está no índice 5.",
            "Erro": "❌ O índice 4 existe nesse vetor, então não há erro.",
        },
        "tip": "Liste os índices: 0, 1, 2, 3, 4, 5.",
    },
    {
        "id": "I03", "level": "Fácil", "concept": "Índice",
        "objective": "Calcular o último índice válido.",
        "prompt": "Um vetor tem 10 elementos. Qual é o último índice válido?",
        "options": ["10", "9", "11", "0"],
        "answer": "9",
        "feedback": {
            "10": "❌ Esse seria o tamanho do vetor, mas o último índice é tamanho - 1.",
            "9": "✅ Exato. Se o vetor tem 10 elementos, os índices vão de 0 a 9.",
            "11": "❌ Está fora do limite.",
            "0": "❌ Esse é o primeiro índice.",
        },
        "tip": "Último índice = length - 1.",
    },
    {
        "id": "D01", "level": "Fácil", "concept": "Declaração",
        "objective": "Declarar e criar vetor de double em Java.",
        "prompt": "Como declarar e criar um vetor de 10 posições para notas do tipo double?",
        "options": [
            "double[] notas = new double[10];",
            "double notas = new double[10];",
            "double notas[10];",
            "new double[] notas = 10;",
        ],
        "answer": "double[] notas = new double[10];",
        "feedback": {
            "double[] notas = new double[10];": "✅ Correto: tipo[] nome = new tipo[tamanho].",
            "double notas = new double[10];": "❌ Falta indicar que notas é vetor com [].",
            "double notas[10];": "❌ Essa sintaxe é comum em outras linguagens, mas não é a forma usada aqui em Java.",
            "new double[] notas = 10;": "❌ A ordem e o uso do new estão incorretos.",
        },
        "tip": "Procure pelos colchetes após o tipo: double[].",
    },
    {
        "id": "D02", "level": "Fácil", "concept": "Declaração",
        "objective": "Reconhecer valor padrão de int em vetor.",
        "prompt": "Qual é o valor inicial de cada posição em `int[] v = new int[5];`?",
        "options": ["0", "1", "null", "vazio sem valor"],
        "answer": "0",
        "feedback": {
            "0": "✅ Correto. Para int, o valor padrão é 0.",
            "1": "❌ O Java não inicia inteiros com 1.",
            "null": "❌ null é usado para referências, como String, não para int.",
            "vazio sem valor": "❌ Em Java, as posições recebem valor padrão.",
        },
        "tip": "Tipos numéricos começam zerados quando criados com new.",
    },
    {
        "id": "P01", "level": "Médio", "concept": "Percurso",
        "objective": "Usar length para descobrir o tamanho do vetor.",
        "prompt": "Qual será a saída?",
        "code": "int[] idades = {18, 30, 35, 42, 47};\nSystem.out.println(idades.length);",
        "options": ["18", "47", "5", "4"],
        "answer": "5",
        "feedback": {
            "18": "❌ 18 é o primeiro conteúdo do vetor, não o tamanho.",
            "47": "❌ 47 é o último conteúdo do vetor, não o tamanho.",
            "5": "✅ Correto. length retorna a quantidade de elementos.",
            "4": "❌ 4 é o último índice, não o tamanho.",
        },
        "tip": "length conta quantas gavetas existem.",
    },
    {
        "id": "P02", "level": "Médio", "concept": "Percurso",
        "objective": "Identificar o laço correto para percorrer vetor.",
        "prompt": "Qual for percorre corretamente todos os elementos de um vetor v?",
        "options": [
            "for (int i = 0; i < v.length; i++)",
            "for (int i = 0; i <= v.length; i++)",
            "for (int i = 1; i <= v.length; i++)",
            "for (int i = v.length; i >= 0; i++)",
        ],
        "answer": "for (int i = 0; i < v.length; i++)",
        "feedback": {
            "for (int i = 0; i < v.length; i++)": "✅ Correto. Começa no 0 e para antes de chegar em length.",
            "for (int i = 0; i <= v.length; i++)": "❌ O <= tenta acessar v[length], que não existe.",
            "for (int i = 1; i <= v.length; i++)": "❌ Pula o índice 0 e ainda tenta acessar índice inválido no fim.",
            "for (int i = v.length; i >= 0; i++)": "❌ Começa fora do vetor e ainda incrementa, causando problema.",
        },
        "tip": "O padrão seguro é i < v.length.",
    },
    {
        "id": "P03", "level": "Médio", "concept": "Percurso",
        "objective": "Diferenciar for tradicional e for-each.",
        "prompt": "Quando o for tradicional é mais indicado do que o for-each?",
        "options": [
            "Quando precisamos do índice para relacionar dois vetores",
            "Quando queremos apenas imprimir cada valor",
            "Quando não sabemos o tipo do vetor",
            "Quando o vetor está vazio",
        ],
        "answer": "Quando precisamos do índice para relacionar dois vetores",
        "feedback": {
            "Quando precisamos do índice para relacionar dois vetores": "✅ Exato. Para nomes[i] e medias[i], o índice é essencial.",
            "Quando queremos apenas imprimir cada valor": "❌ Nesse caso, o for-each pode ser mais simples.",
            "Quando não sabemos o tipo do vetor": "❌ Em Java, o tipo precisa ser conhecido.",
            "Quando o vetor está vazio": "❌ O tipo de laço não resolve sozinho um vetor vazio.",
        },
        "tip": "Se você precisa do i, use for tradicional.",
    },
    {
        "id": "B01", "level": "Médio", "concept": "Boletim",
        "objective": "Relacionar vetores paralelos pelo mesmo índice.",
        "prompt": "Qual saída será produzida?",
        "code": "String[] nomes = {\"Ana\", \"Bruno\", \"Carlos\", \"Diana\"};\ndouble[] medias = {8.5, 6.0, 4.5, 7.2};\nSystem.out.println(nomes[2] + \" - \" + medias[2]);",
        "options": ["Ana - 8.5", "Bruno - 6.0", "Carlos - 4.5", "Diana - 7.2"],
        "answer": "Carlos - 4.5",
        "feedback": {
            "Ana - 8.5": "❌ Esse é o índice 0.",
            "Bruno - 6.0": "❌ Esse é o índice 1.",
            "Carlos - 4.5": "✅ Correto. O mesmo índice relaciona nome e média.",
            "Diana - 7.2": "❌ Esse é o índice 3.",
        },
        "tip": "nomes[2] e medias[2] apontam para dados da mesma posição.",
    },
    {
        "id": "B02", "level": "Médio", "concept": "Boletim",
        "objective": "Classificar situação do estudante pela média.",
        "prompt": "No boletim, qual condição identifica corretamente o aluno em exame?",
        "options": [
            "media >= 5.0 && media < 7.0",
            "media >= 7.0",
            "media < 5.0",
            "media == 7.0",
        ],
        "answer": "media >= 5.0 && media < 7.0",
        "feedback": {
            "media >= 5.0 && media < 7.0": "✅ Correto. Esse intervalo representa exame.",
            "media >= 7.0": "❌ Isso representa aprovado.",
            "media < 5.0": "❌ Isso representa reprovado.",
            "media == 7.0": "❌ Isso pega apenas exatamente 7.0, não o intervalo de exame.",
        },
        "tip": "Use && quando precisar combinar duas condições.",
    },
    {
        "id": "B03", "level": "Difícil", "concept": "Boletim",
        "objective": "Calcular média geral da turma.",
        "prompt": "Depois de somar todas as médias em uma variável `soma`, como calcular a média da turma?",
        "options": ["soma / medias.length", "soma * medias.length", "medias / soma", "soma / 2"],
        "answer": "soma / medias.length",
        "feedback": {
            "soma / medias.length": "✅ Correto. Média é soma dividida pela quantidade de valores.",
            "soma * medias.length": "❌ Isso aumentaria o valor, não calcularia média.",
            "medias / soma": "❌ medias é o vetor inteiro, não um número único.",
            "soma / 2": "❌ Só funcionaria se houvesse exatamente dois estudantes.",
        },
        "tip": "Use length para não depender de quantidade fixa de alunos.",
    },
    {
        "id": "B04", "level": "Difícil", "concept": "Boletim",
        "objective": "Encontrar maior média e nome correspondente.",
        "prompt": "Qual é a melhor inicialização para encontrar a maior média de um vetor não vazio?",
        "code": "double[] medias = {8.5, 6.0, 4.5, 7.2};",
        "options": [
            "double maiorMedia = medias[0];",
            "double maiorMedia = 100;",
            "double maiorMedia = medias.length;",
            "double maiorMedia = null;",
        ],
        "answer": "double maiorMedia = medias[0];",
        "feedback": {
            "double maiorMedia = medias[0];": "✅ Melhor escolha. Você começa comparando com um valor real do vetor.",
            "double maiorMedia = 100;": "❌ Se começar com 100, nenhuma média menor substituirá esse valor.",
            "double maiorMedia = medias.length;": "❌ length é quantidade, não uma média.",
            "double maiorMedia = null;": "❌ double é tipo primitivo e não recebe null.",
        },
        "tip": "Coloque o primeiro aluno no topo provisório e compare os demais.",
    },
    {
        "id": "E01", "level": "Médio", "concept": "Erros",
        "objective": "Reconhecer erro por índice fora do limite.",
        "prompt": "O que acontece com esse código?",
        "code": "int[] numeros = {10, 20, 30, 40, 50};\nSystem.out.println(numeros[5]);",
        "options": ["Imprime 50", "Imprime 0", "Gera erro em tempo de execução", "Imprime 10"],
        "answer": "Gera erro em tempo de execução",
        "feedback": {
            "Imprime 50": "❌ 50 está no índice 4, não no índice 5.",
            "Imprime 0": "❌ Java não retorna 0 para índice inválido.",
            "Gera erro em tempo de execução": "✅ Correto. O índice 5 está fora dos limites.",
            "Imprime 10": "❌ 10 está no índice 0.",
        },
        "tip": "Com 5 elementos, os índices válidos são 0, 1, 2, 3 e 4.",
    },
    {
        "id": "E02", "level": "Difícil", "concept": "Erros",
        "objective": "Entender atribuição de referência entre vetores.",
        "prompt": "Qual será a saída?",
        "code": "int[] a = {1, 2, 3};\nint[] b = a;\nb[0] = 99;\nSystem.out.println(a[0]);",
        "options": ["1", "2", "3", "99"],
        "answer": "99",
        "feedback": {
            "1": "❌ b não recebeu uma cópia independente; b aponta para o mesmo vetor.",
            "2": "❌ 2 está em outro índice.",
            "3": "❌ 3 está em outro índice.",
            "99": "✅ Correto. a e b apontam para o mesmo vetor na memória.",
        },
        "tip": "Atribuir vetor a outro vetor copia a referência, não as gavetas.",
    },
    {
        "id": "X01", "level": "Difícil", "concept": "Desafio",
        "objective": "Executar mentalmente índice aninhado.",
        "prompt": "Qual será a saída?",
        "code": "int[] v = {2, 1, 0};\nSystem.out.println(v[v[0]]);",
        "options": ["2", "1", "0", "Erro"],
        "answer": "0",
        "feedback": {
            "2": "❌ Esse é v[0]. Mas o código usa v[v[0]].",
            "1": "❌ Resolva primeiro v[0], que vale 2. Depois acesse v[2].",
            "0": "✅ Correto. v[0] vale 2; logo v[v[0]] vira v[2], que vale 0.",
            "Erro": "❌ O índice calculado é 2, que existe.",
        },
        "tip": "Resolva de dentro para fora.",
    },
    {
        "id": "X02", "level": "Difícil", "concept": "Desafio",
        "objective": "Imprimir vetor de trás para frente.",
        "prompt": "Qual for imprime um vetor de trás para frente?",
        "options": [
            "for (int i = v.length - 1; i >= 0; i--)",
            "for (int i = 0; i < v.length; i++)",
            "for (int i = v.length; i > 0; i++)",
            "for (int i = 1; i < v.length; i--)",
        ],
        "answer": "for (int i = v.length - 1; i >= 0; i--)",
        "feedback": {
            "for (int i = v.length - 1; i >= 0; i--)": "✅ Correto. Começa no último índice válido e decrementa até 0.",
            "for (int i = 0; i < v.length; i++)": "❌ Esse imprime na ordem normal.",
            "for (int i = v.length; i > 0; i++)": "❌ Começa em índice inválido e incrementa.",
            "for (int i = 1; i < v.length; i--)": "❌ Pode caminhar para índices negativos.",
        },
        "tip": "Último índice é length - 1; para voltar, use i--.",
    },
    {
        "id": "X03", "level": "Difícil", "concept": "Desafio",
        "objective": "Entender troca de valores com variável auxiliar.",
        "prompt": "Como trocar corretamente os valores de v[0] e v[1]?",
        "options": [
            "int aux = v[0]; v[0] = v[1]; v[1] = aux;",
            "v[0] = v[1]; v[1] = v[0];",
            "v[1] = v[0]; v[0] = v[1];",
            "v[0] == v[1];",
        ],
        "answer": "int aux = v[0]; v[0] = v[1]; v[1] = aux;",
        "feedback": {
            "int aux = v[0]; v[0] = v[1]; v[1] = aux;": "✅ Correto. A variável aux evita perder o valor original.",
            "v[0] = v[1]; v[1] = v[0];": "❌ Você perde o valor original de v[0].",
            "v[1] = v[0]; v[0] = v[1];": "❌ Você perde o valor original de v[1].",
            "v[0] == v[1];": "❌ Isso compara; não troca valores.",
        },
        "tip": "Use uma terceira variável como caixa temporária.",
    },
    {
        "id": "X04", "level": "Difícil", "concept": "Desafio",
        "objective": "Reconhecer busca linear.",
        "prompt": "Para descobrir se um número existe em um vetor, a estratégia básica é:",
        "options": [
            "Percorrer o vetor e comparar cada elemento com o valor procurado",
            "Usar length e verificar se ele é igual ao número procurado",
            "Somar todos os valores e comparar com o número procurado",
            "Trocar todos os valores de posição",
        ],
        "answer": "Percorrer o vetor e comparar cada elemento com o valor procurado",
        "feedback": {
            "Percorrer o vetor e comparar cada elemento com o valor procurado": "✅ Correto. Essa é a ideia da busca linear.",
            "Usar length e verificar se ele é igual ao número procurado": "❌ length mostra tamanho, não conteúdo.",
            "Somar todos os valores e comparar com o número procurado": "❌ A soma não indica se um valor específico existe.",
            "Trocar todos os valores de posição": "❌ Trocar não resolve a busca.",
        },
        "tip": "Abra gaveta por gaveta e compare.",
    },
    {
        "id": "X05", "level": "Difícil", "concept": "Desafio",
        "objective": "Interpretar for-each corretamente.",
        "prompt": "Qual será a saída?",
        "code": "int[] v = {3, 4, 5};\nint soma = 0;\nfor (int x : v) {\n    soma += x;\n}\nSystem.out.println(soma);",
        "options": ["3", "5", "12", "Erro"],
        "answer": "12",
        "feedback": {
            "3": "❌ O laço percorre todos os elementos, não apenas o primeiro.",
            "5": "❌ O laço não imprime o último elemento; ele soma todos.",
            "12": "✅ Correto. 3 + 4 + 5 = 12.",
            "Erro": "❌ O código é válido.",
        },
        "tip": "No for-each, x recebe cada conteúdo do vetor.",
    },
    {
        "id": "X06", "level": "Difícil", "concept": "Desafio",
        "objective": "Reconhecer limite do for-each para atualização.",
        "prompt": "O que esse código imprime?",
        "code": "int[] v = {1, 2, 3};\nfor (int x : v) {\n    x = x * 2;\n}\nSystem.out.println(v[0]);",
        "options": ["1", "2", "3", "6"],
        "answer": "1",
        "feedback": {
            "1": "✅ Correto. Alterar x não muda o vetor original nesse caso.",
            "2": "❌ x foi alterado, mas o conteúdo de v[0] não foi substituído.",
            "3": "❌ 3 é outro elemento do vetor.",
            "6": "❌ Isso não representa o primeiro elemento.",
        },
        "tip": "Para alterar o vetor, use for com índice: v[i] = ...",
    },
]

QUESTION_MAP = {q["id"]: q for q in QUESTIONS}

# -----------------------------
# Estado da sessão
# -----------------------------
def init_game(reset: bool = False) -> None:
    if reset or "game" not in st.session_state:
        st.session_state.game = {
            "screen": "SETUP",
            "nome": "",
            "heroi": "Encanador Vermelho",
            "turma": "",
            "modo": "Aula guiada",
            "order": [],
            "q_pos": 0,
            "acertos": 0,
            "pontos": 0,
            "streak": 0,
            "show_feedback": False,
            "last_choice": None,
            "start_q": None,
            "answered_current": False,
            "wrong_ids": [],
        }

init_game()
game = st.session_state.game

# -----------------------------
# Helpers
# -----------------------------
def build_order(modo: str) -> list[str]:
    config = MODES[modo]["question_ids"]
    if config == "ALL_RANDOM_15":
        ids = [q["id"] for q in QUESTIONS]
        random.shuffle(ids)
        return ids[:15]
    return list(config)


def current_question():
    return QUESTION_MAP[game["order"][game["q_pos"]]]


def question_points(q, correct: bool) -> int:
    if not correct:
        return 0
    base = {"Fácil": 10, "Médio": 15, "Difícil": 20}.get(q["level"], 10)
    return base + min(game["streak"], 5) * 2


def append_response(q, choice, correct, elapsed, points):
    with open(RESPONSES_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            datetime.now(timezone.utc).isoformat(), game["turma"], game["nome"], game["heroi"], game["modo"],
            q["id"], q["level"], q["concept"], choice, q["answer"], int(correct), round(elapsed, 1), points
        ])


def append_ranking():
    total = len(game["order"])
    perc = round((game["acertos"] / total) * 100, 1) if total else 0
    with open(RANKING_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            datetime.now(timezone.utc).isoformat(), game["turma"], game["nome"], game["heroi"], game["modo"],
            game["acertos"], total, game["pontos"], perc
        ])


def safe_read_csv(path, cols):
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=cols)

# -----------------------------
# Cabeçalho
# -----------------------------
st.markdown("<div class='big-title'>🍄 Super Vector Bros</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Missão didática: dominar vetores em Java com desafios curtos, feedback imediato e revisão por erro.</div>", unsafe_allow_html=True)

t_game, t_review, t_rank, t_teacher = st.tabs(["🎮 Jogar", "📚 Revisar", "🏆 Ranking", "👨‍🏫 Professor"])

# -----------------------------
# Aba Jogo
# -----------------------------
with t_game:
    if game["screen"] == "SETUP":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Configuração da partida")
        c1, c2, c3 = st.columns([2, 1.5, 1])
        with c1:
            nome = st.text_input("Nome do jogador", placeholder="Digite seu nome")
            turma = st.text_input("Turma / código da aula", placeholder="Ex.: PSC-04-05")
            modo = st.selectbox("Modo", list(MODES.keys()), help="Escolha como o app será usado na aula.")
            st.info(MODES[modo]["desc"])
        with c2:
            heroi = st.selectbox("Avatar", list(HEROES.keys()))
            st.markdown(f"<h1 style='font-size: 90px; text-align:center'>{HEROES[heroi]}</h1>", unsafe_allow_html=True)
        with c3:
            st.metric("Questões", len(build_order(modo)))
            st.metric("Conceitos", len(set(q["concept"] for q in QUESTIONS)))
        start = st.button("PRESS START 🚀", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if start:
            if len(nome.strip()) < 3:
                st.error("Digite um nome com pelo menos 3 caracteres.")
            else:
                game.update({
                    "screen": "PLAYING", "nome": nome.strip(), "turma": turma.strip(),
                    "heroi": heroi, "modo": modo, "order": build_order(modo), "q_pos": 0,
                    "acertos": 0, "pontos": 0, "streak": 0, "show_feedback": False,
                    "last_choice": None, "wrong_ids": [], "start_q": datetime.now(timezone.utc),
                    "answered_current": False,
                })
                st.rerun()

    elif game["screen"] == "PLAYING":
        q = current_question()
        total = len(game["order"])
        hero_icon = HEROES.get(game["heroi"], "⭐")
        progress = game["q_pos"] / total if total else 0

        top1, top2, top3, top4 = st.columns(4)
        top1.metric("Jogador", f"{hero_icon} {game['nome']}")
        top2.metric("Moedas", game["pontos"])
        top3.metric("Acertos", f"{game['acertos']}/{total}")
        top4.metric("Sequência", f"🔥 {game['streak']}")
        st.progress(progress)

        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        st.markdown(f"<span class='concept-pill'>{WORLDS[q['concept']]}</span> <span class='level-pill'>{q['level']}</span>", unsafe_allow_html=True)
        st.caption(f"Objetivo: {q['objective']}")
        st.subheader(q["prompt"])
        if q.get("code"):
            st.code(q["code"], language="java")

        if not game["show_feedback"]:
            choice = st.radio("Escolha uma alternativa:", q["options"], key=f"radio_{q['id']}_{game['q_pos']}")
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Confirmar ✅", use_container_width=True):
                    elapsed = (datetime.now(timezone.utc) - game["start_q"]).total_seconds() if game["start_q"] else 0
                    correct = choice == q["answer"]
                    if correct:
                        game["acertos"] += 1
                        game["streak"] += 1
                    else:
                        game["streak"] = 0
                        game["wrong_ids"].append(q["id"])
                    pts = question_points(q, correct)
                    game["pontos"] += pts
                    game["last_choice"] = choice
                    game["last_correct"] = correct
                    game["last_points"] = pts
                    game["last_elapsed"] = elapsed
                    game["show_feedback"] = True
                    append_response(q, choice, correct, elapsed, pts)
                    st.rerun()
            with c2:
                if st.button("Dica do Cogumelo 🍄", use_container_width=True):
                    st.info(q["tip"])
        else:
            choice = game["last_choice"]
            correct = game["last_correct"]
            feedback = q["feedback"].get(choice, "Resposta registrada.")
            if correct:
                st.success(f"⭐ Acertou! {feedback}")
                st.write(f"🪙 Moedas nesta questão: **{game['last_points']}**")
            else:
                st.error(f"🐢 Quase! {feedback}")
                st.info(f"🍄 Dica: {q['tip']}")
                st.warning(f"Resposta esperada: **{q['answer']}**")
            st.caption(f"Tempo de resposta: {game['last_elapsed']:.1f}s")

            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Próxima fase ➡️", use_container_width=True):
                    game["q_pos"] += 1
                    game["show_feedback"] = False
                    game["last_choice"] = None
                    game["start_q"] = datetime.now(timezone.utc)
                    if game["q_pos"] >= total:
                        append_ranking()
                        game["screen"] = "FINISHED"
                    st.rerun()
            with c2:
                if st.button("Encerrar partida 🏁", use_container_width=True):
                    append_ranking()
                    game["screen"] = "FINISHED"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif game["screen"] == "FINISHED":
        total = len(game["order"])
        perc = (game["acertos"] / total) * 100 if total else 0
        st.balloons()
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.header("🏰 Castelo conquistado!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Moedas", game["pontos"])
        c2.metric("Acertos", f"{game['acertos']}/{total}")
        c3.metric("Precisão", f"{perc:.1f}%")

        if game["wrong_ids"]:
            st.warning("Revise as questões em que você teve dificuldade na aba 📚 Revisar.")
        else:
            st.success("Perfeito! Você acertou todas as questões da partida.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Jogar novamente 🔁", use_container_width=True):
                init_game(reset=True)
                st.rerun()
        with c2:
            if st.button("Recomeçar mantendo nome ⚡", use_container_width=True):
                nome, turma, heroi, modo = game["nome"], game["turma"], game["heroi"], game["modo"]
                init_game(reset=True)
                st.session_state.game.update({"nome": nome, "turma": turma, "heroi": heroi, "modo": modo})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Aba Revisar
# -----------------------------
with t_review:
    st.subheader("📚 Revisão por conceito")
    st.write("Use esta aba para retomar os pontos essenciais depois da partida ou antes do exercício no Eclipse/VS Code.")

    concepts = sorted(set(q["concept"] for q in QUESTIONS))
    selected = st.multiselect("Filtrar conceitos", concepts, default=concepts)
    rows = [q for q in QUESTIONS if q["concept"] in selected]

    for q in rows:
        with st.expander(f"{q['concept']} | {q['id']} | {q['prompt'][:70]}"):
            st.write(f"**Objetivo:** {q['objective']}")
            if q.get("code"):
                st.code(q["code"], language="java")
            st.write(f"**Resposta:** {q['answer']}")
            st.info(q["tip"])

# -----------------------------
# Ranking
# -----------------------------
with t_rank:
    st.subheader("🏆 Ranking do Reino")
    df_rank = safe_read_csv(RANKING_FILE, RANKING_COLUMNS)
    if df_rank.empty:
        st.info("Ainda não há partidas registradas.")
    else:
        turma_filter = st.text_input("Filtrar por turma/código", value="")
        df_show = df_rank.copy()
        if turma_filter.strip():
            df_show = df_show[df_show["turma"].fillna("").str.contains(turma_filter.strip(), case=False, na=False)]
        df_show = df_show.sort_values(["pontos", "percentual"], ascending=False).head(15)
        st.dataframe(df_show[["nome", "heroi", "modo", "acertos", "total", "pontos", "percentual", "turma"]], use_container_width=True)
        st.download_button(
            "Baixar ranking CSV",
            data=df_rank.to_csv(index=False).encode("utf-8"),
            file_name="ranking_super_vector_bros.csv",
            mime="text/csv",
            use_container_width=True,
        )

# -----------------------------
# Professor
# -----------------------------
with t_teacher:
    st.subheader("👨‍🏫 Painel do professor")
    st.caption("Use para fechamento da aula: identificar questões com maior erro e retomar conceitos.")
    password = st.text_input("Código do professor", type="password", placeholder="Digite: prof")
    if password != "prof":
        st.info("Digite o código para visualizar os dados da turma.")
    else:
        df_resp = safe_read_csv(RESPONSES_FILE, RESPONSE_COLUMNS)
        if df_resp.empty:
            st.info("Ainda não há respostas registradas.")
        else:
            turma = st.text_input("Filtrar turma", value="")
            df = df_resp.copy()
            if turma.strip():
                df = df[df["turma"].fillna("").str.contains(turma.strip(), case=False, na=False)]

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Respostas", len(df))
            c2.metric("Participantes", df["nome"].nunique() if not df.empty else 0)
            c3.metric("Acerto médio", f"{df['acertou'].mean()*100:.1f}%" if not df.empty else "0%")
            c4.metric("Tempo médio", f"{df['tempo_seg'].mean():.1f}s" if not df.empty else "0s")

            if not df.empty:
                st.markdown("### Acerto por conceito")
                by_concept = df.groupby("conceito", as_index=False)["acertou"].mean()
                by_concept["% acerto"] = (by_concept["acertou"] * 100).round(1)
                st.bar_chart(by_concept.set_index("conceito")["% acerto"])

                st.markdown("### Questões com maior dificuldade")
                miss = df.groupby(["question_id", "conceito"], as_index=False).agg(
                    respostas=("acertou", "count"), acertos=("acertou", "sum")
                )
                miss["% erro"] = ((1 - miss["acertos"] / miss["respostas"]) * 100).round(1)
                miss = miss.sort_values(["% erro", "respostas"], ascending=False).head(10)
                st.dataframe(miss, use_container_width=True)

                st.download_button(
                    "Baixar respostas CSV",
                    data=df_resp.to_csv(index=False).encode("utf-8"),
                    file_name="respostas_super_vector_bros.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

                if st.button("Limpar dados locais ⚠️", use_container_width=True):
                    ensure_csv(RANKING_FILE, RANKING_COLUMNS)
                    ensure_csv(RESPONSES_FILE, RESPONSE_COLUMNS)
                    RANKING_FILE.write_text(",".join(RANKING_COLUMNS) + "\n", encoding="utf-8")
                    RESPONSES_FILE.write_text(",".join(RESPONSE_COLUMNS) + "\n", encoding="utf-8")
                    st.success("Arquivos locais reiniciados.")
                    st.rerun()
