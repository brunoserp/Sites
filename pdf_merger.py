import streamlit as st
import os
import PyPDF2
import re

# ________________________________________________________________________________________________________
# 1) Mesclar todas as páginas de todos os PDFs da pasta
def todo_pdf(pasta, nome_arquivo="/pdf_merged.pdf"):
    merger = PyPDF2.PdfMerger()
    for file in os.listdir(pasta):
        if file.endswith('.pdf'):
            merger.append(f"{pasta}/{file}")

    output_path = os.path.join(pasta, nome_arquivo)
    merger.write(output_path)
    merger.close()
    st.success(f"PDFs mesclados com sucesso em: {output_path}")

# 2) Mesclar ao menos 1 página de cada PDF da pasta
def mesclar_paginas(pasta, paginas, nome_arquivo="/pdf_merged.pdf"):
    paginas_indicadas = set()
    
    # Separa as páginas por vírgula e hífen
    for parte in paginas.split(','):
        if '-' in parte:
            inicio, fim = parte.split('-')
            paginas_indicadas.update(range(int(inicio), int(fim) + 1))
        else:
            paginas_indicadas.add(int(parte))

    merger = PyPDF2.PdfMerger()
    pdfs_com_problema = []
    problemas_resumidos = False
    
    for file in os.listdir(pasta):
        if file.endswith('.pdf'):
            caminho_pdf = os.path.join(pasta, file)
            leitor_pdf = PyPDF2.PdfReader(caminho_pdf)
            qtd_paginas = len(leitor_pdf.pages)

            # Verifica se as páginas indicadas estão dentro do alcance
            paginas_fora_do_alcance = [pag for pag in paginas_indicadas if pag > qtd_paginas]

            if paginas_fora_do_alcance:
                pdfs_com_problema.append((file, qtd_paginas, paginas_fora_do_alcance))

            # Filtra as páginas válidas para o PDF atual
            paginas_validas = [pag - 1 for pag in paginas_indicadas if pag <= qtd_paginas]
            if paginas_validas:
                merger.append(caminho_pdf, pages=paginas_validas)

            # Checa se já existem mais de 5 PDFs com problemas
            if len(pdfs_com_problema) > 5 and not problemas_resumidos:
                st.warning("Há mais de 5 PDFs sem a(s) página(s) indicada(s). Abaixo estão as informações dos primeiros 5:")
                problemas_resumidos = True

    if pdfs_com_problema:
        st.text('Os PDFs abaixo estão incompatíveis com as informações sinalizadas:')
        mensagem = ""
        for i, (pdf, qtd_paginas, paginas_fora_do_alcance) in enumerate(pdfs_com_problema):
            if i < 5:
                paginas_str = ', '.join(map(str, paginas_fora_do_alcance))
                mensagem += f"O PDF '{pdf}' não tem as páginas {paginas_str}. Ele vai até a página {qtd_paginas}.\n\n"
            else:
                break
        st.warning(mensagem)

    # Salva o PDF mesclado
    output_path = os.path.join(pasta, nome_arquivo)
    try:
        merger.write(output_path)
        st.success(f"PDFs mesclados com sucesso em: {output_path}")
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar o PDF: {e}")
    finally:
        merger.close()
# ________________________________________________________________________________________________________


# PROGRAMA PRINCIPAL
# ________________________________________________________________________________________________________

st.header("Mesclador de PDF", divider="gray")

st.html('''
    <h5>Instruções:</h5>
    Coloque todos os PDFs que você deseja mesclar numa pasta.<br>
    O programa irá acessar todos os arquivos dessa pasta e mesclar conforme o tipo de mesclagem escolhido.<br>
    Para isso, preencha os campos abaixo, e, ao final, clique no botão Mesclar para salvar o arquivo:
    ''')

opcoes = st.selectbox(
    label='Escolha um tipo de mesclagem:',
    options=['Juntar todas as páginas de todos os PDFs',
             'Juntar pelo menos uma página de todos os PDFs'],
    index=None,
    placeholder='None'
)

if opcoes == 'Juntar pelo menos uma página de todos os PDFs':
    st.html('''
        Indique as páginas a serem mescladas.<br>
            <p style="margin-left: 25px;">Caso queira uma única página, digite-a.<br>
            Caso queira uma sequência consecutiva de páginas, indique a primeira e última, separadas por um hífen. Ex. 4-8 (páginas 4 a 8) <br>
            Caso queira uma sequência não consecutiva de páginas, indique a primeira e última página da sequência separadas por hífen, e entre vírgulas se for uma página individual. Ex 4-8,10,12 (páginas 4 a 8, 10 e 12).
    ''')
    paginas = st.text_input("Páginas a serem mescladas: ")

folder_path = st.text_input("Insira o caminho da pasta com os PDFs:")

if st.button("Mesclar"):
    if folder_path and os.path.isdir(folder_path):
        if opcoes == 'Juntar todas as páginas de todos os PDFs':
            todo_pdf(folder_path)
        elif opcoes == 'Juntar pelo menos uma página de todos os PDFs':
            if not re.fullmatch(r'[0-9,-]+', paginas):
                st.write('A sequência de páginas que você informou não é compatível com as instruções. Reescreva-a corretamente.')
            else:
                mesclar_paginas(folder_path, paginas)
    else:
        st.write("Por favor, insira um caminho válido para a pasta.")


# streamlit run C:\Users\bserpellone\Desktop\Python\github\pdf_merger.py