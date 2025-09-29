from src import app
from src.services.tempo_services import obter_cidades, obter_previsao_tempo, obter_estados, converter_data_para_dia
from flask import jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()


API_KEY = os.getenv("key")

@app.route("/estados", methods=["GET"])
def pg_clima():
    estados = obter_estados()
    return jsonify(estados)

@app.route('/cidades/<uf>')
def api_cidades():
    cidades = obter_cidades()
    return jsonify(cidades)

@app.route("/previsao", methods=["POST"])
def previsao():
    estado = request.form["estado"]
    cidade = request.form["cidade"]
    print(estado, cidade)
    dados = obter_previsao_tempo(cidade, estado, API_KEY)
    
    if dados.get("cod") != "200":
        print("Erro na resposta da API:", dados)
        return "Erro ao obter dados. Verifique cidade e estado."

    dias = {}
    for item in dados["list"]:
        data = item["dt_txt"].split()[0]
        if data not in dias:
            dias[data] = []
        dias[data].append(item)

    previsoes = []
    for dia, entradas in dias.items():
        dia_semana = converter_data_para_dia(dia)
        temp_min = min(e["main"]["temp_min"] for e in entradas)
        temp_max = max(e["main"]["temp_max"] for e in entradas)
        umidade = entradas[0]["main"]["humidity"]
        clima = entradas[0]["weather"][0]["description"]
        vento = entradas[0]["wind"]["speed"]
        chuva = entradas[0].get("rain", {}).get("3h", 0.0)
        
        previsoes.append({
            "data": dia,
            "dia_semana": dia_semana,
            "temp_min": round(temp_min, 1),
            "temp_max": round(temp_max, 1),
            "umidade": umidade,
            "clima": clima.capitalize(),
            "vento": vento,
            "chuva": chuva
        })
  
    return jsonify(dados)
    