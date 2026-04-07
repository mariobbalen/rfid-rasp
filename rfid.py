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
    print(f"Você não tem acesso a este projeto, {nome}")
    time.sleep(2)

    nao_autorizados[tag_id] = nao_autorizados.get(tag_id, 0) + 1

    red.on()
    time.sleep(5)
    red.off()


def sem_identificacao(tag_id):
    global invasoes
    clear_console()
    print("Identificação não encontrada!")
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

        clear_console()
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