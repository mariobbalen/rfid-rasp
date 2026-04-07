from mfrc522 import SimpleMFRC522
import time
import os
from gpiozero import LED

red = LED(20)
green = LED(21)
reader = SimpleMFRC522()

tags_cadastradas = {"359927119411": "Mario", "77496997218": "Pablo"}
autorizados = ["359927119411"]
entraram = {}
nao_autorizados = {}
invasoes = 0           


def sem_acesso(tag_id):
    global nao_autorizados
    clear_console()
    nome = tags_cadastradas[tag_id]
    print(f"\nVocê não tem acesso a este projeto, {nome}")
    time.sleep(2)

    nao_autorizados[tag_id] = nao_autorizados.get(tag_id, 0) + 1

    red.on()
    time.sleep(5)
    red.off()


def sem_identificacao(tag_id):
    global invasoes
    clear_console()
    print("\nIdentificação não encontrada!")
    time.sleep(2)

    invasoes += 1

    for _ in range(10):
        red.on()
        time.sleep(0.3)
        red.off()
        time.sleep(0.3)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    while True:
        clear_console()

        print("Aguardando...")

        tag_id, text = reader.read()
        tag_id = str(tag_id)

        if tag_id not in tags_cadastradas:
            sem_identificacao(tag_id)
            continue

        if tag_id not in autorizados:
            sem_acesso(tag_id)
            continue

        nome = tags_cadastradas[tag_id]

        if tag_id not in entraram:
            entraram[tag_id] = {
                "tempo": 0,
                "entrada": None,
                "dentro": False
            }

        if not entraram[tag_id]["dentro"]:
            # ENTRANDO
            print(f"Bem-vindo, {nome}\n")
            entraram[tag_id]["entrada"] = time.perf_counter()
            entraram[tag_id]["dentro"] = True
        else:
            # SAINDO
            tempo = time.perf_counter() - entraram[tag_id]["entrada"]
            entraram[tag_id]["tempo"] += tempo
            entraram[tag_id]["dentro"] = False

            print(f"Saída registrada, {nome}\n")

        green.on()
        time.sleep(5)
        green.off()

except KeyboardInterrupt:
    print("\n\n===== RELATÓRIO =====\n")

    print("AUTORIZADOS:\n")
    for tag_id, dados in entraram.items():
        nome = tags_cadastradas[tag_id]

        tempo_total = dados["tempo"]

        # Se ainda estiver dentro, soma tempo atual
        if dados["dentro"]:
            tempo_total += time.perf_counter() - dados["entrada"]

        print(f"{nome} ({tag_id}) - {tempo_total:.2f} segundos")

    print("\nNÃO AUTORIZADOS:\n")
    for tag_id, tentativas in nao_autorizados.items():
        nome = tags_cadastradas.get(tag_id, "Desconhecido")
        print(f"{nome} ({tag_id}) - {tentativas} tentativa(s)")

    print("\nINVASÕES (IDs desconhecidos):")
    print(invasoes)
    print("\n")






























# from mfrc522 import SimpleMFRC522
# import time
# import os
# from gpiozero import LED

# red = LED(67)
# green = LED(69)
# reader = SimpleMFRC522()
# tags_cadastradas = {"359927119411": "Mario", "77496997218": "Pablo"}
# autorizados = ["359927119411"]
# entraram = {}
# nao_autorizados = []

# def sem_acesso():
#     print(f"\nVocê não tem acesso a este projeto, {tags_cadastradas[id]}")
#     time.sleep(3)
#     nao_autorizados.append(id)
#     for i in range(10):
#         red.on()
#         time.sleep(0.5)
#         red.off()
#         time.sleep(0.5)

# def sem_identificacao():
#     print("\nIdentificação não encontrada!")
#     time.sleep(3)
#     nao_autorizados.append(id)
#     red.on()
#     time.sleep(5)
#     red.off()

# def clear_console():
#     os.system('cls' if os.name == 'nt' else 'clear')

# try:
#     while True:
#         clear_console()

#         id, text = reader.read()

#         if id not in tags_cadastradas:
#             sem_identificacao()
#             continue
            
#         if not id in autorizados:
#             sem_acesso()
#             continue
        
#         start_time = time.perf_counter()

#         if id not in entraram:
#             print(f"Bem-vindo, {tags_cadastradas[id]}\n")
#             entraram[id] = {"tempo": 0}
#         else:
#             print(f"Bem-vindo de volta, {tags_cadastradas[id]}\n")

#         # LED VERDE
#         green.on()
#         time.sleep(5)
#         green.off()

#         time.sleep(5)
#         clear_console()

#         end_time = time.perf_counter()

#         tempo_atual = entraram[id]["tempo"]
#         entraram[id]["tempo"] = (end_time - start_time) + tempo_atual

# except KeyboardInterrupt:
#     print("AUTORIZADOS\n")
#     for key, value in entraram.items():
#         print(f"{key} - {value['tempo']:.2f}")
#     print("\nNAO AUTORIZADOS\n")
#     for item in nao_autorizados:
#         print(item)
#     print("\n")


