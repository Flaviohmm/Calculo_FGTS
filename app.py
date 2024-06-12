from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def calcular_fgts(data_inicial, data_final, salario_bruto):
    try:
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        data_final = datetime.strptime(data_final, "%d/%m/%Y")
    except ValueError:
        return None
    

    # Calcula a diferença em meses
    diferenca_meses = (data_final.year - data_inicial.year) * 12 + data_final.month - data_inicial.month

    fgts_mensal = salario_bruto * 0.08
    saldo_fgts = fgts_mensal * diferenca_meses

    return saldo_fgts, fgts_mensal, diferenca_meses

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data_inicial = request.form.get('data_inicial')
        data_final = request.form.get('data_final')
        salario_bruto = request.form.get('salario_bruto', type=float)

        resultado = calcular_fgts(data_inicial, data_final, salario_bruto)
        
        if resultado:
            saldo_fgts, fgts_mensal, meses_trabalhados = resultado
            return render_template('resultado.html', saldo_fgts=saldo_fgts, fgts_mensal=fgts_mensal, meses_trabalhados=meses_trabalhados)
        else:
            error_message = "There was an error processing your request. Please check the dates format."
            return render_template('index.html', error=error_message)
        
    return render_template('index.html')

@app.route('/resultado')
def resultado():
    return render_template('resultado.html')

if __name__ == '__main__':
    app.run(debug=True)
