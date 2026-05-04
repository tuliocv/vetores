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
    # --- MUNDO 1 (ALINHADO À AULA) ---
    {"id": "M1-1", "level": "Fácil", "prompt": "Qual o valor padrão de um elemento em 'int[] v = new int[5];'?", "options": ["null", "0", "1", "Lixo"], "answer": "0", "rationale": {"0": "✅ Wahoo! Java inicializa vetores numéricos primitivos com zero automaticamente."}, "tip": "Primitivos numéricos sempre começam com zero."},
    {"id": "M1-2", "level": "Fácil", "prompt": "O que define um vetor como 'homogêneo'?", "options": ["Tamanho fixo", "Mesma cor", "Elementos do mesmo tipo", "Mudar de tamanho"], "answer": "Elementos do mesmo tipo", "rationale": {"Elementos do mesmo tipo": "✅ Exato! Todas as gavetas guardam o mesmo tipo de dado."}, "tip": "Homogêneo = mesma natureza[cite: 1]."},
    {"id": "M1-3", "level": "Fácil", "prompt": "Qual a sintaxe correta para declarar um vetor de Strings?", "options": ["String v = new[5];", "String[] v = new String[5];", "array v[5];", "v = String[5];"], "answer": "String[] v = new String[5];", "rationale": {"String[] v = new String[5];": "✅ Perfeito! Tipo[] nome = new Tipo[tamanho][cite: 1]."}, "tip": "Use [] para indicar estrutura composta[cite: 1]."},
    {"id": "M1-4", "level": "Fácil", "prompt": "Em um vetor de tamanho N, qual o último índice válido?", "options": ["N", "N+1", "N-1", "0"], "answer": "N-1", "rationale": {"N-1": "✅ Isso! Se começa em 0, termina em total-1[cite: 1]."}, "tip": "Se length é 10, o último é 9[cite: 1]."},
    {"id": "M1-5", "level": "Fácil", "prompt": "O atributo '.length' retorna:", "options": ["Maior valor", "Último índice", "Quantidade total de gavetas", "Espaço livre"], "answer": "Quantidade total de gavetas", "rationale": {"Quantidade total de gavetas": "✅ Correto! Ele informa a capacidade total do vetor[cite: 1]."}, "tip": "Dica: .length não tem parênteses em vetores[cite: 1]."},
    {"id": "M1-6", "level": "Fácil", "prompt": "Onde o vetor 'objeto' fica guardado na memória?", "options": ["Pilha", "Heap", "Cache", "Disco"], "answer": "Heap", "rationale": {"Heap": "✅ Correto! Vetores são objetos e vivem no Heap dinâmico."}, "tip": "A variável é o endereço, o vetor é o objeto no Heap."},
    {"id": "M1-7", "level": "Fácil", "prompt": "int[] v = {2, 4, 6}; Qual o valor de v[2]?", "options": ["2", "4", "6", "Erro"], "answer": "6", "rationale": {"6": "✅ Exato! O terceiro elemento está no índice 2[cite: 1]."}, "tip": "Conte: 0, 1, 2..."},

    # --- MUNDO 2 (ALINHADO À AULA) ---
    {"id": "M2-1", "level": "Médio", "prompt": "Qual loop causa 'ArrayIndexOutOfBoundsException'?", "options": ["i < v.length", "i <= v.length", "i == 0", "i--"], "answer": "i <= v.length", "rationale": {"i <= v.length": "✅ Erro clássico! O '=' tenta acessar um índice que não existe no final[cite: 1]."}, "tip": "A condição deve ser estritamente menor que length[cite: 1]."},
    {"id": "M2-2", "level": "Médio", "prompt": "No loop 'for (int x : v)', a variável 'x' é:", "options": ["O índice", "O endereço", "O conteúdo da posição", "O tamanho"], "answer": "O conteúdo da posição", "rationale": {"O conteúdo da posição": "✅ Wahoo! O for-each lê o valor direto da gaveta[cite: 1]."}, "tip": "Útil para leitura rápida sem índices[cite: 1]."},
    {"id": "M2-3", "level": "Médio", "prompt": "Para somar valores, a variável acumuladora inicia em:", "options": ["1", "null", "0", "length"], "answer": "0", "rationale": {"0": "✅ Sim! O neutro da soma é zero[cite: 1]."}, "tip": "Comece o balde vazio para somar moedas[cite: 1]."},
    {"id": "M2-4", "level": "Médio", "prompt": "Em vetores paralelos, como ligar Nome e Nota?", "options": ["Mesmo índice", "Mesmo nome", "Ponteiros", "Nomes[Nota]"], "answer": "Mesmo índice", "rationale": {"Mesmo índice": "✅ Bingo! O índice compartilhado une as informações[cite: 1]."}, "tip": "Apontador comum para estruturas diferentes[cite: 1]."},
    {"id": "M2-5", "level": "Médio", "prompt": "O que faz 'v[i] = v[i] * 2;'?", "options": ["Dobra o tamanho", "Dobra o valor do elemento", "Apaga tudo", "Cria novo"], "answer": "Dobra o valor do elemento", "rationale": {"Dobra o valor do elemento": "✅ Isso! Atualiza o conteúdo da gaveta atual[cite: 1]."}, "tip": "Atribuição direta no índice i[cite: 1]."},
    {"id": "M2-6", "level": "Médio", "prompt": "Desvantagem do for-each:", "options": ["Lento", "Não permite alterar valores", "Só inteiros", "Não compila"], "answer": "Não permite alterar valores", "rationale": {"Não permite alterar valores": "✅ Exato! Ele serve apenas para leitura[cite: 1]."}, "tip": "Para mudar o valor, use o for tradicional com índice[cite: 1]."},
    {"id": "M2-7", "level": "Médio", "prompt": "Para percorrer apenas a metade do vetor:", "options": ["i < v.length / 2", "i < v.length", "i < 2", "i = 5"], "answer": "i < v.length / 2", "rationale": {"i < v.length / 2": "✅ Isso! Divide o limite de iterações por 2[cite: 1]."}, "tip": "Aritmética no limite do loop[cite: 1]."},

    # --- MUNDO 3 (ALINHADO À AULA) ---
    {"id": "M3-1", "level": "Difícil", "prompt": "Se 'b = a;', e mudamos 'b[0] = 99;', o que ocorre com 'a[0]'?", "options": ["Igual", "Muda para 99", "null", "Erro"], "answer": "Muda para 99", "rationale": {"Muda para 99": "✅ Mamma Mia! Em Java, b e a agora apontam para o mesmo objeto."}, "tip": "Atribuição de vetores copia a referência, não os dados."},
    {"id": "M3-2", "level": "Difícil", "prompt": "Qual cria uma cópia independente?", "options": ["v.copy()", "v.clone()", "v = b", "v.dup()"], "answer": "v.clone()", "rationale": {"v.clone()": "✅ Isso! Aloca um novo espaço de memória independente."}, "tip": "Clone gera um novo armário idêntico."},
    {"id": "M3-3", "level": "Difícil", "prompt": "Lógica para achar o MENOR valor:", "options": ["if (v[i] > menor)", "if (v[i] < menor)", "menor = length", "menor = 0"], "answer": "if (v[i] < menor)", "rationale": {"if (v[i] < menor)": "✅ Correto! Atualiza se achar alguém menor[cite: 1]."}, "tip": "Compare o atual com o recordista atual[cite: 1]."},
    {"id": "M3-4", "level": "Difícil", "prompt": "Gavetas vazias de String[] contêm:", "options": ["\"\"", "0", "null", "Erro"], "answer": "null", "rationale": {"null": "✅ Exato! Referências não inicializadas são null."}, "tip": "Objetos começam nulos."},
    {"id": "M3-5", "level": "Difícil", "prompt": "Pior caso da busca linear (tam 1000):", "options": ["1", "500", "1000", "0"], "answer": "1000", "rationale": {"1000": "✅ Isso! No pior caso, olha-se tudo."}, "tip": "Busca sequencial completa."},
    {"id": "M3-6", "level": "Difícil", "prompt": "Função do 'Arrays.sort(v);':", "options": ["Embaralhar", "Somar", "Ordenar", "Excluir"], "answer": "Ordenar", "rationale": {"Ordenar": "✅ Wahoo! Organiza os dados em ordem crescente."}, "tip": "Biblioteca java.util.Arrays."},
    {"id": "M3-7", "level": "Difícil", "prompt": "Vetores passados para métodos são:", "options": ["Copiados", "Por referência", "Ignorados", "Texto"], "answer": "Por referência", "rationale": {"Por referência": "✅ Sim! Mudanças no método afetam o vetor original."}, "tip": "O método recebe o endereço do armário."},

    # --- CASTELO (DESAFIADOR - ALÉM DA AULA) ---
    {"id": "CH-1", "level": "Desafiador", "prompt": "Causa de 'NegativeArraySizeException'?", "options": ["Índice -1", "new int[-10]", "Soma neg", "Diminuir"], "answer": "new int[-10]", "rationale": {"new int[-10]": "✅ Bingo! Não se cria vetor com tamanho negativo."}, "tip": "Tamanho deve ser zero ou positivo[cite: 1]."},
    {"id": "CH-2", "level": "Desafiador", "prompt": "Como fazer o SWAP (troca) de v[0] e v[1]?", "options": ["0=1; 1=0", "aux=0; 0=1; 1=aux", "v[0] <-> v[1]", "swap(v)"], "answer": "aux=0; 0=1; 1=aux", "rationale": {"aux=0; 0=1; 1=aux": "✅ Isso! A gaveta auxiliar evita a perda de dados[cite: 1]."}, "tip": "Sempre use um temporário[cite: 1]."},
    {"id": "CH-3", "level": "Desafiador", "prompt": "Uma matriz 'int[][] m' é:", "options": ["Cubo", "Vetor de vetores", "String", "Excel"], "answer": "Vetor de vetores", "rationale": {"Vetor de vetores": "✅ Exato! Cada linha é um vetor independente."}, "tip": "Estrutura multidimensional no Java."},
    {"id": "CH-4", "level": "Desafiador", "prompt": "Resultado de 'v[v.length]':", "options": ["Último", "Tamanho", "Erro: OOB", "0"], "answer": "Erro: OOB", "rationale": {"Erro: OOB": "✅ Correto! O índice length está fora do limite[cite: 1]."}, "tip": "O limite é sempre length - 1[cite: 1]."},
    {"id": "CH-5", "level": "Desafiador", "prompt": "Complexidade de acesso via índice:", "options": ["O(n)", "O(1)", "O(log n)", "O(n^2)"], "answer": "O(1)", "rationale": {"O(1)": "✅ Isso! O acesso é direto e instantâneo."}, "tip": "Tempo constante."},
    {"id": "CH-6", "level": "Desafiador", "prompt": "Redimensionar um vetor nativo:", "options": ["v.resize", "Não é possível", "Automático", "Diminui"], "answer": "Não é possível", "rationale": {"Não é possível": "✅ Correto! Vetores têm tamanho estático[cite: 1]."}, "tip": "Para mudar, crie um novo armário[cite: 1]."},
    {"id": "CH-7", "level": "Desafiador", "prompt": "x={1, 2, 3}; Valor de x[x[x[0]]]:", "options": ["1", "2", "3", "Erro"], "answer": "3", "rationale": {"3": "✅ Gênio! x[0]=1 -> x[1]=2 -> x[2]=3[cite: 1]."}, "tip": "Resolva de dentro para fora[cite: 1]."}
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
