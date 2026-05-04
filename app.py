import os
import csv
import random
import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime, timezone

# =========================
# 🍄 CONFIGURAÇÃO E TEMA GAMER
# =========================
st.set_page_config(page_title="Mario Vector Master", page_icon="🦖", layout="wide")

# Estilos CSS para simular a interface de um console
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 60px; font-weight: bold; font-size: 18px; }
    .main-card { border: 3px solid #e74c3c; border-radius: 15px; padding: 25px; background: white; box-shadow: 5px 5px 0px #000; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #e74c3c; color: white; font-weight: bold; border: 2px solid #b22222; }
    .stButton>button:hover { background-color: #ff4d4d; border: 2px solid #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# 💾 PERSISTÊNCIA E LOGS
# =========================
DATA_DIR = Path("data_mario_pro")
DATA_DIR.mkdir(parents=True, exist_ok=True)
RANKING_FILE = DATA_DIR / "ranking_v2.csv"

def ensure_ranking():
    if not RANKING_FILE.exists():
        with open(RANKING_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["ts", "name", "char", "corrects", "score", "percent"])

ensure_ranking()

# =========================
# 🎮 CONFIGURAÇÃO DO MUNDO
# =========================
CHARACTERS = {
    "Mario": "🔴", "Luigi": "🟢", "Peach": "💖", "Toad": "🍄", "Bowser": "🔥", "Yoshi": "🦖"
}

PHASES = {
    "Fácil": "Mundo 1-1: Planície dos Índices",
    "Médio": "Mundo 2-4: Deserto das Iterações",
    "Difícil": "Mundo 7-3: Mar de Referências",
    "Desafiador": "Bowser's Castle: O Caos da Memória"
}

# =========================
# 📚 BANCO DE 28 QUESTÕES
# =========================
QUESTIONS = [
    # ------------------------------------------------------------
    # MUNDO 1: PLANÍCIE DOS ÍNDICES (Fácil - Conceitos e Sintaxe)
    # ------------------------------------------------------------
    {
        "id": "M1-1", "level": "Fácil",
        "prompt": "Na Aula 12, um vetor é definido como uma variável composta e:",
        "options": ["Heterogênea", "Homogênea", "Dinâmica", "Infinita"], "answer": "Homogênea",
        "rationale": {
            "Heterogênea": "❌ Errado. Vetores guardam apenas dados do mesmo tipo[cite: 1].",
            "Homogênea": "✅ Wahoo! Significa que todas as gavetas guardam o mesmo tipo de dado[cite: 1].",
            "Dinâmica": "❌ Errado. Vetores nativos em Java têm tamanho fixo.",
            "Infinita": "❌ Errado. Vetores têm um número finito de variáveis[cite: 1]."
        },
        "tip": "Pense no armário: se é para médias, só guarda números[cite: 1]."
    },
    {
        "id": "M1-2", "level": "Fácil",
        "prompt": "Qual o valor padrão de um elemento em 'int[] v = new int[5];'?",
        "options": ["null", "0", "1", "Vazio"], "answer": "0",
        "rationale": {
            "null": "❌ Errado. 'null' é para objetos; 'int' é um tipo primitivo.",
            "0": "✅ Isso! Java inicializa vetores de números inteiros com zero automaticamente.",
            "1": "❌ Errado. O valor inicial padrão é sempre zero.",
            "Vazio": "❌ Errado. Gavetas de tipos primitivos sempre possuem um valor inicial."
        },
        "tip": "Tipos numéricos começam 'zerados'."
    },
    {
        "id": "M1-3", "level": "Fácil",
        "prompt": "Como o Mario deve declarar um vetor de 10 posições para notas (double)?",
        "options": ["double[] notas = new double[10];", "double notas = new double[10];", "double notas[10];", "new double notas[10];"], "answer": "double[] notas = new double[10];",
        "rationale": {
            "double[] notas = new double[10];": "✅ Perfeito! Tipo[] nome = new Tipo[tamanho][cite: 1].",
            "double notas = new double[10];": "❌ Falta o '[]' no tipo para indicar que é um vetor[cite: 1].",
            "double notas[10];": "❌ Sintaxe de outras linguagens (como C), não Java.",
            "new double notas[10];": "❌ Ordem incorreta dos comandos."
        },
        "tip": "Os colchetes '[]' são a marca do vetor[cite: 1]."
    },
    {
        "id": "M1-4", "level": "Fácil",
        "prompt": "O atributo '.length' em um vetor serve para:",
        "options": ["Somar valores", "Ver o maior valor", "Saber o tamanho total", "Deletar o vetor"], "answer": "Saber o tamanho total",
        "rationale": {
            "Somar valores": "❌ Errado. Para somar, você precisa de um loop.",
            "Ver o maior valor": "❌ Errado. O length mede gavetas, não o que tem dentro.",
            "Saber o tamanho total": "✅ Correto! Retorna a quantidade de gavetas do armário[cite: 1].",
            "Deletar o vetor": "❌ Errado. Java usa o Garbage Collector para isso."
        },
        "tip": "Dica: .length não tem parênteses em vetores[cite: 1]."
    },
    {
        "id": "M1-5", "level": "Fácil",
        "prompt": "Qual é o índice do primeiro elemento de qualquer vetor em Java?",
        "options": ["1", "0", "-1", "length"], "answer": "0",
        "rationale": {
            "1": "❌ Errado. Começar no 1 faria você perder a primeira gaveta[cite: 1].",
            "0": "✅ Wahoo! A contagem sempre começa no zero[cite: 1].",
            "-1": "❌ Errado. Índices negativos não são permitidos.",
            "length": "❌ Errado. Este índice estaria fora do limite[cite: 1]."
        },
        "tip": "Em Java, somos 'Zero-indexed'[cite: 1]."
    },
    {
        "id": "M1-6", "level": "Fácil",
        "prompt": "O que acontece se você tentar acessar 'notas[10]' em um vetor de tamanho 10?",
        "options": ["Acessa o último", "Retorna 0", "Dá erro de execução", "Acessa o primeiro"], "answer": "Dá erro de execução",
        "rationale": {
            "Acessa o último": "❌ Errado. O último seria o índice 9[cite: 1].",
            "Retorna 0": "❌ Errado. O programa trava antes de retornar algo.",
            "Dá erro de execução": "✅ Mamma Mia! O índice 10 está fora do limite (0 a 9)[cite: 1].",
            "Acessa o primeiro": "❌ Errado. O primeiro é o índice 0."
        },
        "tip": "Último índice é sempre length - 1[cite: 1]."
    },
    {
        "id": "M1-7", "level": "Fácil",
        "prompt": "Vetores são chamados de estruturas unidimensionais porque:",
        "options": ["Têm várias linhas", "Formam um cubo", "São como uma linha de gavetas", "Não têm tamanho"], "answer": "São como uma linha de gavetas",
        "rationale": {
            "Têm várias linhas": "❌ Errado. Isso seria bidimensional (matriz).",
            "Formam um cubo": "❌ Errado. Isso seria tridimensional.",
            "São como uma linha de gavetas": "✅ Isso! Formam uma única dimensão linear[cite: 1].",
            "Não têm tamanho": "❌ Errado. Eles têm tamanho finito[cite: 1]."
        },
        "tip": "Imagine uma régua horizontal[cite: 1]."
    },

    # ------------------------------------------------------------
    # MUNDO 2: DESERTO DAS ITERAÇÕES (Médio - Acesso e Loops)
    # ------------------------------------------------------------
    {
        "id": "M2-1", "level": "Médio",
        "prompt": "Qual o problema deste código: 'for(int i=0; i <= v.length; i++)'?",
        "options": ["Nenhum", "Pula o primeiro", "Erro no último índice", "Loop infinito"], "answer": "Erro no último índice",
        "rationale": {
            "Nenhum": "❌ Errado. O programa vai travar.",
            "Pula o primeiro": "❌ Errado. Ele começa no 0 corretamente.",
            "Erro no último índice": "✅ Isso! O '=' tenta acessar um índice que não existe[cite: 1].",
            "Loop infinito": "❌ Errado. O loop para, mas com um erro."
        },
        "tip": "Sempre use 'i < length'[cite: 1]."
    },
    {
        "id": "M2-2", "level": "Médio",
        "prompt": "No loop 'for (int x : v)', o que a variável 'x' recebe a cada volta?",
        "options": ["O índice", "O tamanho", "O conteúdo da gaveta", "O endereço"], "answer": "O conteúdo da gaveta",
        "rationale": {
            "O índice": "❌ Errado. O for-each 'esconde' o índice.",
            "O tamanho": "❌ Errado. O tamanho é fixo (length).",
            "O conteúdo da gaveta": "✅ Wahoo! O 'x' recebe o valor direto do vetor[cite: 1].",
            "O endereço": "❌ Errado. Recebe o dado armazenado."
        },
        "tip": "O for-each serve para ler os valores sem se preocupar com o índice[cite: 1]."
    },
    {
        "id": "M2-3", "level": "Médio",
        "prompt": "Para somar todas as notas de um vetor, a variável 'soma' deve iniciar com:",
        "options": ["1", "0", "length", "null"], "answer": "0",
        "rationale": {
            "1": "❌ Errado. Isso alteraria o resultado final.",
            "0": "✅ Correto! O elemento neutro da soma é zero[cite: 1].",
            "length": "❌ Errado. Somaria o tamanho às notas.",
            "null": "❌ Errado. Não se soma números com null."
        },
        "tip": "Comece com o balde de moedas vazio[cite: 1]."
    },
    {
        "id": "M2-4", "level": "Médio",
        "prompt": "Como o Mario altera o valor da terceira posição (índice 2) para 10.0?",
        "options": ["v[2] = 10.0;", "v[3] = 10.0;", "v = 10.0;", "v{2} = 10.0;"], "answer": "v[2] = 10.0;",
        "rationale": {
            "v[2] = 10.0;": "✅ Isso! Acesso direto pelo índice[cite: 1].",
            "v[3] = 10.0;": "❌ Errado. Isso alteraria a quarta posição.",
            "v = 10.0;": "❌ Errado. Você não pode atribuir um número a um vetor inteiro.",
            "v{2} = 10.0;": "❌ Errado. Java usa colchetes '[]'."
        },
        "tip": "Use a gaveta certa: 0, 1, 2...[cite: 1]"
    },
    {
        "id": "M2-5", "level": "Médio",
        "prompt": "O que o loop for-each NÃO consegue fazer?",
        "options": ["Ler valores", "Imprimir o vetor", "Alterar valores do vetor", "Somar valores"], "answer": "Alterar valores do vetor",
        "rationale": {
            "Ler valores": "❌ Errado. Ele faz isso perfeitamente.",
            "Imprimir o vetor": "❌ Errado. É ótimo para isso.",
            "Alterar valores do vetor": "✅ Correto! Ele fornece apenas uma cópia do valor para leitura[cite: 1].",
            "Somar valores": "❌ Errado. Pode ser usado para acumular somas."
        },
        "tip": "Para mudar o conteúdo das gavetas, use o for tradicional[cite: 1]."
    },
    {
        "id": "M2-6", "level": "Médio",
        "prompt": "Na metáfora da aula, as 'gavetas' representam os:",
        "options": ["Índices", "Elementos", "Tipos", "Loops"], "answer": "Elementos",
        "rationale": {
            "Índices": "❌ Errado. O índice é o número da gaveta[cite: 1].",
            "Elementos": "✅ Isso! O conteúdo guardado em cada divisão[cite: 1].",
            "Tipos": "❌ Errado. O tipo define o que a gaveta aceita.",
            "Loops": "❌ Errado. Loops servem para abrir as gavetas."
        },
        "tip": "Gaveta = Elemento; Número da gaveta = Índice[cite: 1]."
    },
    {
        "id": "M2-7", "level": "Médio",
        "prompt": "Qual o resultado de 'System.out.println(v.length)' para 'int[] v = {5, 10, 15};'?",
        "options": ["5", "10", "15", "3"], "answer": "3",
        "rationale": {
            "5": "❌ Errado. Este é o valor v[0].",
            "10": "❌ Errado. Este é o valor v[1].",
            "15": "❌ Errado. Este é o valor v[2].",
            "3": "✅ Wahoo! Existem 3 elementos no vetor[cite: 1]."
        },
        "tip": "Length conta quantas gavetas existem[cite: 1]."
    },

    # ------------------------------------------------------------
    # MUNDO 7: MAR DE REFERÊNCIAS (Difícil - Processamento)
    # ------------------------------------------------------------
    {
        "id": "M3-1", "level": "Difícil",
        "prompt": "Como calcular a média da turma usando 'soma' e o vetor 'notas'?",
        "options": ["soma / 2", "soma / notas.length", "soma * length", "notas / soma"], "answer": "soma / notas.length",
        "rationale": {
            "soma / 2": "❌ Errado. Só funcionaria para 2 alunos.",
            "soma / notas.length": "✅ Isso! Soma total dividida pela quantidade de alunos[cite: 1].",
            "soma * length": "❌ Errado. Isso daria um valor astronômico.",
            "notas / soma": "❌ Errado. Operação inválida."
        },
        "tip": "Divida o total de moedas pelo número de caixas[cite: 1]."
    },
    {
        "id": "M3-2", "level": "Difícil",
        "prompt": "Em vetores paralelos (nomes e notas), como saber a nota da 'Ana'?",
        "options": ["Procurar o nome e usar o mesmo índice", "Nomes e notas são a mesma coisa", "Usar índices diferentes", "Não é possível"], "answer": "Procurar o nome e usar o mesmo índice",
        "rationale": {
            "Procurar o nome e usar o mesmo índice": "✅ Bingo! O índice une os dados relacionados[cite: 1].",
            "Nomes e notas são a mesma coisa": "❌ Errado. São vetores diferentes.",
            "Usar índices diferentes": "❌ Errado. Isso traria a nota de outra pessoa[cite: 1].",
            "Não é possível": "❌ Errado. É uma técnica comum na aula 12[cite: 1]."
        },
        "tip": "Mesmo índice = mesma pessoa[cite: 1]."
    },
    {
        "id": "M3-3", "level": "Difícil",
        "prompt": "Para achar a maior nota, com qual valor devemos iniciar a variável 'maior'?",
        "options": ["0", "Com o primeiro elemento do vetor", "100", "-1"], "answer": "Com o primeiro elemento do vetor",
        "rationale": {
            "0": "❌ Funciona para notas positivas, mas não é o ideal.",
            "Com o primeiro elemento do vetor": "✅ Melhor prática! Garante que você compara com valores reais[cite: 1].",
            "100": "❌ Errado. Se a maior nota for 90, você nunca a acharia.",
            "-1": "❌ Funciona apenas para números positivos."
        },
        "tip": "Inicie o trono com o primeiro competidor do vetor[cite: 1]."
    },
    {
        "id": "M3-4", "level": "Difícil",
        "prompt": "O que faz 'if (medias[i] >= 7.0)' no sistema de boletim?",
        "options": ["Reprova o aluno", "Manda para exame", "Aprova o aluno", "Zera a nota"], "answer": "Aprova o aluno",
        "rationale": {
            "Reprova o aluno": "❌ Errado. Reprovado é para notas baixas.",
            "Manda para exame": "❌ Errado. Exame seria entre 5 e 7[cite: 1].",
            "Aprova o aluno": "✅ Isso! Notas 7 ou superiores garantem a aprovação[cite: 1].",
            "Zera a nota": "❌ Errado. É apenas uma verificação."
        },
        "tip": "Verificando se o Mario passou de fase[cite: 1]."
    },
    {
        "id": "M3-5", "level": "Difícil",
        "prompt": "Na máquina de bebidas, por que usamos 'menu[a - 1]'?",
        "options": ["Para dar desconto", "Para ajustar o índice 0", "Para pular o café", "Porque o Java manda"], "answer": "Para ajustar o índice 0",
        "rationale": {
            "Para dar desconto": "❌ Errado. Não envolve dinheiro.",
            "Para ajustar o índice 0": "✅ Exato! Se o usuário digita 1, queremos a posição 0[cite: 1].",
            "Para pular o café": "❌ Errado. O café está no menu.",
            "Porque o Java manda": "❌ Errado. É uma necessidade lógica de mapeamento."
        },
        "tip": "Humano conta do 1, Java conta do 0[cite: 1]."
    },
    {
        "id": "M3-6", "level": "Difícil",
        "prompt": "Como o Mario descobre quem ficou em EXAME (entre 5.0 e 6.9)?",
        "options": ["if (nota >= 5.0 && nota < 7.0)", "if (nota > 7.0)", "if (nota < 5.0)", "if (nota == 5.0)"], "answer": "if (nota >= 5.0 && nota < 7.0)",
        "rationale": {
            "if (nota >= 5.0 && nota < 7.0)": "✅ Isso! Captura o intervalo de recuperação[cite: 1].",
            "if (nota > 7.0)": "❌ Errado. Isso é para aprovados.",
            "if (nota < 5.0)": "❌ Errado. Isso é para reprovados.",
            "if (nota == 5.0)": "❌ Errado. Pega apenas uma nota específica."
        },
        "tip": "Use o operador 'E' (&&) para cercar a nota[cite: 1]."
    },
    {
        "id": "M3-7", "level": "Difícil",
        "prompt": "Para imprimir o Nome e a Média juntos em um loop 'for', usamos:",
        "options": ["System.out.println(nomes[i] + medias[i])", "System.out.println(nomes + medias)", "System.out.println(i + i)", "Não é possível"], "answer": "System.out.println(nomes[i] + medias[i])",
        "rationale": {
            "System.out.println(nomes[i] + medias[i])": "✅ Correto! Combina os dados de ambos os vetores[cite: 1].",
            "System.out.println(nomes + medias)": "❌ Errado. Isso imprime os endereços de memória.",
            "System.out.println(i + i)": "❌ Errado. Isso soma o número do índice.",
            "Não é possível": "❌ Errado. Foi demonstrado na aula 12[cite: 1]."
        },
        "tip": "Concatene as gavetas de mesmo número[cite: 1]."
    },

    # ------------------------------------------------------------
    # BOWSER'S CASTLE: O CAOS DA MEMÓRIA (Desafiador - Lógica Extra)
    # ------------------------------------------------------------
    {
        "id": "CH-1", "level": "Desafiador",
        "prompt": "Como o Mario faz para trocar os valores de v[0] e v[1] (SWAP)?",
        "options": ["v[0] = v[1]; v[1] = v[0];", "v[1] = v[0]; v[0] = v[1];", "int aux = v[0]; v[0] = v[1]; v[1] = aux;", "v[0] == v[1];"], "answer": "int aux = v[0]; v[0] = v[1]; v[1] = aux;",
        "rationale": {
            "v[0] = v[1]; v[1] = v[0];": "❌ Errado. Você perderia o valor original de v[0].",
            "v[1] = v[0]; v[0] = v[1];": "❌ Errado. Você perderia o valor original de v[1].",
            "int aux = v[0]; v[0] = v[1]; v[1] = aux;": "✅ Bingo! A variável 'aux' guarda o valor para não ser perdido.",
            "v[0] == v[1];": "❌ Errado. Isso apenas compara, não troca."
        },
        "tip": "Pense no Mario segurando um item enquanto move os outros dois."
    },
    {
        "id": "CH-2", "level": "Desafiador",
        "prompt": "O que acontece se você declarar 'int[] v = new int[-5];'?",
        "options": ["Cria um vetor negativo", "Dá erro de execução", "O Java ignora", "Cria um vetor de 5"], "answer": "Dá erro de execução",
        "rationale": {
            "Cria um vetor negativo": "❌ Errado. Não existem gavetas negativas.",
            "Dá erro de execução": "✅ Correto! Lança uma 'NegativeArraySizeException'.",
            "O Java ignora": "❌ Errado. O Java é rigoroso com o tamanho.",
            "Cria um vetor de 5": "❌ Errado. Ele não converte automaticamente."
        },
        "tip": "Não dá para construir um armário com menos que zero gavetas."
    },
    {
        "id": "CH-3", "level": "Desafiador",
        "prompt": "Se 'String[] nomes = new String[5];', o que tem em 'nomes[0]' antes de atribuir?",
        "options": ["Espaço vazio", "null", "0", "Erro"], "answer": "null",
        "rationale": {
            "Espaço vazio": "❌ Errado. Isso seria uma String instanciada.",
            "null": "✅ Isso! Vetores de Objetos (Strings) iniciam como nulos.",
            "0": "❌ Errado. 0 é apenas para números.",
            "Erro": "❌ Errado. A gaveta existe, só está vazia."
        },
        "tip": "Objetos (como Strings) começam apontando para o 'nada'."
    },
    {
        "id": "CH-4", "level": "Desafiador",
        "prompt": "O que acontece ao fazer 'int[] b = a;' em Java?",
        "options": ["Copia os valores", "Cria um vetor novo", "Faz 'b' apontar para o mesmo vetor de 'a'", "Dá erro"], "answer": "Faz 'b' apontar para o mesmo vetor de 'a'",
        "rationale": {
            "Copia os valores": "❌ Errado. Isso não acontece automaticamente.",
            "Cria um vetor novo": "❌ Errado. Não houve uso do 'new'.",
            "Faz 'b' apontar para o mesmo vetor de 'a'": "✅ Mamma Mia! Ambos agora dividem o mesmo armário na memória.",
            "Dá erro": "❌ Errado. É uma operação comum."
        },
        "tip": "Atribuir vetores é copiar o 'endereço' do armário, não as gavetas."
    },
    {
        "id": "CH-5", "level": "Desafiador",
        "prompt": "Qual o resultado de 'v[v[0]]' se 'int[] v = {2, 1, 0};'?",
        "options": ["2", "1", "0", "Erro"], "answer": "0",
        "rationale": {
            "2": "❌ Errado. Este é o v[0].",
            "1": "❌ Errado. Este é o v[1].",
            "0": "✅ Gênio! v[0] é 2, então acessamos v[2], que é 0.",
            "Erro": "❌ Errado. É uma lógica válida de índices aninhados."
        },
        "tip": "Resolva de dentro para fora: primeiro o índice interno."
    },
    {
        "id": "CH-6", "level": "Desafiador",
        "prompt": "Para imprimir um vetor de trás para frente, qual o 'for' correto?",
        "options": ["for(int i=v.length-1; i >= 0; i--)", "for(int i=0; i < v.length; i++)", "for(int i=v.length; i > 0; i++)", "Não é possível"], "answer": "for(int i=v.length-1; i >= 0; i--)",
        "rationale": {
            "for(int i=v.length-1; i >= 0; i--)": "✅ Isso! Começa na última gaveta e desce até a zero.",
            "for(int i=0; i < v.length; i++)": "❌ Errado. Isso imprime na ordem normal.",
            "for(int i=v.length; i > 0; i++)": "❌ Errado. Isso causaria erro de índice.",
            "Não é possível": "❌ Errado. É um exercício clássico de lógica."
        },
        "tip": "Comece no fim e use o decremento (i--)."
    },
    {
        "id": "CH-7", "level": "Desafiador",
        "prompt": "Como o Bowser descobre se um número existe no vetor?",
        "options": ["Usando um 'if' dentro de um loop", "Olhando o length", "Usando o operador +", "Perguntando ao Java"], "answer": "Usando um 'if' dentro de um loop",
        "rationale": {
            "Usando um 'if' dentro de um loop": "✅ Bingo! Chamamos isso de Busca Linear.",
            "Olhando o length": "❌ Errado. Isso só diz o tamanho.",
            "Usando o operador +": "❌ Errado. Isso soma valores.",
            "Perguntando ao Java": "❌ Errado. Você deve programar a lógica."
        },
        "tip": "Abra gaveta por gaveta e compare com o que você procura."
    }
]

# =========================
# ⚙️ ESTADO DA SESSÃO
# =========================
if "state" not in st.session_state:
    st.session_state.state = {
        "screen": "SETUP", "name": "", "char": "Mario",
        "q_idx": 0, "corrects": 0, "points": 0, "streak": 0,
        "show_fb": False, "last_choice": None, "order": list(range(len(QUESTIONS)))
    }
    random.shuffle(st.session_state.state["order"])

s = st.session_state.state

# =========================
# 🏰 INTERFACE PRINCIPAL
# =========================
t_game, t_rank = st.tabs(["🎮 JOGAR FASE", "🏆 RANKING DO REINO"])

with t_game:
    if s["screen"] == "SETUP":
        st.header("🍄 Bem-vindo ao Reino dos Vetores!")
        col_l, col_r = st.columns([2, 1])
        with col_l:
            name = st.text_input("Player Name:", placeholder="Seu nome aqui")
            char = st.selectbox("Escolha seu Herói:", list(CHARACTERS.keys()))
        with col_r:
            st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{CHARACTERS[char]}</h1>", unsafe_allow_html=True)
            
        if st.button("PRESS START 🚀"):
            if len(name.strip()) >= 3:
                s["name"], s["char"], s["screen"] = name.strip(), char, "PLAYING"
                st.rerun()
            else:
                st.error("O nome deve ter 3+ caracteres.")

    elif s["screen"] == "PLAYING":
        q = QUESTIONS[s["order"][s["q_idx"]]]
        total_q = len(QUESTIONS)
        
        # Stats Bar
        st.markdown(f"### {CHARACTERS[s['char']]} {s['name']} | {PHASES[q['level']]} | 🔥 {s['streak']} | 🪙 {s['points']}")
        st.progress(s["q_idx"] / total_q)
        
        with st.container():
            st.markdown(f"#### {q['prompt']}")
            
            if not s["show_fb"]:
                choice = st.radio("Selecione a ação:", q["options"], key=f"r_{q['id']}")
                if st.button("CONFIRMAR ✅"):
                    s["last_choice"], s["show_fb"] = choice, True
                    if choice == q["answer"]:
                        s["corrects"] += 1; s["streak"] += 1
                        s["points"] += (10 * s["streak"])
                    else:
                        s["streak"] = 0
                    st.rerun()
            else:
                choice = s["last_choice"]
                correct = (choice == q["answer"])
                fb = q["rationale"].get(choice, "Essa alternativa não parece correta.")
                
                if correct: st.success(f"⭐ **WAHOO!** {fb}")
                else: 
                    st.error(f"💀 **MAMMA MIA!** {fb}")
                    st.info(f"💡 **Dica do Toad:** {q['tip']}")
                    st.warning(f"A resposta certa era: **{q['answer']}**")
                
                if st.button("PRÓXIMA FASE ➡️"):
                    s["q_idx"] += 1
                    s["show_fb"] = False
                    if s["q_idx"] >= total_q: s["screen"] = "FINISHED"
                    st.rerun()

    elif s["screen"] == "FINISHED":
        st.balloons()
        st.header("🏁 CHEGADA NO CASTELO!")
        perc = (s["corrects"] / len(QUESTIONS)) * 100
        
        st.metric("Moedas (Pontos)", s["points"])
        st.write(f"Parabéns! Precisão final: **{perc:.1f}%**")
        
        # Salva Ranking
        with open(RANKING_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([datetime.now(timezone.utc), s["name"], s["char"], s["corrects"], s["points"], f"{perc:.1f}%"])
            
        if st.button("RECOMEÇAR AVENTURA 🔁"):
            st.session_state.clear()
            st.rerun()

with t_rank:
    st.header("🏆 Hall da Fama do Reino")
    try:
        df = pd.read_csv(RANKING_FILE)
        if not df.empty:
            df["Herói"] = df["char"].apply(lambda x: f"{CHARACTERS.get(x, '❓')} {x}")
            df_disp = df.sort_values(by="score", ascending=False).head(10)
            df_disp = df_disp[["name", "Herói", "score", "percent", "corrects"]]
            df_disp.columns = ["Jogador", "Personagem", "Pontos", "% Acertos", "Acertos"]
            st.table(df_disp)
        else: st.info("Ranking vazio. Seja o primeiro!")
    except: st.error("Erro ao carregar ranking.")
