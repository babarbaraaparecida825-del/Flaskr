from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request

bp = Blueprint("calculos", __name__)


def calcular_irpf(salario_bruto):
    """Calcula a alíquota e o desconto estimado do IRPF com base na tabela progressiva."""
    if salario_bruto <= 2259.20:
        aliquota = 0.0
        parcela_deduzir = 0.0
    elif salario_bruto <= 2826.65:
        aliquota = 7.5
        parcela_deduzir = 169.44
    elif salario_bruto <= 3751.05:
        aliquota = 15.0
        parcela_deduzir = 381.44
    elif salario_bruto <= 4664.68:
        aliquota = 22.5
        parcela_deduzir = 662.77
    else:
        aliquota = 27.5
        parcela_deduzir = 896.00

    desconto = max(0.0, (salario_bruto * (aliquota / 100)) - parcela_deduzir)
    salario_liquido = salario_bruto - desconto

    return {
        "salario_bruto": salario_bruto,
        "aliquota": aliquota,
        "desconto": round(desconto, 2),
        "salario_liquido": round(salario_liquido, 2),
    }


def calcular_decimo_terceiro(salario_base, meses_trabalhados):
    """Calcula o valor proporcional aproximado do 13º salário na rescisão."""
    valor_proporcional = (salario_base / 12) * meses_trabalhados

    return {
        "salario_base": salario_base,
        "meses_trabalhados": meses_trabalhados,
        "valor_proporcional": round(valor_proporcional, 2),
    }


@bp.route("/painel", methods=("GET", "POST"))
def painel():
    """Exibe e processa as calculadoras financeiras na memória."""
    resultado_irpf = None
    resultado_rescisao = None

    if request.method == "POST":
        tipo_calculo = request.form.get("tipo_calculo")

        if tipo_calculo == "irpf":
            try:
                salario_bruto = float(request.form.get("salario_bruto", "").replace(",", "."))
                if salario_bruto < 0:
                    flash("O salário bruto não pode ser negativo.")
                else:
                    resultado_irpf = calcular_irpf(salario_bruto)
            except ValueError:
                flash("Informe um valor numérico válido para o salário bruto.")

        elif tipo_calculo == "rescisao":
            try:
                salario_base = float(request.form.get("salario_base", "").replace(",", "."))
                meses_trabalhados = int(request.form.get("meses_trabalhados", ""))

                if salario_base < 0:
                    flash("O salário base não pode ser negativo.")
                elif meses_trabalhados < 1 or meses_trabalhados > 12:
                    flash("Os meses trabalhados devem estar entre 1 e 12.")
                else:
                    resultado_rescisao = calcular_decimo_terceiro(
                        salario_base, meses_trabalhados
                    )
            except ValueError:
                flash("Informe valores numéricos válidos para o cálculo de rescisão.")

    return render_template(
        "calculos/index.html",
        resultado_irpf=resultado_irpf,
        resultado_rescisao=resultado_rescisao,
    )