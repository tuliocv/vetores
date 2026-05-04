import os
import csv
import random
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st

# =========================
# 🍄 CONFIGURAÇÃO E ESTILO (CORREÇÃO HTML)
# =========================
st.set_page_config(page_title="Mario Vector Adventure", page_icon="🍄", layout="centered")

# Correção: parâmetro 'unsafe_allow_html' para carregar o CSS gamer
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        background-color: #e74c3c; 
        color: white; 
        font-weight: bold;
        border: 2px solid #b22222;
    }
    .stButton>button:hover { 
        background-color: #ff4d4d; 
        border: 2px solid #f1c40f; 
    }
    .stProgress > div > div > div > div { background-color: #2ecc71; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍄 Mario Vector Adventure")
st.caption(f"Revisão para Avaliação A1 | {datetime.now().strftime('%d/%m/%Y')}")

# =========================
# 💾 PERSISTÊNCIA DE DADOS
# =========================
DATA_DIR = Path("data_mario_final")
DATA_DIR.mkdir(parents=True, exist_ok=True)
SCORES_FILE = DATA_DIR / "scores.csv"
ANSWERS_FILE = DATA_DIR / "answers.csv"

def ensure_files():
    if not SCORES_FILE.exists():
        with open(SCORES_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["ts", "name", "correct", "points", "total", "percent"])
    if not ANSWERS_FILE.exists():
        with open(ANSWERS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["ts", "name", "qid", "is_correct"])

ensure_files()

# =========================
# 🎮 BANCO DE QUESTÕES (20 ITENS)
# =========================
QUESTIONS = [
    # --- MUNDO 1: FÁCIL (Conceitos Iniciais) ---
    {
        "id": "M1-1", "level": "Fácil",
        "prompt": "O Mario criou: `int[] bau = {10, 20, 30};`. Qual o valor em `bau[0]`?",
        "options": ["0", "10", "20", "30"], "answer": "10",
        "rationale": {"10": "✅ Wahoo! Em Java, o índice 0 acessa a primeira posição.", "0": "❌ O índice é 0, mas o valor guardado lá é 10."},
        "tip": "Vetores são indexados a partir de zero[cite: 1]."
    },
    {
        "id": "M1-2", "level": "Fácil",
        "prompt": "Como o Luigi declara um vetor de 5 decimais vazio?",
        "options": ["double[] v = new double[5];", "double v = new double[5];", "double[5] v;", "array v[5];"], "answer": "double[] v = new double[5];",
        "rationale": {"double[] v = new double[5];": "✅ Correto! Tipo[] nome = new Tipo[tamanho][cite: 1]."},
        "tip": "Use colchetes para indicar que a variável é composta e homogênea[cite: 1]."
    },
    {
        "id": "M1-3", "level": "Fácil",
        "prompt": "Qual o atributo que retorna o tamanho de um vetor?",
        "options": [".size()", ".count", ".length", ".capacity"], "answer": ".length",
        "rationale": {".length": "✅ Isso! O atributo .length informa o número total de gavetas[cite: 1]."},
        "tip": "Length não tem parênteses em vetores nativos[cite: 1]."
    },
    {
        "id": "M1-4", "level": "Fácil",
        "prompt": "Se um vetor tem length 10, qual o último índice válido?",
        "options": ["10", "11", "9", "0"], "answer": "9",
        "rationale": {"9": "✅ Correto! O último índice é sempre length - 1[cite: 1]."},
        "tip": "Sempre subtraia 1 para evitar erros de limite[cite: 1]."
    },
    {
        "id": "M1-5", "level": "Fácil",
        "prompt": "Um vetor 'homogêneo' significa que:",
        "options": ["Aceita tipos diferentes", "Todos os elementos são do mesmo tipo", "O tamanho muda sozinho", "Não aceita números"], "answer": "Todos os elementos são do mesmo tipo",
        "rationale": {"Todos os elementos são do mesmo tipo": "✅ Exato! Se o armário é de int, todas as gavetas guardam int[cite: 1]."},
        "tip": "A estrutura é composta, mas o tipo de dado é único[cite: 1]."
    },
    # --- MUNDO 2: MÉDIO (Acesso e Loops) ---
    {
        "id": "M2-1", "level": "Médio",
        "prompt": "O Bowser acessou `v[5]` em um vetor de tamanho 5. O que ocorre?",
        "options": ["Imprime 0", "Imprime o último valor", "Erro: ArrayIndexOutOfBounds", "Imprime null"], "answer": "Erro: ArrayIndexOutOfBounds",
        "rationale": {"Erro: ArrayIndexOutOfBounds": "✅ Mamma Mia! Se o tamanho é 5, os índices vão de 0 a 4[cite: 1]."},
        "tip": "Nunca acesse o índice igual ao length[cite: 1]."
    },
    {
        "id": "M2-2", "level": "Médio",
        "prompt": "Qual a condição correta para um loop 'for' percorrer o vetor todo?",
        "options": ["i <= v.length", "i < v.length", "i == v.length", "i < 10"], "answer": "i < v.length",
        "rationale": {"i < v.length": "✅ Correto! Isso garante que o loop pare antes de atingir um índice inválido[cite: 1]."},
        "tip": "A condição de parada deve ser estritamente menor que o tamanho[cite: 1]."
    },
    {
        "id": "M2-3", "level": "Médio",
        "prompt": "O que faz o loop 'for-each'? `for(int x : v)`",
        "options": ["Acessa os índices", "Acessa os conteúdos diretamente", "Inverte o vetor", "Deleta o vetor"], "answer": "Acessa os conteúdos diretamente",
        "rationale": {"Acessa os conteúdos diretamente": "✅ Wahoo! Ele percorre os valores sem precisar gerenciar o índice[cite: 1]."},
        "tip": "Ótimo para leitura, mas não serve para alterar posições específicas[cite: 1]."
    },
    {
        "id": "M2-4", "level": "Médio",
        "prompt": "Se `int[] p = {2, 5, 8};`, qual o valor de `p[1]`?",
        "options": ["2", "5", "8", "1"], "answer": "5",
        "rationale": {"5": "✅ Correto! O 5 está na segunda posição (índice 1)[cite: 1]."},
        "tip": "O índice aponta para a gaveta desejada[cite: 1]."
    },
    {
        "id": "M2-5", "level": "Médio",
        "prompt": "Vetores são comparados a armários horizontais por serem:",
        "options": ["Unidimensionais", "Bidimensionais", "Infinitos", "Dinâmicos"], "answer": "Unidimensionais",
        "rationale": {"Unidimensionais": "✅ Isso! Possuem apenas uma dimensão (uma linha de gavetas)[cite: 1]."},
        "tip": "Estrutura linear composta homogênea[cite: 1]."
    },
    # --- MUNDO 3: DIFÍCIL (Processamento) ---
    {
        "id": "M3-1", "level": "Difícil",
        "prompt": "Para calcular a média de 10 notas em um vetor, qual a lógica?",
        "options": ["Soma / length", "Soma * length", "Soma / 2", "Notas[9]"], "answer": "Soma / length",
        "rationale": {"Soma / length": "✅ Correto! Somamos tudo e dividimos pelo total de elementos[cite: 1]."},
        "tip": "O length representa o total de alunos processados[cite: 1]."
    },
    {
        "id": "M3-2", "level": "Difícil",
        "prompt": "Em vetores paralelos (nomes e notas), a relação é feita por:",
        "options": ["Nomes das variáveis", "Mesmo índice", "Ponteiros", "Não há relação"], "answer": "Mesmo índice",
        "rationale": {"Mesmo índice": "✅ Bingo! O índice 3 de 'nomes' pertence à nota no índice 3 de 'notas'[cite: 1]."},
        "tip": "O apontador (índice) une as informações paralelas[cite: 1]."
    },
    {
        "id": "M3-3", "level": "Difícil",
        "prompt": "Qual o melhor valor inicial para achar a 'maior nota' no vetor?",
        "options": ["0", "A primeira nota do vetor", "100", "-1"], "answer": "A primeira nota do vetor",
        "rationale": {"A primeira nota do vetor": "✅ Perfeito! Assim você garante que está comparando com valores reais[cite: 1]."},
        "tip": "Use notas[0] como ponto de partida para a comparação[cite: 1]."
    },
    {
        "id": "M3-4", "level": "Difícil",
        "prompt": "Como atualizar o valor da terceira posição de um vetor 'v' para 10?",
        "options": ["v[3]=10;", "v[2]=10;", "v=10;", "set(v, 2, 10);"], "answer": "v[2]=10;",
        "rationale": {"v[2]=10;": "✅ Sim! A terceira posição é o índice 2[cite: 1]."},
        "tip": "Atribuição em vetor: nome[indice] = valor[cite: 1]."
    },
    {
        "id": "M3-5", "level": "Difícil",
        "prompt": "O que acontece em: `int[] a = {1, 2}; int[] b = a; b[0] = 5;`? Qual `a[0]`?",
        "options": ["1", "5", "2", "Erro"], "answer": "5",
        "rationale": {"5": "✅ Cuidado! 'b' aponta para o mesmo armário de 'a'. Mudou em um, mudou no outro[cite: 1]."},
        "tip": "Vetores em Java são tratados por referência."
    },
    # --- CASTELO: DESAFIADOR (Lógica Avançada) ---
    {
        "id": "CH-1", "level": "Desafiador",
        "prompt": "Qual a saída de `x[x[1]]` se `x = {2, 0, 1}`?",
        "options": ["0", "1", "2", "Erro"], "answer": "2",
        "rationale": {"2": "✅ Lógica pura! x[1] é 0. Então x[0] é 2[cite: 1]."},
        "tip": "Resolva o índice de dentro para fora[cite: 1]."
    },
    {
        "id": "CH-2", "level": "Desafiador",
        "prompt": "Para inverter valores entre v[0] e v[1], o que é essencial?",
        "options": ["Um loop", "Uma variável auxiliar", "Um novo vetor", "O método reverse()"], "answer": "Uma variável auxiliar",
        "rationale": {"Uma variável auxiliar": "✅ Correto! Precisamos de uma gaveta extra para não perder o valor original durante a troca[cite: 1]."},
        "tip": "int aux = v[0]; v[0] = v[1]; v[1] = aux;[cite: 1]."
    },
    {
        "id": "CH-3", "level": "Desafiador",
        "prompt": "Como imprimir o vetor de trás para frente?",
        "options": ["i=0 até length", "i=length até 0", "i=length-1 até 0", "Não é possível"], "answer": "i=length-1 até 0",
        "rationale": {"i=length-1 até 0": "✅ Isso! Começa no último índice válido e decrementa[cite: 1]."},
        "tip": "O loop deve ser `i--`[cite: 1]."
    },
    {
        "id": "CH-4", "level": "Desafiador",
        "prompt": "O operador `% 2 == 0` serve para:",
        "options": ["Achar números ímpares", "Achar números pares", "Dividir por 2", "Zerar o vetor"], "answer": "Achar números pares",
        "rationale": {"Achar números pares": "✅ Correto! Verifica se o resto da divisão por 2 é zero[cite: 1]."},
        "tip": "Útil para processar apenas posições ou valores pares[cite: 1]."
    },
    {
        "id": "CH-5", "level": "Desafiador",
        "prompt": "Na máquina de bebidas, por que `menu[opcao - 1]`?",
        "options": ["Para somar o preço", "Porque o humano conta de 1 e o Java de 0", "Para pular o café", "É um erro"], "answer": "Porque o humano conta de 1 e o Java de 0",
        "rationale": {"Porque o humano conta de 1 e o Java de 0": "✅ Exato! O item 1 está na gaveta 0[cite: 1]."},
        "tip": "Sempre mapeie a interface do usuário para a lógica do vetor[cite: 1]."
    }
]

# =========================
# 🕹️ LÓGICA DO JOGO
# =========================
if "q_order" not in st.session_state:
    order = list(range(len(QUESTIONS)))
    random.shuffle(order)
    st.session_state.update({
        "q_order": order, "q_idx": 0, "corrects": 0, "points": 0, 
        "streak": 0, "show_fb": False, "last_choice": None, "student_name": ""
    })

if not st.session_state.student_name:
    st.info("🍄 Bem-vindo ao Reino dos Vetores! Identifique-se para começar.")
    name = st.text_input("Player Name:", placeholder="Mario Silva")
    if st.button("PRESS START"):
        if len(name.strip()) >= 3:
            st.session_state.student_name = name.strip()
            st.rerun()
        else:
            st.error("Nome muito curto!")
else:
    total_q = len(QUESTIONS)
    if st.session_state.q_idx < total_q:
        q = QUESTIONS[st.session_state.q_order[st.session_state.q_idx]]
        
        # Header e Stats
        st.progress(st.session_state.q_idx / total_q)
        st.write(f"🎮 **{st.session_state.student_name}** | 🔥 Streak: {st.session_state.streak} | 🪙 Moedas: {st.session_state.points}")
        
        st.divider()
        st.markdown(f"### Missão {st.session_state.q_idx + 1}: {q['level']}")
        st.write(q["prompt"])
        
        if not st.session_state.show_fb:
            choice = st.radio("Selecione a ação:", q["options"], key=f"r_{q['id']}")
            if st.button("CONFIRMAR ✅"):
                st.session_state.last_choice = choice
                st.session_state.show_fb = True
                is_correct = (choice == q["answer"])
                
                if is_correct:
                    st.session_state.corrects += 1
                    st.session_state.streak += 1
                    st.session_state.points += (10 + (st.session_state.streak * 2))
                else:
                    st.session_state.streak = 0
                
                # Log de Resposta
                with open(ANSWERS_FILE, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow([datetime.now(), st.session_state.student_name, q["id"], int(is_correct)])
                st.rerun()
        else:
            # FEEDBACK COM .get() PARA EVITAR KEYERROR
            choice = st.session_state.last_choice
            is_correct = (choice == q["answer"])
            fb = q["rationale"].get(choice, "Essa alternativa não leva ao castelo da lógica.")
            
            if is_correct:
                st.success(f"⭐ **WAHOO!** {fb}")
            else:
                st.error(f"💀 **MAMMA MIA!** {fb}")
                st.warning(f"Resposta certa: **{q['answer']}**")
                st.info(f"💡 **Dica do Toad:** {q['tip']}")
            
            if st.button("PRÓXIMA FASE ➡️"):
                st.session_state.q_idx += 1
                st.session_state.show_fb = False
                st.rerun()
    else:
        st.balloons()
        st.success(f"🎊 FIM DE JOGO! {st.session_state.student_name.upper()} SALVOU A PRINCESA!")
        st.metric("Acertos Oficiais", f"{st.session_state.corrects}/{total_q}")
        st.metric("Moedas Acumuladas", st.session_state.points)
        
        # Salva Final Score
        with open(SCORES_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([datetime.now(), st.session_state.student_name, st.session_state.corrects, st.session_state.points, total_q, (st.session_state.corrects/total_q)*100])
        
        if st.button("RECOMEÇAR AVENTURA 🔁"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
