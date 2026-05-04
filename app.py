import os
import csv
import random
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st

# =========================
# CONFIGURAÇÃO TEMÁTICA
# =========================
st.set_page_config(page_title="Mario Vector Adventure", page_icon="🍄", layout="centered")
st.title("🍄 Mario Vector Adventure: Java Edition")
st.caption("Domine os Arrays (Vetores) e ajude o Mario a resgatar a lógica perdida!")

# =========================
# STORAGE (CSV) - Persistência
# =========================
DATA_DIR = Path("data_mario")
DATA_DIR.mkdir(parents=True, exist_ok=True)
SCORES_FILE = DATA_DIR / "mario_scores.csv"
ANSWERS_FILE = DATA_DIR / "mario_answers.csv"
PROGRESS_FILE = DATA_DIR / "mario_progress.csv"

SCORES_HEADERS = ["timestamp_utc", "student_name", "base_correct", "final_points", "total", "percent", "max_streak"]
ANS_HEADERS = ["timestamp_utc", "student_name", "question_id", "level", "is_correct"]
PROGRESS_HEADERS = ["timestamp_utc", "student_name", "q_index", "total", "base_correct", "final_points", "status"]

def ensure_files():
    for p, h in [(SCORES_FILE, SCORES_HEADERS), (ANSWERS_FILE, ANS_HEADERS), (PROGRESS_FILE, PROGRESS_HEADERS)]:
        if not p.exists():
            with open(p, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(h)

ensure_files()

# =========================
# QUESTÕES (20 EXERCÍCIOS)
# =========================
# Baseado na Aula 12: Vetores, Índices e Loops
QUESTIONS = [
    # --- FÁCIL (Mundo 1: Green Hill Road) ---
    {
        "id": "M1-1", "level": "Fácil",
        "prompt": "O Mario criou um vetor: int[] moedas = {10, 20, 30}. Qual o valor no índice 0?",
        "options": ["0", "10", "20", "30"],
        "answer": "10",
        "rationale": {
            "0": "❌ O índice começa em 0, mas o valor lá é o primeiro elemento.",
            "10": "✅ Wahoo! Em Java, o primeiro elemento está na posição 0.",
            "20": "❌ 20 está no índice 1.",
            "30": "❌ 30 está no índice 2."
        },
        "tip": "Arrays em Java são 'zero-indexed'."
    },
    {
        "id": "M1-2", "level": "Fácil",
        "prompt": "Como o Luigi pode descobrir o tamanho total do vetor 'itens'?",
        "options": ["itens.size()", "itens.length", "itens.count", "itens.capacity"],
        "answer": "itens.length",
        "rationale": {
            "itens.size()": "❌ .size() é usado em listas, não em arrays simples.",
            "itens.length": "✅ Correto! O atributo .length retorna o número de gavetas[cite: 1].",
            "itens.count": "❌ Não existe este atributo para vetores em Java.",
            "itens.capacity": "❌ Termo incorreto para Java."
        },
        "tip": "O length é um atributo, não um método (não tem parênteses)."
    },
    {
        "id": "M1-3", "level": "Fácil",
        "prompt": "Se um vetor tem length = 5, qual o índice da última gaveta?",
        "options": ["5", "6", "4", "0"],
        "answer": "4",
        "rationale": {
            "5": "❌ Se começar em 0, o 5 está fora dos limites!",
            "4": "✅ Isso! O último índice é sempre length - 1[cite: 1].",
            "0": "❌ Este é o primeiro índice."
        },
        "tip": "Sempre subtraia 1 do total para achar o último índice."
    },
    {
        "id": "M1-4", "level": "Fácil",
        "prompt": "Um vetor 'homogêneo' significa que:",
        "options": ["Aceita int e String juntos", "Todos os dados são do mesmo tipo", "O tamanho muda sozinho", "Só aceita números"],
        "answer": "Todos os dados são do mesmo tipo",
        "rationale": {
            "Aceita int e String juntos": "❌ Isso seria heterogêneo.",
            "Todos os dados são do mesmo tipo": "✅ Correto! Todos na mesma 'gaveta' devem ser iguais[cite: 1].",
            "O tamanho muda sozinho": "❌ Vetores têm tamanho fixo após criados."
        },
        "tip": "Pense no armário da aula: se é de sapatos, só entra sapatos[cite: 1]."
    },
    {
        "id": "M1-5", "level": "Fácil",
        "prompt": "Qual a forma correta de declarar um vetor de decimais?",
        "options": ["double medias[]", "double[] medias", "array medias", "vector medias"],
        "answer": "double[] medias",
        "rationale": {
            "double[] medias": "✅ Padrão Java recomendado!",
            "double medias[]": "⚠️ Funciona, mas não é a convenção moderna.",
            "array medias": "❌ 'array' não é uma palavra reservada de tipo."
        },
        "tip": "O tipo seguido de [] é a marca registrada do vetor[cite: 1]."
    },

    # --- MÉDIO (Mundo 2: Desert Land) ---
    {
        "id": "M2-1", "level": "Médio",
        "prompt": "O que acontece ao executar: System.out.println(vetor[5]) se o length for 5?",
        "options": ["Imprime 0", "Imprime o último valor", "Erro: ArrayIndexOutOfBounds", "Imprime nulo"],
        "answer": "Erro: ArrayIndexOutOfBounds",
        "rationale": {
            "Erro: ArrayIndexOutOfBounds": "✅ Mamma Mia! O índice 5 não existe se o tamanho é 5 (vai de 0 a 4)[cite: 1].",
            "Imprime o último valor": "❌ O último seria o índice 4."
        },
        "tip": "Cuidado com o erro clássico de 'fora de limite'."
    },
    {
        "id": "M2-2", "level": "Médio",
        "prompt": "Para percorrer o vetor 'notas', qual o cabeçalho correto do loop?",
        "options": ["for(int i=0; i<=notas.length; i++)", "for(int i=1; i<=notas.length; i++)", "for(int i=0; i<notas.length; i++)", "for(int i=0; i<10; i++)"],
        "answer": "for(int i=0; i<notas.length; i++)",
        "rationale": {
            "for(int i=0; i<=notas.length; i++)": "❌ O <= causará erro no último índice.",
            "for(int i=0; i<notas.length; i++)": "✅ Perfeito! Começa no 0 e para antes do length[cite: 1].",
            "for(int i=1; i<=notas.length; i++)": "❌ Perderia o primeiro elemento (0)."
        },
        "tip": "A condição deve ser sempre i < length."
    },
    {
        "id": "M2-3", "level": "Médio",
        "prompt": "O Bowser quer mudar o valor da primeira posição. Como ele faz?",
        "options": ["vetor[0] = 10;", "vetor.first = 10;", "vetor[1] = 10;", "set(vetor, 10);"],
        "answer": "vetor[0] = 10;",
        "rationale": {
            "vetor[0] = 10;": "✅ Direto na gaveta 0!",
            "vetor[1] = 10;": "❌ Isso mudaria a segunda posição."
        },
        "tip": "Use o operador de atribuição = junto com o índice."
    },
    {
        "id": "M2-4", "level": "Médio",
        "prompt": "Qual o resultado de: int[] v={4, 8, 15}; System.out.println(v[1] + v[2]);",
        "options": ["12", "23", "27", "15"],
        "answer": "23",
        "rationale": {
            "23": "✅ v[1] é 8 e v[2] é 15. 8 + 15 = 23.",
            "12": "❌ Você somou v[0] e v[1].",
            "27": "❌ Valor incorreto."
        },
        "tip": "Identifique o conteúdo de cada posição antes de somar[cite: 1]."
    },
    {
        "id": "M2-5", "level": "Médio",
        "prompt": "O loop for-each (for(int x : vetor)) serve para:",
        "options": ["Alterar valores do vetor", "Apenas ler os valores", "Inverter o vetor", "Deletar o vetor"],
        "answer": "Apenas ler os valores",
        "rationale": {
            "Apenas ler os valores": "✅ Sim! Ele é prático para exibição e cálculos simples[cite: 1].",
            "Alterar valores": "❌ Para alterar, precisamos do índice (i), que o for-each não fornece."
        },
        "tip": "For-each é ótimo para o 'Boletim Final' (leitura)."
    },

    # --- DIFÍCIL (Mundo 3: Water World) ---
    {
        "id": "M3-1", "level": "Difícil",
        "prompt": "Como calcular a média de um vetor 'notas' de 10 posições?",
        "options": ["soma / 10.0", "soma * 10", "notas.average()", "soma / notas[9]"],
        "answer": "soma / 10.0",
        "rationale": {
            "soma / 10.0": "✅ Soma-se tudo e divide pelo length (que é 10)[cite: 1].",
            "notas.average()": "❌ Arrays nativos não possuem esse método direto."
        },
        "tip": "Use uma variável acumuladora dentro de um loop."
    },
    {
        "id": "M3-2", "level": "Difícil",
        "prompt": "Para achar o MAIOR valor no vetor 'medias', qual a lógica correta?",
        "options": ["if(m > maior) { maior = m; }", "if(m < maior) { maior = m; }", "maior = medias.max();", "maior = medias[10];"],
        "answer": "if(m > maior) { maior = m; }",
        "rationale": {
            "if(m > maior) { maior = m; }": "✅ Se o valor atual for maior que o guardado, atualizamos o trono[cite: 1].",
            "if(m < maior)": "❌ Isso acharia o menor valor."
        },
        "tip": "Inicie a variável 'maior' com a primeira posição do vetor."
    },
    {
        "id": "M3-3", "level": "Difícil",
        "prompt": "Considerando vetores paralelos (nomes e notas), se o maior valor está no índice 3 de 'notas', onde está o nome do dono?",
        "options": ["Índice 0 de nomes", "Índice 3 de nomes", "Índice 4 de nomes", "Não há relação"],
        "answer": "Índice 3 de nomes",
        "rationale": {
            "Índice 3 de nomes": "✅ Exato! A relação é mantida pelo índice compartilhado[cite: 1].",
            "Não há relação": "❌ Há sim, se os vetores forem populados em ordem paralela."
        },
        "tip": "O 'apontador' serve para os dois vetores ao mesmo tempo."
    },
    {
        "id": "M3-4", "level": "Difícil",
        "prompt": "O que este código faz? for(int i=0; i<v.length/2; i++) { ... }",
        "options": ["Percorre o vetor todo", "Percorre apenas a metade", "Dá erro de compilação", "Multiplica o vetor"],
        "answer": "Percorre apenas a metade",
        "rationale": {
            "Percorre apenas a metade": "✅ Útil para algoritmos de inversão de valores.",
            "Percorre o vetor todo": "❌ O limite é length dividido por 2."
        },
        "tip": "Operações aritméticas podem ser usadas no limite do loop[cite: 1]."
    },
    {
        "id": "M3-5", "level": "Difícil",
        "prompt": "Como instanciar um vetor de inteiros já com os valores 1, 2, 3?",
        "options": ["int[] v = {1, 2, 3};", "int v = [1, 2, 3];", "new Array(1,2,3);", "int[] v = new int(3);"],
        "answer": "int[] v = {1, 2, 3};",
        "rationale": {
            "int[] v = {1, 2, 3};": "✅ Inicialização estática direta.",
            "int v = [1, 2, 3];": "❌ Sintaxe de outras linguagens (como Python/JS)."
        },
        "tip": "As chaves {} são usadas para inicializar valores em Java[cite: 1]."
    },

    # --- DESAFIADOR (Castelo do Bowser) ---
    {
        "id": "CH-1", "level": "Desafiador",
        "prompt": "Qual o valor final de 'cont' se v={5, 9, 2, 8, 4} e o loop for: if(v[i]%2==0) cont++;",
        "options": ["2", "3", "5", "0"],
        "answer": "3",
        "rationale": {
            "3": "✅ Os números pares são 2, 8 e 4. O contador subiu 3 vezes.",
            "2": "❌ Você esqueceu de um número par."
        },
        "tip": "O operador %2==0 identifica números pares."
    },
    {
        "id": "CH-2", "level": "Desafiador",
        "prompt": "Se v={10, 20, 30} e fazemos: v[0] = v[2]; v[2] = v[0]; qual o estado final de v?",
        "options": ["{30, 20, 10}", "{30, 20, 30}", "{10, 20, 30}", "{30, 30, 30}"],
        "answer": "{30, 20, 30}",
        "rationale": {
            "{30, 20, 30}": "✅ Atenção! Na segunda linha, v[0] já vale 30. Para inverter, precisaríamos de uma variável 'aux'.",
            "{30, 20, 10}": "❌ Sem variável auxiliar, o valor original de v[0] (10) se perdeu."
        },
        "tip": "Lógica de troca (swap) exige uma terceira gaveta temporária."
    },
    {
        "id": "CH-3", "level": "Desafiador",
        "prompt": "Como imprimir o vetor de trás para frente?",
        "options": ["for(int i=v.length-1; i>=0; i--)", "for(int i=v.length; i>0; i--)", "for(int i=0; i<v.length; i--)", "v.reverse().print()"],
        "answer": "for(int i=v.length-1; i>=0; i--)",
        "rationale": {
            "for(int i=v.length-1; i>=0; i--)": "✅ Começa no último índice e vai subtraindo até chegar no 0.",
            "for(int i=v.length; i>0; i--)": "❌ Erro: v.length é um índice inválido."
        },
        "tip": "O decremento i-- é a chave aqui."
    },
    {
        "id": "CH-4", "level": "Desafiador",
        "prompt": "Qual o resultado de v[v[0]] se v={2, 1, 0}?",
        "options": ["0", "1", "2", "Erro"],
        "answer": "0",
        "rationale": {
            "0": "✅ v[0] é 2. Então v[v[0]] vira v[2]. O valor em v[2] é 0.",
            "2": "❌ v[0] é 2, mas você quer o conteúdo dessa posição."
        },
        "tip": "Resolva de dentro para fora: primeiro o índice interno[cite: 1]."
    },
    {
        "id": "CH-5", "level": "Desafiador",
        "prompt": "No exercício da Máquina de Bebidas, se o cliente digita '5' e o vetor tem 5 itens, por que usamos menu[opcao - 1]?",
        "options": ["Porque o array começa em 0", "Porque o item 5 é vazio", "Para arredondar o número", "É opcional"],
        "answer": "Porque o array começa em 0",
        "rationale": {
            "Porque o array começa em 0": "✅ Exato! O item 5 para o humano é o índice 4 para o Java[cite: 1].",
            "É opcional": "❌ Se não subtrair, dará erro de 'fora de limite'."
        },
        "tip": "Sempre mapeie a entrada do usuário para o índice real[cite: 1]."
    }
]

# =========================
# LÓGICA DO APP (Streamlit)
# =========================
def reset_all():
    order = list(range(len(QUESTIONS)))
    random.shuffle(order)
    st.session_state.q_order = order
    st.session_state.q_index = 0
    st.session_state.base_correct = 0
    st.session_state.final_points = 0
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    st.session_state.show_feedback = False
    st.session_state.last_choice = None
    st.session_state.last_q = None

if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "q_order" not in st.session_state:
    reset_all()

# UI Lateral
st.sidebar.image("https://img.icons8.com/color/512/super-mario.png", width=100)
st.sidebar.title("World Select")
if st.sidebar.button("Reiniciar Aventura"):
    reset_all()
    st.rerun()

# --- TELA DE LOGIN ---
if not st.session_state.student_name:
    st.subheader("🍄 Digite seu nome para começar a jornada!")
    nome = st.text_input("Player Name:", placeholder="Mario")
    if st.button("Press Start"):
        if len(nome.strip()) >= 3:
            st.session_state.student_name = nome.strip()
            reset_all()
            st.rerun()
        else:
            st.warning("O nome deve ter pelo menos 3 letras.")
else:
    # --- JOGO EM ANDAMENTO ---
    total = len(QUESTIONS)
    if st.session_state.q_index < total:
        qpos = st.session_state.q_order[st.session_state.q_index]
        q = QUESTIONS[qpos]
        
        # Header Status
        st.info(f"📍 {st.session_state.student_name} | Questão {st.session_state.q_index + 1}/{total} | 🔥 Streak: {st.session_state.streak}")
        
        # Difficulty Progress
        colors = {"Fácil": "green", "Médio": "orange", "Difícil": "red", "Desafiador": "purple"}
        st.markdown(f"**Dificuldade:** :{colors[q['level']]}[{q['level']}]")
        st.progress((st.session_state.q_index) / total)

        st.markdown(f"### {q['prompt']}")
        
        # Opções
        if not st.session_state.show_feedback:
            choice = st.radio("Selecione a resposta:", q["options"], key=f"q_{q['id']}")
            if st.button("Confirmar ✅"):
                st.session_state.last_choice = choice
                st.session_state.last_q = q
                st.session_state.show_feedback = True
                
                # Lógica de Pontos
                if choice == q["answer"]:
                    st.session_state.base_correct += 1
                    st.session_state.streak += 1
                    st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.streak)
                    bonus = max(0, st.session_state.streak - 1)
                    st.session_state.final_points += 10 + (bonus * 5) # 10 pontos base + bônus
                else:
                    st.session_state.streak = 0
                st.rerun()
        else:
            # Feedback
            q = st.session_state.last_q
            choice = st.session_state.last_choice
            
            if choice == q["answer"]:
                st.success(f"⭐ **HERE WE GO!** {q['rationale'][choice]}")
            else:
                st.error(f"🍄 **MAMMA MIA!** {q['rationale'][choice]}")
                st.warning(f"A resposta correta era: **{q['answer']}**")
            
            st.markdown(f"💡 **Dica do Toad:** {q['tip']}")
            
            if st.button("Próxima Fase ➡️"):
                st.session_state.q_index += 1
                st.session_state.show_feedback = False
                st.rerun()
    else:
        # --- FINAL ---
        st.balloons()
        st.success(f"🏆 PARABÉNS, {st.session_state.student_name.upper()}! VOCÊ RESGATOU A PRINCESA (E O CÓDIGO)!")
        col1, col2 = st.columns(2)
        col1.metric("Acertos", f"{st.session_state.base_correct}/{total}")
        col2.metric("Moedas (Pontos)", st.session_state.final_points)
        
        if st.button("Jogar Novamente 🔁"):
            reset_all()
            st.rerun()
