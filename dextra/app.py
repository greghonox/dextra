"""
@ GREGÓRIO HONORATO
PROGRAMA DESENVOLVIDO PARA DEXTRA 05/04/2017
"""
try: from flask import Flask, render_template, request
except: print("INSTALE O PACOTE Flask")

app = Flask(__name__)

#A seguir, apresentamos a lista de ingredientes disponíveis:
igredientes = {"Alface":0.4, "Bacon":2, "Hamburger de Carne":3, "Ovo":0.8,
               "Queijo":1.50}

"""
O valor de cada opção do cardápio é dado pela soma dos ingredientes que compõe o lanche.
Além destas opções, o cliente pode personalizar seu lanche e escolher os ingredientes que desejar.
Nesse caso, o preço do lanche também será calculado pela soma dos ingredientes.
"""

cardapio = {"X-Bacon": igredientes["Bacon"] + igredientes["Hamburger de Carne"] + igredientes["Ovo"],
            "X-Burge": igredientes["Hamburger de Carne"] + igredientes["Queijo"],
            "X-Egg": igredientes["Ovo"] + igredientes["Hamburger de Carne"] + igredientes["Queijo"],
            "X-Egg Bacon": igredientes["Ovo"] + igredientes["Bacon"] + igredientes["Queijo"]}

#CHAMA A PASTA TEMPLATES COM O INDEX.HTML
@app.route("/")
def carregar_pagina():
    return render_template("index.html", cardapio=cardapio,
                                         igredientes=igredientes), 200

@app.route("/resultado", methods=["POST"])
def resultado():
    ingredientes = 0.00
    ingr = []

    try: ingredientes += float(request.form.get("preco_Alface")) * float(request.form.get("qtde_Alface"))
    except: pass
    try: ingredientes += float(request.form.get("preco_Bacon")) * float(request.form.get("qtde_Bacon"))
    except: pass
    try: ingredientes += float(request.form.get("preco_Hamburger_de_Carne")) * float(request.form.get("qtde_Hamburger_de_Carne"))
    except: pass
    try: ingredientes += float(request.form.get("preco_Ovo")) * float(request.form.get("qtde_Ovo"))
    except: pass
    try: ingredientes += float(request.form.get("preco_Queijo")) * float(request.form.get("qtde_Queijo"))
    except: pass

    try: lanche = float(request.form.get("lanches"))
    except: lanche = None

    try: total = ingredientes + lanche
    except: total = "SELECIONE UM LANCHE!"

    ingr.append(True if(int(request.form.get("qtde_Alface")) > 0) else False)
    ingr.append(True if(int(request.form.get("qtde_Bacon")) > 0) else False)
    ingr.append(True if(int(request.form.get("qtde_Hamburger_de_Carne")) > 0) else False)
    ingr.append(True if(int(request.form.get("qtde_Ovo")) > 0) else False)
    ingr.append(True if(int(request.form.get("qtde_Queijo")) > 0) else False)
    """
      Light:
      Se o lanche tem alface e não tem bacon, ganha 10% de desconto.
    """
    if(ingr[0] == True and ingr[1] == False):
        total = round(total - (total * .1) ,2)
    """
        Muita carne:
        A cada 3 porções de carne o cliente só paga 2. Se o lanche tiver 6 porções, o cliente pagará 4. Assim por diante...
    """
    if(ingr[2] and int(request.form.get("qtde_Hamburger_de_Carne")) % 3 == 0):
        total = round(total - int(int(request.form.get("qtde_Hamburger_de_Carne")) / 3) * 3 ,2)

    """
        Muito queijo:
        A cada 3 porções de queijo o cliente só paga 2. Se o lanche tiver 6 porções, o cliente pagará 4. Assim por diante...
    """
    if(ingr[4] and int(request.form.get("qtde_Queijo")) % 3 == 0):
        queijo = int(request.form.get("qtde_Queijo"))
        print((queijo - ((queijo / 3)) * 1.5))
        total = round(total - ((queijo - (queijo / 3)) * 1.5), 2)

    total = 'R$ ' + str(total) if(total != 'SELECIONE UM LANCHE!') else total
    return render_template("resultado.html", total=total), 200

app.run(use_reloader=True, host='0.0.0.0')
