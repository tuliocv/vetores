import os
import csv
import random
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st

# =========================
# CONFIGURAÇÃO DO REINO DO COGUMELO
# =========================
st.set_page_config(page_title="Mario Vector Adventure", page_icon="🍄", layout="centered")

# Estilo para simular um tom mais "gamer"
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #e74c3c; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #c0392b; border: 2px solid #f1c40f; }
    </style>
    """, unsafe_allow_value=True)

st.title("🍄 Mario Vector Adventure")
st.subheader("Arrays em Java: A Missão de Resgate")
st.caption(f"Período de Avaliação A1 | Hoje: {datetime.now().strftime('%d/%m/%Y')}")

# =========================
# PERSISTÊNCIA DE DADOS (CSV)
# =========================
DATA_DIR = Path("data_mario_v2")
DATA_DIR.mkdir(parents=True, exist_ok=True)
SCORES_FILE = DATA_DIR / "scores.csv"
ANSWERS_FILE = DATA_DIR / "answers.csv"
PROGRESS_FILE = DATA_DIR / "progress.csv"

def ensure_files():
    files_headers = [
        (SCORES_FILE, ["ts", "name", "correct", "points", "total", "percent", "streak"]),
        (ANSWERS_FILE, ["ts", "name", "qid", "level", "is_correct"]),
        (PROGRESS_FILE, ["ts", "name", "idx", "total", "correct", "points", "status"])
    ]
    for p, h in files_headers:
        if not p.exists():
            with open(p, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(h)

ensure_files()

# =========================
# BANCO DE QUESTÕES (20 ITENS)
# =========================
QUESTIONS = [
    # MUNDO 1 - FÁCIL
    {
        "id": "M1-1", "level": "Fácil",
        "prompt": "O Mario guardou moedas em um vetor: `int[] bau = {10, 20, 30, 40};`. Qual o valor de `bau[1]`?",
        "options": ["10", "20", "30", "40"],
        "answer": "20",
        "rationale": {
            "10": "❌ Quase! O 10 está no índice 0. Lembre-se: o índice começa em zero.",
            "20": "✅ Wahoo! O índice 1 aponta para a segunda gaveta do nosso armário.",
            "30": "❌ Errado. O 30 está no índice 2.",
            "40": "❌ Errado. O 40 está no índice 3 (última posição)."
        },
        "tip": "Arrays são indexados em 0. O primeiro é bau[0], o segundo é bau[1]."
    },
    {
        "id": "M1-2", "level": "Fácil",
        "prompt": "Para criar um novo armário (vetor) de 10 gavetas para guardar cogumelos (inteiros), como o Luigi deve escrever?",
        "options": ["int[] itens = new int[10];", "int itens = new int[10];", "int[10] itens = new int[];", "itens = int[10];"],
        "answer": "int[] itens = new int[10];",
        "rationale": {
            "int[] itens = new int[10];": "✅ Perfeito! Tipo[] nome = new Tipo[tamanho][cite: 1].",
            "int itens = new int[10];": "❌ Falta o [] no tipo para indicar que é um vetor.",
            "int[10] itens = new int[];": "❌ O tamanho deve ser definido na inicialização (lado direito).",
            "itens = int[10];": "❌ Sintaxe inválida em Java."
        },
        "tip": "Sempre use colchetes [] para declarar estruturas compostas homogêneas[cite: 1]."
    },
    {
        "id": "M1-3", "level": "Fácil",
        "prompt": "Se um vetor 'moedas' tem 100 elementos, qual o índice do último elemento?",
        "options": ["100", "99", "1", "0"],
        "answer": "99",
        "rationale": {
            "100": "❌ Mamma Mia! O índice 100 estaria fora dos limites (ArrayIndexOutOfBounds).",
            "99": "✅ Correto! Como começa em 0, o último é sempre tamanho - 1[cite: 1].",
            "1": "❌ Este seria apenas o segundo elemento.",
            "0": "❌ Este é o índice do primeiro elemento."
        },
        "tip": "Último índice = length - 1."
    },
    {
        "id": "M1-4", "level": "Fácil",
        "prompt": "O que significa dizer que um vetor é uma estrutura 'homogênea'?",
        "options": ["Pode guardar int e String juntos", "Guarda apenas elementos do mesmo tipo", "O tamanho muda dinamicamente", "Só guarda números positivos"],
        "answer": "Guarda apenas elementos do mesmo tipo",
        "rationale": {
            "Pode guardar int e String juntos": "❌ Isso seria heterogêneo. Vetores Java são rígidos!",
            "Guarda apenas elementos do mesmo tipo": "✅ Exato! Todas as 'gavetas' guardam o mesmo tipo de dado[cite: 1].",
            "O tamanho muda dinamicamente": "❌ Vetores têm tamanho fixo após criados.",
            "Só guarda números positivos": "❌ O tipo define o dado, não o sinal (pode ser int negativo)."
        },
        "tip": "Se o armário é de 'double', só entram valores 'double'[cite: 1]."
    },
    {
        "id": "M1-5", "level": "Fácil",
        "prompt": "Como descobrir quantas gavetas (tamanho) tem o vetor 'inventario'?",
        "options": ["inventario.length", "inventario.size()", "inventario.count", "inventario.tamanho"],
        "answer": "inventario.length",
        "rationale": {
            "inventario.length": "✅ Isso! .length é o atributo que nos diz o tamanho do vetor[cite: 1].",
            "inventario.size()": "❌ .size() é usado em ArrayLists, não em vetores simples.",
            "inventario.count": "❌ Não existe esse atributo em Java.",
            "inventario.tamanho": "❌ Java usa termos em inglês: length."
        },
        "tip": "Dica: length em vetores não tem parênteses ( ) pois é um atributo, não um método."
    },

    # MUNDO 2 - MÉDIO
    {
        "id": "M2-1", "level": "Médio",
        "prompt": "O Bowser tentou rodar: `int[] v = {5, 10}; System.out.println(v[2]);`. O que acontece?",
        "options": ["Imprime 0", "Imprime 10", "Erro: ArrayIndexOutOfBoundsException", "Imprime nulo"],
        "answer": "Erro: ArrayIndexOutOfBoundsException",
        "rationale": {
            "Imprime 0": "❌ Errado. O índice 2 nem existe.",
            "Imprime 10": "❌ O 10 está no índice 1.",
            "Erro: ArrayIndexOutOfBoundsException": "✅ Boom! Você tentou acessar uma gaveta que não existe no armário[cite: 1].",
            "Imprime nulo": "❌ Primitivos não são nulos e o erro impede a impressão."
        },
        "tip": "Um vetor de tamanho 2 só tem os índices 0 e 1."
    },
    {
        "id": "M2-2", "level": "Médio",
        "prompt": "Qual o loop 'for' correto para percorrer o vetor 'notas' sem causar erro?",
        "options": ["for(int i=0; i<=notas.length; i++)", "for(int i=1; i<notas.length; i++)", "for(int i=0; i<notas.length; i++)", "for(int i=0; i<10; i++)"],
        "answer": "for(int i=0; i<notas.length; i++)",
        "rationale": {
            "for(int i=0; i<=notas.length; i++)": "❌ O '=' fará o loop tentar acessar um índice inexistente no final.",
            "for(int i=1; i<notas.length; i++)": "❌ O loop pularia o primeiro elemento (índice 0).",
            "for(int i=0; i<notas.length; i++)": "✅ Perfeito! Começa no zero e vai até o último válido[cite: 1].",
            "for(int i=0; i<10; i++)": "❌ Arriscado. E se o vetor não tiver tamanho 10?"
        },
        "tip": "Sempre use i < vetor.length no seu loop."
    },
    {
        "id": "M2-3", "level": "Médio",
        "prompt": "O que faz o loop 'for-each' abaixo? `for(int x : moedas) { System.out.println(x); }`?",
        "options": ["Imprime os índices", "Imprime o conteúdo de cada gaveta", "Multiplica as moedas", "Deleta o vetor"],
        "answer": "Imprime o conteúdo de cada gaveta",
        "rationale": {
            "Imprime os índices": "❌ O for-each não te dá o índice, apenas o valor direto.",
            "Imprime o conteúdo de cada gaveta": "✅ Isso! É uma forma curta e elegante de ler todo o vetor[cite: 1].",
            "Multiplica as moedas": "❌ Não há operação de multiplicação no código.",
            "Deleta o vetor": "❌ O loop apenas lê os dados."
        },
        "tip": "Use for-each quando não precisar do número do índice (i)."
    },
    {
        "id": "M2-4", "level": "Médio",
        "prompt": "Se `int[] p = {2, 4, 6, 8};`, qual o resultado de `p[0] + p[3]`?",
        "options": ["6", "10", "12", "14"],
        "answer": "10",
        "rationale": {
            "6": "❌ Você somou p[0] e p[1].",
            "10": "✅ Wahoo! 2 (p[0]) + 8 (p[3]) = 10.",
            "12": "❌ Erro de cálculo.",
            "14": "❌ Erro de cálculo."
        },
        "tip": "Sempre identifique o valor dentro da posição antes de operar."
    },
    {
        "id": "M2-5", "level": "Médio",
        "prompt": "Vetores são estruturas 'unidimensionais'. Na aula, isso foi comparado a:",
        "options": ["Um armário horizontal com gavetas", "Uma pilha de pratos", "Um prédio de vários andares", "Uma teia de aranha"],
        "answer": "Um armário horizontal com gavetas",
        "rationale": {
            "Um armário horizontal com gavetas": "✅ Exato! Uma linha de divisões diretas[cite: 1].",
            "Uma pilha de pratos": "❌ Pilha é outro tipo de estrutura (LIFO).",
            "Um prédio de vários andares": "❌ Isso seria uma matriz (bidimensional).",
            "Uma teia de aranha": "❌ Isso seria um grafo."
        },
        "tip": "Pense em uma régua ou uma linha de gavetas numeradas[cite: 1]."
    },

    # MUNDO 3 - DIFÍCIL
    {
        "id": "M3-1", "level": "Difícil",
        "prompt": "Para calcular a média da turma, o que devemos fazer primeiro?",
        "options": ["Multiplicar as notas", "Somar todos os elementos do vetor", "Achar a maior nota", "Dividir o primeiro pelo último"],
        "answer": "Somar todos os elementos do vetor",
        "rationale": {
            "Multiplicar as notas": "❌ Isso não faz parte do cálculo de média.",
            "Somar todos os elementos do vetor": "✅ Correto! Acumulamos a soma para depois dividir pelo length[cite: 1].",
            "Achar a maior nota": "❌ Isso serve para estatística, não para a média geral.",
            "Dividir o primeiro pelo último": "❌ Lógica incorreta."
        },
        "tip": "Use uma variável `double soma = 0;` e um loop."
    },
    {
        "id": "M3-2", "level": "Difícil",
        "prompt": "Temos dois vetores: `nomes` e `notas`. Para saber a nota da 'Ana' (índice 0), usamos:",
        "options": ["nomes[0] e notas[0]", "nomes[0] e notas[1]", "nomes[Ana] e notas[Ana]", "Não é possível"],
        "answer": "nomes[0] e notas[0]",
        "rationale": {
            "nomes[0] e notas[0]": "✅ Sim! Vetores paralelos usam o mesmo índice para relacionar dados[cite: 1].",
            "nomes[0] e notas[1]": "❌ Isso pegaria a nota da pessoa errada.",
            "nomes[Ana] e notas[Ana]": "❌ Índices devem ser números inteiros, não nomes.",
            "Não é possível": "❌ É perfeitamente possível e comum."
        },
        "tip": "O índice é o 'apontador' que une as informações de vetores diferentes[cite: 1]."
    },
    {
        "id": "M3-3", "level": "Difícil",
        "prompt": "Como inicializar o 'maior valor' ao buscar o máximo em um vetor de notas?",
        "options": ["maior = 0;", "maior = notas[0];", "maior = 100;", "maior = -1;"],
        "answer": "maior = notas[0];",
        "rationale": {
            "maior = 0;": "⚠️ Funciona para notas, mas e se todos os valores fossem negativos?",
            "maior = notas[0];": "✅ Melhor prática! Começamos comparando com o primeiro elemento real[cite: 1].",
            "maior = 100;": "❌ Errado. Você nunca acharia um valor maior que 100 se ele não existisse.",
            "maior = -1;": "⚠️ Funciona para notas, mas não é universal."
        },
        "tip": "Sempre inicie buscas de extremos com um valor presente no próprio vetor."
    },
    {
        "id": "M3-4", "level": "Difícil",
        "prompt": "Qual a saída deste código: `int[] v = {1, 2, 3}; v[1] = 10; System.out.println(v[1]);`?",
        "options": ["2", "1", "10", "3"],
        "answer": "10",
        "rationale": {
            "2": "❌ O 2 foi sobrescrito pela nova atribuição.",
            "1": "❌ O 1 está no índice 0.",
            "10": "✅ Correto! Você atualizou o conteúdo daquela gaveta específica[cite: 1].",
            "3": "❌ O 3 está no índice 2."
        },
        "tip": "Vetores permitem alteração de valores (atribuição) após a criação."
    },
    {
        "id": "M3-5", "level": "Difícil",
        "prompt": "Para imprimir apenas as notas maiores ou iguais a 7 (Aprovados), qual o 'if' correto?",
        "options": ["if(notas[i] > 7)", "if(notas[i] >= 7)", "if(notas == 7)", "if(i >= 7)"],
        "answer": "if(notas[i] >= 7)",
        "rationale": {
            "if(notas[i] > 7)": "❌ Isso excluiria quem tirou exatamente 7.",
            "if(notas[i] >= 7)": "✅ Perfeito! Inclui o 7 e valores superiores[cite: 1].",
            "if(notas == 7)": "❌ Você está comparando o vetor inteiro com um número (erro).",
            "if(i >= 7)": "❌ Você está testando o índice, não a nota."
        },
        "tip": "Lembre-se de comparar o CONTEÚDO (notas[i]), não o ÍNDICE (i)."
    },

    # CASTELO DO BOWSER - DESAFIADOR
    {
        "id": "CH-1", "level": "Desafiador",
        "prompt": "O que acontece se você fizer `int[] a = {1, 2}; int[] b = a; b[0] = 9;` e imprimir `a[0]`?",
        "options": ["Imprime 1", "Imprime 9", "Erro de compilação", "Imprime 2"],
        "answer": "Imprime 9",
        "rationale": {
            "1": "❌ Errado. Em Java, vetores são objetos. 'b' e 'a' apontam para o mesmo armário.",
            "9": "✅ Exato! Ao mudar 'b', você muda o mesmo armário que 'a' está olhando.",
            "Erro de compilação": "❌ O código é perfeitamente válido.",
            "2": "❌ O 2 está no índice 1."
        },
        "tip": "Vetores em Java funcionam por referência."
    },
    {
        "id": "CH-2", "level": "Desafiador",
        "prompt": "Como inverter o valor de `v[0]` com `v[1]` sem perder dados?",
        "options": ["v[0]=v[1]; v[1]=v[0];", "int aux=v[0]; v[0]=v[1]; v[1]=aux;", "v[0]=v[1];", "int aux=v[1]; v[1]=v[1];"],
        "answer": "int aux=v[0]; v[0]=v[1]; v[1]=aux;",
        "rationale": {
            "v[0]=v[1]; v[1]=v[0];": "❌ Errado. O valor original de v[0] seria apagado na primeira linha.",
            "int aux=v[0]; v[0]=v[1]; v[1]=aux;": "✅ Bingo! A gaveta 'aux' guarda o valor para não o perdermos durante a troca.",
            "v[0]=v[1];": "❌ Só copia, não inverte.",
            "int aux=v[1]; v[1]=v[1];": "❌ Lógica sem sentido."
        },
        "tip": "Sempre use uma variável auxiliar para 'swaps'."
    },
    {
        "id": "CH-3", "level": "Desafiador",
        "prompt": "Se `int[] x = {2, 0, 1};`, qual o valor de `x[x[0]]`?",
        "options": ["2", "0", "1", "Erro"],
        "answer": "1",
        "rationale": {
            "2": "❌ x[0] é 2, mas queremos x[2].",
            "0": "❌ Este seria o valor de x[1].",
            "1": "✅ Mestre da Lógica! x[0] é 2. Logo, x[x[0]] é x[2]. O valor em x[2] é 1.",
            "Erro": "❌ O código é válido, pois 2 é um índice existente."
        },
        "tip": "Resolva o índice de dentro dos colchetes primeiro."
    },
    {
        "id": "CH-4", "level": "Desafiador",
        "prompt": "Qual o resultado de `15 % 4`? (Operador usado para verificar índices pares/ímpares)",
        "options": ["3", "1", "0", "4"],
        "answer": "3",
        "rationale": {
            "3": "✅ Correto! 15 dividido por 4 é 3, com resto 3.",
            "1": "❌ Resto incorreto.",
            "0": "❌ Não é uma divisão exata.",
            "4": "❌ O resto nunca pode ser igual ou maior que o divisor."
        },
        "tip": "O operador % (módulo) retorna o resto da divisão."
    },
    {
        "id": "CH-5", "level": "Desafiador",
        "prompt": "Para percorrer um vetor de trás para frente, como deve ser o loop?",
        "options": ["for(int i=length; i>0; i--)", "for(int i=length-1; i>=0; i--)", "for(int i=0; i<length; i--)", "for(int i=length-1; i>0; i--)"],
        "answer": "for(int i=length-1; i>=0; i--)",
        "rationale": {
            "for(int i=length; i>0; i--)": "❌ Erro: length é um índice inválido (out of bounds).",
            "for(int i=length-1; i>=0; i--)": "✅ Wahoo! Começa no último índice e para no zero, descendo[cite: 1].",
            "for(int i=0; i<length; i--)": "❌ Loop infinito ou erro imediato.",
            "for(int i=length-1; i>0; i--)": "❌ Esqueceria o elemento do índice zero."
        },
        "tip": "Comece em length-1 e use o decremento i--."
    }
]

# =========================
# LÓGICA DE NAVEGAÇÃO E SESSÃO
# =========================
if "q_order" not in st.session_state:
    order = list(range(len(QUESTIONS)))
    random.shuffle(order)
    st.session_state.q_order = order
    st.session_state.q_idx = 0
    st.session_state.corrects = 0
    st.session_state.points = 0
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    st.session_state.show_feedback = False
    st.session_state.last_choice = None
    st.session_state.student_name = ""

# Sidebar
st.sidebar.image("https://img.icons8.com/color/512/super-mario.png", width=80)
st.sidebar.title("Menu do Jogo")
if st.sidebar.button("Trocar Jogador / Reiniciar"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- LOGIN ---
if not st.session_state.student_name:
    st.info("Bem-vindo, Recruta! Identifique-se para começar o treinamento de Vetores.")
    name_input = st.text_input("Nome do Player:", placeholder="Ex: Mario Silva")
    if st.button("PRESS START"):
        if len(name_input.strip()) >= 3:
            st.session_state.student_name = name_input.strip()
            st.rerun()
        else:
            st.error("O nome deve ter pelo menos 3 caracteres.")
else:
    # --- JOGO ---
    total_q = len(QUESTIONS)
    
    if st.session_state.q_idx < total_q:
        q_real_idx = st.session_state.q_order[st.session_state.q_idx]
        q = QUESTIONS[q_real_idx]
        
        # Barra de Progresso e Stats
        st.progress(st.session_state.q_idx / total_q)
        c1, c2, c3 = st.columns(3)
        c1.write(f"🎮 **Player:** {st.session_state.student_name}")
        c2.write(f"🔥 **Streak:** {st.session_state.streak}")
        c3.write(f"🪙 **Moedas:** {st.session_state.points}")
        
        st.divider()
        st.markdown(f"### Missão {st.session_state.q_idx + 1}: {q['level']}")
        st.markdown(f"**{q['prompt']}**")
        
        if not st.session_state.show_feedback:
            # Seleção de resposta
            choice = st.radio("Escolha sua estratégia:", q["options"], key=f"radio_{q['id']}")
            if st.button("CONFIRMAR ✅"):
                st.session_state.last_choice = choice
                st.session_state.show_feedback = True
                
                # Validação
                is_correct = (choice == q["answer"])
                ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                
                if is_correct:
                    st.session_state.corrects += 1
                    st.session_state.streak += 1
                    st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.streak)
                    # Bônus de moedas por streak
                    st.session_state.points += (10 + (st.session_state.streak * 2))
                else:
                    st.session_state.streak = 0
                
                # Log de Resposta
                with open(ANSWERS_FILE, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow([ts, st.session_state.student_name, q["id"], q["level"], int(is_correct)])
                
                st.rerun()
        else:
            # EXIBIÇÃO DE FEEDBACK COM .get() PARA EVITAR KEYERROR
            choice = st.session_state.last_choice
            is_correct = (choice == q["answer"])
            
            # Busca a explicação. Se não existir no rationale, usa uma mensagem padrão.
            feedback_text = q["rationale"].get(choice, "Essa alternativa não parece ser a resposta correta para este desafio.")
            
            if is_correct:
                st.success(f"⭐ **WAHOO!** {feedback_text}")
            else:
                st.error(f"💀 **MAMMA MIA!** {feedback_text}")
                st.info(f"💡 **Dica do Toad:** {q['tip']}")
                st.warning(f"A resposta certa era: **{q['answer']}**")
            
            if st.button("PRÓXIMA FASE ➡️"):
                st.session_state.q_idx += 1
                st.session_state.show_feedback = False
                st.rerun()
    
    else:
        # --- FIM DE JOGO ---
        st.balloons()
        st.success(f"🎊 PARABÉNS, {st.session_state.student_name.upper()}! VOCÊ CONCLUIU O TREINAMENTO!")
        
        percent = (st.session_state.corrects / total_q) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Acertos Oficiais", f"{st.session_state.corrects}/{total_q}")
        col2.metric("Moedas Totais", st.session_state.points)
        col3.metric("Maior Streak", st.session_state.max_streak)
        
        st.markdown(f"### Sua nota final de precisão: **{percent:.1f}%**")
        
        # Salva Score Final
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        with open(SCORES_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                ts, st.session_state.student_name, 
                st.session_state.corrects, st.session_state.points, 
                total_q, f"{percent:.2f}", st.session_state.max_streak
            ])
        
        if st.button("RECOMEÇAR AVENTURA 🔁"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
