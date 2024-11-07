# Tentativa 0

#0.1 Entender um jogo IPD
#0.2 Montar um com estrategias normais
#0.3 Fazer com estrategias em dados 



# Estratégias em dados
strategies_data = {
    "tht": {
        "first_move": "cooperate",
        "response": {"cooperate": "cooperate", "defect": "defect"},
    },
    "allc": {
        "first_move": "cooperate",
        "response": {"cooperate": "cooperate", "defect": "cooperate"},
    },
    "alld": {
        "first_move": "defect",
        "response": {"cooperate": "defect", "defect": "defect"},
    },
    "rn": {
        "first_move": "random",
        "response": {"cooperate": "random", "defect": "random"},
    },
    "tht^-1": {
        "first_move": "defect",
        "response": {"cooperate": "defect", "defect": "cooperate"  } 
    },
    "grim": {
        "first_move": "cooperate",
        "response": {"cooperate": "cooperate", "defect": "defect"  },
        "status_angry": False
        } 
}


#Agente
import random
def agente(strategy_data, hist_op):
    # Decisão da primeira jogada
    if not hist_op:
        if strategy_data["first_move"] == "random":
            return random.choice(["cooperate", "defect"])
        return strategy_data["first_move"]
   
   #Status 
    if "status_angry" in strategy_data:
        if not strategy_data["status_angry"] and "defect" in hist_op:
            strategy_data["status_angry"] = True
        if strategy_data["status_angry"]:
            return "defect"

    # Decisão com base no histórico do oponente
    last_move_op = hist_op[-1]
    response_action = strategy_data["response"][last_move_op]
    if response_action == "random":
        return random.choice(["cooperate", "defect"])
    return response_action


#Jogo
def jogo(jogada_a, jogada_b):
    if jogada_a == "cooperate" and jogada_b == "cooperate":
        return (3, 3)  # Todos coperam
    elif jogada_a == "cooperate" and jogada_b == "defect":
        return (0, 5)  # A coopera, B trai
    elif jogada_a == "defect" and jogada_b == "cooperate":
        return (5, 0)  # A trai, B copera
    else:
        return (1, 1)  # Todos traem
    

#IPD
def simular_jogo(strategy_data_a, strategy_data_b, rounds=10):
    hist_a, hist_b = [], []  # Histórico de jogadas
    total_score_a, total_score_b = 0, 0  # Pontuações

    for _ in range(rounds):
        # Cada agente escolhe sua jogada com base nos dados da estratégia e no histórico do oponente
        jogada_a = agente(strategy_data_a, hist_b)
        jogada_b = agente(strategy_data_b, hist_a)
        
        # Pontuação da rodada
        score_a, score_b = jogo(jogada_a, jogada_b)
        total_score_a += score_a
        total_score_b += score_b
        
        # Atualiza o histórico
        hist_a.append(jogada_a)
        hist_b.append(jogada_b)
        
        # Cada jogada e pontuação da rodada
        print(f"Rodada: {jogada_a} vs {jogada_b} | Pontos: {score_a}-{score_b}")
    
    # Observar se funciona
    print(f"\nPontuação Final: Agente A: {total_score_a}, Agente B: {total_score_b}")
simular_jogo(strategies_data["grim"], strategies_data["tht^-1"], rounds=10)

#1.1 Criar um agente que possua uma função para escolha de estratégia
#1.2 Agente deve escolher a estrategias inicial aleatoriamente
#1.3 Durante o jogo deve selecionar as estrategias, sem restrição

def escolher_estrategia():
   return random.choice(list(strategies_data.keys()))

def agente(strategy_name, hist_op, current_strategy_data):
    if not current_strategy_data:
        strategy_name = escolher_estrategia()
        current_strategy_data = strategies_data[strategy_name].copy()
  
    if not hist_op:
        if current_strategy_data["first_move"] == "random":
            return random.choice(["cooperate", "defect"]), current_strategy_data
        return current_strategy_data["first_move"], current_strategy_data


    if "has_betrayed" in current_strategy_data:
        if not current_strategy_data["has_betrayed"] and "defect" in hist_op:
            current_strategy_data["has_betrayed"] = True
        if current_strategy_data["has_betrayed"]:
            return "defect", current_strategy_data

   
    last_move_op = hist_op[-1]
    response_action = current_strategy_data["response"][last_move_op]
    if response_action == "random":
        return random.choice(["cooperate", "defect"]), current_strategy_data
    return response_action, current_strategy_data
    
#2.1 Dicionaro com as informações para o agente 
#