import requests

enumProcesso = 0
enumStatus = {
    "importando": 4,
    "ligado": 2,
    "desligado": 3,
    "erro": 1,
    "sem arquivos para integrar": 8
}

def putRequestFunction(status, enumBanco):
    horaFeita = f'http://172.16.10.6:8443/acompanhamentoTotal/horaFeita/{enumProcesso}/{enumBanco}'
    URLnovaApi = f'http://172.16.10.6:8443/acompanhamentoTotal/processoAndBancoStatus/{enumProcesso}/{enumBanco}'

    data = { "status": enumStatus[status] }
    headers = { "Content-Type": "application/json" }
    
    response = requests.put(URLnovaApi, headers=headers, json=data)
    requests.put(horaFeita)

    if response.status_code == 200:
        print("Requisição PUT bem-sucedida!")
        print("Resposta:", response.json())
    else:
        print(f"Falha na requisição PUT. Código de status: {response.status_code}")
        print("Resposta:", response.text)
