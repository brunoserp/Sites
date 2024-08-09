import streamlit as st
import os
import PyPDF2
import re

# ___________________________________________________________________________________________________________________________________
# Funções para mesclagem de PDFs
# ___________________________________________________________________________________________________________________________________
def todo_pdf(pasta, nome_arquivo="pdf_merged.pdf"):
    merger = PyPDF2.PdfMerger()
    for file in os.listdir(pasta):
        if file.endswith('.pdf'):
            caminho_pdf = os.path.join(pasta, file)
            merger.append(caminho_pdf)

    output_path = os.path.join(pasta, nome_arquivo)
    
    try:
        merger.write(output_path)
        st.markdown(f'''
            <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
                <p style="font-size: 16px; color: green; font-weight: bold;">PDFs mesclados salvos com sucesso em:<br>{output_path}</p>
            </div>
        ''', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar o PDF: {e}")
    finally:
        merger.close()

def mesclar_paginas(pasta, paginas, nome_arquivo="pdf_merged.pdf"):
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
                for pagina in paginas_validas:
                    merger.append(caminho_pdf, pages=(pagina, pagina + 1))

            # Checa se já existem mais de 5 PDFs com problemas
            if len(pdfs_com_problema) > 5 and not problemas_resumidos:
                st.warning("Há mais de 5 PDFs sem a(s) página(s) indicada(s). Abaixo estão as informações dos primeiros 5:")
                problemas_resumidos = True

    if pdfs_com_problema:
        st.markdown('''
            <div style="background-color: #ffeb3b; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <div style="display: flex; justify-content: flex-start; align-items: flex-start;">
                    <p style="font-size: 16px; color: #333; font-weight: bold; text-align: left;">
                        Os PDFs abaixo estão incompatíveis com as informações sinalizadas:<br>
                        ''' + "<br>".join(f"O PDF '{pdf}' não tem as páginas {', '.join(map(str, paginas_fora_do_alcance))}. Ele vai até a página {qtd_paginas}." for pdf, qtd_paginas, paginas_fora_do_alcance in pdfs_com_problema[:5]) + '''
                    </p>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        st.warning("O PDF mesclado será salvo sem as páginas inexistentes indicadas acima.")
    
    # Salva o PDF mesclado
    output_path = os.path.join(pasta, nome_arquivo)
    try:
        merger.write(output_path)
        st.markdown(f'''
            <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
                <p style="font-size: 16px; color: green; font-weight: bold;">PDFs mesclados salvos com sucesso em:<br>{output_path}</p>
            </div>
        ''', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar o PDF: {e}")
    finally:
        merger.close()


# ___________________________________________________________________________________________________________________________________
# PROGRAMA PRINCIPAL
# ___________________________________________________________________________________________________________________________________

st.markdown(
    """
    <style>
    .footer {
        text-align: left;
        font-size: 12px;
        margin: 10px 0;
    }
    </style>
    <div class="footer">
        Feito por <a href='https://www.linkedin.com/in/brunoserp/' target='_blank'>Bruno Serpellone</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('''
    <style>
    h2 {
        margin: 0px;
        padding: 0px;
        margin-bottom: 5px;
        font-family: Arial, sans-serif;
    }
    h5 {
        margin: 0px;
        padding: 0px;
        font-family: Arial, sans-serif;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    p {
        font-family: Arial, sans-serif;
        font-size: 14px;
        line-height: 1.4;
        margin: 0;
        padding: 0;
    }
    hr {
        border: none;
        border-top: 1px solid gray;
        margin: 5px 0;
    }
    </style>
    <h2>Mesclador de PDF</h2>
    <hr>
    <h5>Instruções:</h5>
    <p style="margin-left: 25px;">
    Coloque todos os PDFs que você deseja mesclar numa pasta.<br>
    O programa irá acessar todos os arquivos dessa pasta e mesclar conforme o tipo de mesclagem escolhido.<br>
    Para isso, preencha os campos abaixo, e, ao final, clique no botão Mesclar para salvar o arquivo.
    </p>
    ''', unsafe_allow_html=True)

st.write("")

opcoes = st.selectbox(
    label='Escolha um tipo de mesclagem:',
    options=['Juntar todas as páginas de todos os PDFs',
             'Juntar pelo menos uma página de todos os PDFs'],
    index=None,
    placeholder='None'
)

if opcoes == 'Juntar pelo menos uma página de todos os PDFs':
    st.markdown('''
        <style>
        .instructions {
            margin-bottom: 15px; 
        }
        .instructions p {
            margin: 0; 
            padding: 0;
        }
        .instructions p.inner {
            margin-left: 25px; 
        }
        </style>
        <div class="instructions">
            <p>Indique as páginas a serem mescladas.<br>
            <p class="inner">
            Caso queira uma única página, digite-a.<br>
            Caso queira uma sequência consecutiva de páginas, indique a primeira e última, separadas por um hífen. Ex. 4-8 (páginas 4 a 8) <br>
            Caso queira uma sequência não consecutiva de páginas, indique a primeira e última página da sequência separadas por hífen, e entre vírgulas se for uma página individual. Ex. 4-8,10,12 (páginas 4 a 8, 10 e 12).</p>
        </div>
    ''', unsafe_allow_html=True)
    paginas = st.text_input("Páginas a serem mescladas: ")

folder_path = st.text_input("Insira o caminho da pasta com os PDFs:")
folder_path = os.path.normpath(folder_path)

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


# streamlit run C:\Users\bserpellone\Desktop\Python\github\pdf_merger\pdf_merger.py