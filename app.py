QUESTIONS = [
    # ============================================================
    # MUNDO 1-1: PLANÍCIE DOS ÍNDICES (FÁCIL)
    # ============================================================
    {
        "id": "M1-1", "level": "Fácil",
        "prompt": "Qual o valor padrão de um elemento em 'int[] v = new int[5];'?",
        "options": ["null", "0", "1", "Lixo de memória"], "answer": "0",
        "rationale": {
            "null": "❌ Errado. 'null' é para objetos; tipos primitivos numéricos iniciam com zero.",
            "0": "✅ Wahoo! Java inicializa vetores numéricos primitivos com zero automaticamente.",
            "1": "❌ Errado. Java não assume 1 como valor inicial.",
            "Lixo de memória": "❌ Errado. Ao contrário de C++, o Java limpa a memória e atribui valores padrão."
        },
        "tip": "Pense no armário da aula: ele já vem com 'zero' moedas em cada gaveta[cite: 1]."
    },
    {
        "id": "M1-2", "level": "Fácil",
        "prompt": "O que define um vetor como 'homogêneo'?",
        "options": ["Tamanho fixo", "Mesma cor de gaveta", "Elementos do mesmo tipo", "Armazenamento em disco"],
        "answer": "Elementos do mesmo tipo",
        "rationale": {
            "Tamanho fixo": "❌ Isso é uma característica (estático), mas não define a homogeneidade.",
            "Mesma cor de gaveta": "❌ Metáfora visual, não técnica.",
            "Elementos do mesmo tipo": "✅ Isso mesmo! Todas as gavetas guardam o mesmo tipo de dado[cite: 1].",
            "Armazenamento em disco": "❌ Vetores residem na memória RAM (Heap)."
        },
        "tip": "Se o armário é de 'double', só entra 'double'[cite: 1]."
    },
    {
        "id": "M1-3", "level": "Fácil",
        "prompt": "Qual a sintaxe correta para declarar e instanciar um vetor de Strings?",
        "options": ["String v = new String[5];", "String[] v = new String[5];", "array v = new String[5];", "v[] = new String;"],
        "answer": "String[] v = new String[5];",
        "rationale": {
            "String v = new String[5];": "❌ Falta o '[]' no tipo para indicar que é um vetor.",
            "String[] v = new String[5];": "✅ Perfeito! Tipo[] nome = new Tipo[tamanho][cite: 1].",
            "array v = new String[5];": "❌ 'array' não é uma palavra reservada em Java.",
            "v[] = new String;": "❌ Sintaxe completamente inválida."
        },
        "tip": "O símbolo '[]' é a marca registrada do vetor em Java[cite: 1]."
    },
    {
        "id": "M1-4", "level": "Fácil",
        "prompt": "Em um vetor de tamanho N, qual o índice do primeiro e do último elemento?",
        "options": ["1 e N", "0 e N", "0 e N-1", "1 e N-1"],
        "answer": "0 e N-1",
        "rationale": {
            "1 e N": "❌ Errado. Java usa 'Zero-based indexing'[cite: 1].",
            "0 e N": "❌ Errado. O índice N está fora dos limites.",
            "0 e N-1": "✅ Wahoo! Começamos no 0 e terminamos no total menos 1[cite: 1].",
            "1 e N-1": "❌ Errado. Começar no 1 faria você perder a primeira gaveta."
        },
        "tip": "Sempre subtraia 1 do total para achar a última posição[cite: 1]."
    },
    {
        "id": "M1-5", "level": "Fácil",
        "prompt": "O atributo '.length' retorna:",
        "options": ["O maior valor do vetor", "O índice do último elemento", "A quantidade total de gavetas", "O espaço livre"],
        "answer": "A quantidade total de gavetas",
        "rationale": {
            "O maior valor do vetor": "❌ Errado. O length mede tamanho, não conteúdo.",
            "O índice do último elemento": "❌ Quase. O último índice é length-1.",
            "A quantidade total de gavetas": "✅ Isso! Ele informa a capacidade total definida na criação[cite: 1].",
            "O espaço livre": "❌ Vetores não rastreiam 'espaço livre' automaticamente."
        },
        "tip": "Dica do Toad: Length é o tamanho total do seu armário[cite: 1]."
    },
    {
        "id": "M1-6", "level": "Fácil",
        "prompt": "Onde um vetor é armazenado fisicamente na memória Java?",
        "options": ["Stack (Pilha)", "Heap", "CPU Cache", "Disco Rígido"],
        "answer": "Heap",
        "rationale": {
            "Stack (Pilha)": "❌ Na pilha ficam apenas as referências (o nome da variável).",
            "Heap": "✅ Correto! Todos os objetos e vetores residem no Heap (Memória Dinâmica).",
            "CPU Cache": "❌ Nível muito baixo para gerenciamento de objetos Java.",
            "Disco Rígido": "❌ Muito lento. Vetores são estruturas de memória volátil."
        },
        "tip": "A variável é o endereço, mas o armário real fica no Heap."
    },
    {
        "id": "M1-7", "level": "Fácil",
        "prompt": "int[] v = {2, 4, 6}; Qual o valor de v[2]?",
        "options": ["2", "4", "6", "Erro"],
        "answer": "6",
        "rationale": {
            "2": "❌ Este é o v[0].",
            "4": "❌ Este é o v[1].",
            "6": "✅ Exato! O terceiro elemento está na posição 2[cite: 1].",
            "Erro": "❌ O código é válido e o índice está dentro do limite."
        },
        "tip": "Conte: 0, 1, 2... O terceiro dedo é o índice 2[cite: 1]."
    },

    # ============================================================
    # MUNDO 2-4: DESERTO DAS ITERAÇÕES (MÉDIO)
    # ============================================================
    {
        "id": "M2-1", "level": "Médio",
        "prompt": "Qual cabeçalho de loop causa 'ArrayIndexOutOfBoundsException'?",
        "options": ["i < v.length", "i <= v.length", "i == 0", "i--"],
        "answer": "i <= v.length",
        "rationale": {
            "i < v.length": "❌ Este é o correto e seguro.",
            "i <= v.length": "✅ Mamma Mia! O '=' faz o loop tentar acessar uma posição que não existe no final[cite: 1].",
            "i == 0": "❌ Condição de parada inválida para um loop comum.",
            "i--": "❌ Este é o decremento, não a condição."
        },
        "tip": "Nunca use '=' junto com length em loops de vetor[cite: 1]."
    },
    {
        "id": "M2-2", "level": "Médio",
        "prompt": "No loop 'for (int x : v)', a variável 'x' representa:",
        "options": ["O índice atual", "O endereço de memória", "O conteúdo da posição", "O tamanho do vetor"],
        "answer": "O conteúdo da posição",
        "rationale": {
            "O índice atual": "❌ Errado. O for-each 'esconde' o índice.",
            "O endereço de memória": "❌ Java esconde endereços de memória do programador.",
            "O conteúdo da posição": "✅ Wahoo! O for-each extrai o valor de cada gaveta diretamente[cite: 1].",
            "O tamanho do vetor": "❌ Este seria o .length."
        },
        "tip": "Use o for-each para ler o 'Boletim' sem se preocupar com números de gaveta[cite: 1]."
    },
    {
        "id": "M2-3", "level": "Médio",
        "prompt": "Para somar valores de um vetor, a variável acumuladora deve iniciar em:",
        "options": ["1", "null", "0", "O tamanho do vetor"],
        "answer": "0",
        "rationale": {
            "1": "❌ Errado. Se começar em 1, o resultado final terá 1 a mais do que a soma real.",
            "null": "❌ Primitivos não aceitam null.",
            "0": "✅ Correto! O elemento neutro da soma é zero[cite: 1].",
            "O tamanho do vetor": "❌ Errado. Isso não faz sentido matemático para soma de notas."
        },
        "tip": "Limpe o balde (zero) antes de começar a enchê-lo com moedas[cite: 1]."
    },
    {
        "id": "M2-4", "level": "Médio",
        "prompt": "Como acessar a média do aluno no índice 'i' em vetores paralelos?",
        "options": ["notas[i]", "notas[nomes[i]]", "notas.get(i)", "notas[media]"],
        "answer": "notas[i]",
        "rationale": {
            "notas[i]": "✅ Isso! Vetores paralelos compartilham o mesmo apontador (índice)[cite: 1].",
            "notas[nomes[i]]": "❌ Errado. Não se pode usar String como índice de vetor.",
            "notas.get(i)": "❌ .get() é para ArrayList, não para vetores nativos.",
            "notas[media]": "❌ 'media' não foi definida como índice numérico."
        },
        "tip": "Se a Ana está na gaveta 3 de nomes, a nota dela está na gaveta 3 de notas[cite: 1]."
    },
    {
        "id": "M2-5", "level": "Médio",
        "prompt": "O que o código 'v[i] = v[i] * 2;' faz dentro de um loop?",
        "options": ["Duplica o tamanho do vetor", "Dobra o valor de cada elemento", "Apaga o vetor", "Cria um novo vetor"],
        "answer": "Dobra o valor de cada elemento",
        "rationale": {
            "Duplica o tamanho do vetor": "❌ Vetores têm tamanho estático. O length não muda.",
            "Dobra o valor de cada elemento": "✅ Correto! Você acessa o conteúdo, multiplica e guarda de volta na mesma gaveta[cite: 1].",
            "Apaga o vetor": "❌ Pelo contrário, você está preenchendo com novos dados.",
            "Cria um novo vetor": "❌ Não houve uso da palavra reservada 'new'."
        },
        "tip": "É como se o Mario pegasse um item, usasse um cogumelo para dobrá-lo e o devolvesse para a caixa[cite: 1]."
    },
    {
        "id": "M2-6", "level": "Médio",
        "prompt": "Qual a principal desvantagem do loop 'for-each'?",
        "options": ["É mais lento", "Não permite alterar valores no vetor", "Só funciona com inteiros", "Não compila no Java moderno"],
        "answer": "Não permite alterar valores no vetor",
        "rationale": {
            "É mais lento": "❌ Errado. A performance é praticamente idêntica.",
            "Não permite alterar valores no vetor": "✅ Exato! Ele fornece apenas uma cópia do valor para leitura[cite: 1].",
            "Só funciona com inteiros": "❌ Funciona com qualquer tipo de dado.",
            "Não compila no Java moderno": "❌ É uma ferramenta padrão desde o Java 5."
        },
        "tip": "Se você quer mudar as notas dos alunos, use o 'for' tradicional com índice[cite: 1]."
    },
    {
        "id": "M2-7", "level": "Médio",
        "prompt": "Para percorrer apenas a metade do vetor, a condição do 'for' deve ser:",
        "options": ["i < v.length / 2", "i < v.length", "i < 2", "i = 5"],
        "answer": "i < v.length / 2",
        "rationale": {
            "i < v.length / 2": "✅ Wahoo! Você limita o percurso ao meio do caminho[cite: 1].",
            "i < v.length": "❌ Isso percorreria o vetor inteiro.",
            "i < 2": "❌ Isso percorreria apenas os dois primeiros itens.",
            "i = 5": "❌ Isso é uma atribuição, não uma comparação."
        },
        "tip": "Aritmética básica no controle do loop resolve o mistério[cite: 1]."
    },

    # ============================================================
    # MUNDO 7-3: MAR DE REFERÊNCIAS (DIFÍCIL)
    # ============================================================
    {
        "id": "M7-1", "level": "Difícil",
        "prompt": "Se 'b = a;', e mudamos 'b[0] = 99;', o que acontece com 'a[0]'?",
        "options": ["Permanece igual", "Também muda para 99", "Torna-se null", "Lança um erro"],
        "answer": "Também muda para 99",
        "rationale": {
            "Permanece igual": "❌ Errado. 'b = a' não cria um novo vetor, apenas aponta para o mesmo.",
            "Também muda para 99": "✅ Mamma Mia! Eles compartilham o mesmo endereço na memória Heap.",
            "Torna-se null": "❌ Não houve comando de limpeza.",
            "Lança um erro": "❌ Operação perfeitamente válida."
        },
        "tip": "Em Java, atribuir um vetor a outro é como dar dois nomes diferentes para a mesma casa."
    },
    {
        "id": "M7-2", "level": "Difícil",
        "prompt": "Qual método cria uma cópia real e independente de um vetor?",
        "options": ["v.copy()", "v.clone()", "v = b", "v.duplicate()"],
        "answer": "v.clone()",
        "rationale": {
            "v.copy()": "❌ Não existe método .copy() nativo para arrays em Java.",
            "v.clone()": "✅ Isso! O clone aloca um novo espaço na memória com os mesmos valores.",
            "v = b": "❌ Isso apenas copia a referência, não os dados.",
            "v.duplicate()": "❌ Não é um método padrão do Java."
        },
        "tip": "Para ter seu próprio armário igual ao do Mario, você precisa de um clone."
    },
    {
        "id": "M7-3", "level": "Difícil",
        "prompt": "Como encontrar o menor valor em um vetor durante um loop?",
        "options": ["if (v[i] > menor)", "if (v[i] < menor)", "menor = v.length", "menor = 0"],
        "answer": "if (v[i] < menor)",
        "rationale": {
            "if (v[i] > menor)": "❌ Isso acharia o maior valor.",
            "if (v[i] < menor)": "✅ Correto! Se o valor atual é menor que o guardado, atualizamos o recorde[cite: 1].",
            "menor = v.length": "❌ Isso apenas guarda o tamanho do vetor.",
            "menor = 0": "❌ Se houver apenas números positivos, 0 sempre será o menor, mesmo se não estiver no vetor."
        },
        "tip": "O menor valor é aquele que 'perde' na comparação de magnitude[cite: 1]."
    },
    {
        "id": "M7-4", "level": "Difícil",
        "prompt": "Em vetores de objetos (ex: String[]), as gavetas vazias contêm:",
        "options": ["Espaço vazio \"\"", "O número 0", "null", "Erro de compilação"],
        "answer": "null",
        "rationale": {
            "Espaço vazio \"\"": "❌ Errado. Isso é uma String instanciada, mas vazia.",
            "O número 0": "❌ Errado. 0 é para tipos numéricos primitivos.",
            "null": "✅ Exato! Objetos não inicializados apontam para o 'nada' (null).",
            "Erro de compilação": "❌ A declaração é válida; o erro só ocorreria ao tentar usar o null."
        },
        "tip": "Null significa que a gaveta está lá, mas não tem nada dentro ainda."
    },
    {
        "id": "M7-5", "level": "Difícil",
        "prompt": "A busca linear em um vetor de tamanho 1000 faz, no pior caso:",
        "options": ["1 comparação", "500 comparações", "1000 comparações", "Nenhuma"],
        "answer": "1000 comparações",
        "rationale": {
            "1 comparação": "❌ Este seria o melhor caso (achar de primeira).",
            "500 comparações": "❌ Este seria o caso médio aproximado.",
            "1000 comparações": "✅ Correto! Se o item for o último ou não existir, você olhará todas as gavetas.",
            "Nenhuma": "❌ Impossível achar sem olhar."
        },
        "tip": "No pior cenário, o Bowser escondeu a chave na última gaveta possível."
    },
    {
        "id": "M7-6", "level": "Difícil",
        "prompt": "Para que serve o método 'Arrays.sort(v);'?",
        "options": ["Embaralhar moedas", "Somar valores", "Ordenar os elementos", "Excluir o vetor"],
        "answer": "Ordenar os elementos",
        "rationale": {
            "Embaralhar moedas": "❌ Errado. O sort organiza, não bagunça.",
            "Somar valores": "❌ Para somar usamos loops ou Streams.",
            "Ordenar os elementos": "✅ Isso! Coloca os valores em ordem crescente (numérica ou alfabética).",
            "Excluir o vetor": "❌ Java usa o Garbage Collector para excluir o que não é usado."
        },
        "tip": "Sort em inglês significa classificar ou ordenar."
    },
    {
        "id": "M7-7", "level": "Difícil",
        "prompt": "Vetores passados como parâmetros para métodos em Java são:",
        "options": ["Copiados integralmente", "Passados por referência", "Ignorados pelo compilador", "Convertidos em texto"],
        "answer": "Passados por referência",
        "rationale": {
            "Copiados integralmente": "❌ Errado. Isso seria muito lento para vetores grandes.",
            "Passados por referência": "✅ Correto! O método recebe o endereço do armário e pode alterar o original.",
            "Ignorados pelo compilador": "❌ Errado. São fundamentais na programação modular.",
            "Convertidos em texto": "❌ Somente se você chamar explicitamente o .toString()."
        },
        "tip": "Se você emprestar a chave do seu armário (referência), a pessoa pode mudar o que está lá dentro."
    },

    # ============================================================
    # BOWSER'S CASTLE: O CAOS DA MEMÓRIA (DESAFIADOR)
    # ============================================================
    {
        "id": "CH-1", "level": "Desafiador",
        "prompt": "O que lança uma 'NegativeArraySizeException'?",
        "options": ["Acessar índice -1", "Criar 'new int[-10]'", "Somar números negativos", "Diminuir o length"],
        "answer": "Criar 'new int[-10]'",
        "rationale": {
            "Acessar índice -1": "❌ Isso lança ArrayIndexOutOfBoundsException.",
            "Criar 'new int[-10]'": "✅ Bingo! Você não pode construir um armário com um número negativo de gavetas.",
            "Somar números negativos": "❌ Operação matemática normal.",
            "Diminuir o length": "❌ O length não pode ser diminuído após a criação."
        },
        "tip": "Você já viu um armário com -5 gavetas? O Java também não."
    },
    {
        "id": "CH-2", "level": "Desafiador",
        "prompt": "Como realizar o 'swap' (troca) entre v[0] e v[1]?",
        "options": ["v[0]=v[1]; v[1]=v[0];", "int aux=v[0]; v[0]=v[1]; v[1]=aux;", "v[0] <-> v[1]", "swap(v)"],
        "answer": "int aux=v[0]; v[0]=v[1]; v[1]=aux;",
        "rationale": {
            "v[0]=v[1]; v[1]=v[0];": "❌ Errado. O valor de v[0] seria perdido na primeira linha.",
            "int aux=v[0]; v[0]=v[1]; v[1]=aux;": "✅ Isso! A variável 'aux' segura o valor para não o perdermos[cite: 1].",
            "v[0] <-> v[1]": "❌ Sintaxe inexistente em Java.",
            "swap(v)": "❌ Não existe método nativo 'swap' para vetores básicos."
        },
        "tip": "Pense no Mario segurando um item enquanto troca os outros dois de lugar[cite: 1]."
    },
    {
        "id": "CH-3", "level": "Desafiador",
        "prompt": "Uma matriz em Java ('int[][] m') é tecnicamente:",
        "options": ["Um cubo de dados", "Um vetor de vetores", "Uma String muito longa", "Um arquivo Excel"],
        "answer": "Um vetor de vetores",
        "rationale": {
            "Um cubo de dados": "❌ Isso seria tridimensional (int[][][]).",
            "Um vetor de vetores": "✅ Exato! Cada linha da matriz é um vetor independente guardado em outro vetor.",
            "Uma String muito longa": "❌ Tipos incompatíveis.",
            "Um arquivo Excel": "❌ Excel é um software, não uma estrutura de memória Java."
        },
        "tip": "É um armário onde cada gaveta contém... outro armário menor!"
    },
    {
        "id": "CH-4", "level": "Desafiador",
        "prompt": "Qual o resultado de 'v[v.length]'?",
        "options": ["O último valor", "O tamanho", "ArrayIndexOutOfBoundsException", "0"],
        "answer": "ArrayIndexOutOfBoundsException",
        "rationale": {
            "O último valor": "❌ Este seria v[length-1].",
            "O tamanho": "❌ Este seria v.length (sem colchetes).",
            "ArrayIndexOutOfBoundsException": "✅ Correto! O índice igual ao length sempre estará fora do limite[cite: 1].",
            "0": "❌ Errado. O Java nem chega a olhar o valor, ele trava antes."
        },
        "tip": "O length é a placa da porta, mas não há gaveta com esse número[cite: 1]."
    },
    {
        "id": "CH-5", "level": "Desafiador",
        "prompt": "Qual a complexidade de tempo (O) para acessar v[500] sabendo o índice?",
        "options": ["O(n)", "O(1)", "O(log n)", "O(n^2)"],
        "answer": "O(1)",
        "rationale": {
            "O(n)": "❌ Errado. Isso seria se tivéssemos que procurar o valor.",
            "O(1)": "✅ Exato! O acesso via índice é direto e instantâneo (tempo constante).",
            "O(log n)": "❌ Errado. Isso seria para buscas binárias em dados ordenados.",
            "O(n^2)": "❌ Errado. Isso seria para loops aninhados."
        },
        "tip": "Ir direto para a gaveta 500 é muito mais rápido do que olhar uma por uma."
    },
    {
        "id": "CH-6", "level": "Desafiador",
        "prompt": "O que acontece se você tentar redimensionar um vetor nativo?",
        "options": ["v.resize(20)", "Não é possível (tamanho é fixo)", "O Java faz sozinho", "O length diminui"],
        "answer": "Não é possível (tamanho é fixo)",
        "rationale": {
            "v.resize(20)": "❌ Não existe este método em vetores Java.",
            "Não é possível (tamanho é fixo)": "✅ Correto! Vetores têm tamanho estático definido na criação[cite: 1].",
            "O Java faz sozinho": "❌ Somente em classes como ArrayList.",
            "O length diminui": "❌ Length é imutável após a criação."
        },
        "tip": "Se o armário ficou pequeno, o Mario precisa comprar um armário novo e mudar as coisas para lá[cite: 1]."
    },
    {
        "id": "CH-7", "level": "Desafiador",
        "prompt": "int[] x = {1, 2, 3}; Qual o valor de 'x[x[x[0]]]'?",
        "options": ["1", "2", "3", "Erro de compilação"],
        "answer": "3",
        "rationale": {
            "1": "❌ Este é o x[0].",
            "2": "❌ Este é o x[x[0]].",
            "3": "✅ Gênio! x[0]=1 -> x[1]=2 -> x[2]=3. Você seguiu as pistas corretamente![cite: 1].",
            "Erro de compilação": "❌ O código é lógico e perfeitamente válido."
        },
        "tip": "Resolva como uma boneca russa: abra a de dentro primeiro[cite: 1]."
    }
]
