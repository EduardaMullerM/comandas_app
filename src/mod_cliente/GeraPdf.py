from fpdf import FPDF
from datetime import datetime
import requests
from settings import ENDPOINT_CLIENTE, HEADERS_API

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 5, 'Abc Bolinhas', 0, 1, 'C', 0)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def listaTodos(self):
        pdf = PDF(orientation="P", unit="mm", format="A4")  # L paisagem, P retrato
        pdf.set_author("Aluno")
        pdf.set_title('Clientes')
        pdf.alias_nb_pages()  # mostra o número da página no rodapé
        pdf.add_page()

        # mostra o cabeçalho
        pdf.set_font('helvetica', 'b', 12)
        pdf.cell(190, 5, 'Clientes', 0, 1, 'C', 0)
        pdf.set_font('helvetica', '', 6)
        pdf.cell(190, 4, "Emitido em: " + str(datetime.now()), 0, 1, 'R')
        pdf.ln(5)

        # monta tabela para mostrar os dados
        pdf.set_font('helvetica', 'B', 8)
        pdf.cell(10, 5, 'ID', 0, 0, 'L')
        pdf.cell(50, 5, 'Nome', 0, 0, 'L')
        pdf.cell(30, 5, 'CPF', 0, 0, 'L')
        pdf.cell(30, 5, 'Telefone', 0, 0, 'L')
        pdf.cell(20, 5, 'Compra Fiado', 0, 0, 'L')
        pdf.cell(20, 5, 'Dia Fiado', 0, 1, 'L')

        # busca na API e mostra todos os dados
        pdf.set_font('helvetica', '', 8)

        try:
            response = requests.get(ENDPOINT_CLIENTE, headers=HEADERS_API)
            result = response.json()
            if response.status_code != 200:
                error_message = result.get('error', 'Erro desconhecido na API')
                raise Exception(error_message)

            for row in result[0]:
                pdf.cell(10, 5, str(row['id_cliente']), 0, 0, 'L')
                pdf.cell(50, 5, row.get('nome', ''), 0, 0, 'L')
                pdf.cell(30, 5, row.get('cpf', ''), 0, 0, 'L')
                pdf.cell(30, 5, row.get('telefone', ''), 0, 0, 'L')
                pdf.cell(20, 5, str(row['compra_fiado']), 0, 0, 'L')
                pdf.cell(20, 5, row.get('dia_fiado', ''), 0, 1, 'L')

        except Exception as e:
            pdf.multi_cell(190, 5, 'ERRO: ' + str(e), 1, 'J', False)

        pdf.output("C:\\Users\\matheus.felipe\\source\\repos\\Teste\\pastelaria-frontend\\src\\pdfCliente.pdf")

# Exemplo de uso
pdf_generator = PDF()
pdf_generator.listaTodos()
