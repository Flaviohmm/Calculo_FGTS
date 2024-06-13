from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def calcular_fgts(data_inicial, data_final, salario_bruto):
    try:
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        data_final = datetime.strptime(data_final, "%d/%m/%Y")
    except ValueError:
        return None
    

    # Cálcula a diferença em meses
    diferenca_meses = ((data_final.year - data_inicial.year) * 12 + data_final.month - data_inicial.month) + 1

    fgts_mensal = salario_bruto * 0.08
    saldo_fgts = fgts_mensal * diferenca_meses

    # Cálculo de juros (exemplo: 3% ao ano)
    taxa_juros_anual = 0.03
    juros = (saldo_fgts * taxa_juros_anual * diferenca_meses) / 12

    # Simulação de correção do saldo FGTS (exemplo: adicionar 2% por mês)
    taxa_correcao_mensal = 0.02
    saldo_fgts_corrigido = saldo_fgts + (saldo_fgts * taxa_correcao_mensal * diferenca_meses)

    # Cálculo da multa de 40% em caso de demissão sem justa causa
    multa_40 = saldo_fgts * 0.4

    # Total a receber com multa
    total_com_multa = saldo_fgts + multa_40

    return saldo_fgts, fgts_mensal, diferenca_meses, juros, saldo_fgts_corrigido, multa_40, total_com_multa

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data_inicial = request.form.get('data_inicial')
        data_final = request.form.get('data_final')
        salario_bruto = request.form.get('salario_bruto', type=float)

        resultado = calcular_fgts(data_inicial, data_final, salario_bruto)
        
        if resultado:
            saldo_fgts, fgts_mensal, diferenca_meses, juros, saldo_fgts_corrigido, multa_40, total_com_multa = resultado
            return render_template(
                'resultado.html', 
                data_inicial=data_inicial,
                data_final=data_final,
                meses_trabalhados=diferenca_meses,
                salario_bruto=salario_bruto,
                juros=juros,
                fgts_mensal=fgts_mensal, 
                saldo_fgts=saldo_fgts, 
                saldo_fgts_corrigido=saldo_fgts_corrigido,
                multa_40=multa_40,
                total_com_multa=total_com_multa
            )
        else:
            error_message = "There was an error processing your request. Please check the dates format."
            return render_template('index.html', error=error_message)
        
    return render_template('index.html')

@app.route('/resultado')
def resultado():
    data_inicial = request.form.get('data_inicial')
    data_final = request.form.get('data_final')
    salario_bruto = request.form.get('salario_bruto', type=float)

    resultado = calcular_fgts(data_inicial, data_final, salario_bruto)

    if resultado:
        saldo_fgts, fgts_mensal, diferenca_meses, juros, saldo_fgts_corrigido, multa_40, total_com_multa = resultado

        return render_template(
            'resultado.html', 
            data_inicial=data_inicial, 
            data_final=data_final,
            diferenca_meses=diferenca_meses,
            salario_bruto=salario_bruto,
            fgts_mensal=fgts_mensal,
            saldo_fgts=saldo_fgts,
            juros=juros,
            saldo_fgts_corrigido=saldo_fgts_corrigido,
            multa_40=multa_40,
            total_com_multa=total_com_multa
        )
    else:
        error_message = "There was an error processing your request. Please check the dates format."
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
