
from pegaDadosSheets import autentica
from relatorioDiario import geraRelatorioDiario
from relatorioAtualizado import geraRelatorioAtualizado
from enviaDadosSheets import excel_to_google_sheets
from datetime import datetime

def main():
    autentica()
    print("Autenticação feita com sucesso e relatorio_backup criado!")
    
    geraRelatorioDiario()
    hoje = datetime.today().date()
    hoje = (str(hoje))
    print("Filtro do relatorio do dia "+hoje +" feito!")
    geraRelatorioAtualizado()
    print("Base de dados do dia " + hoje + " está atualizado no excel!")
    excel_to_google_sheets()
    print("Base de dados do dia " + hoje + " está atualizado no google sheets!")

if __name__ == "__main__":
    main()




