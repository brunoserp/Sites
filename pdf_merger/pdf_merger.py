import streamlit as st
import PyPDF2
import re
import io

# ___________________________________________________________________________________________________________________________________
# Funções para mesclagem de PDFs
# ___________________________________________________________________________________________________________________________________

def todo_pdf(uploaded_files, nome_arquivo="pdf_merged.pdf"):
    merger = PyPDF2.PdfMerger()
    for file in uploaded_files:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        merger.append(pdf_reader)

    output = io.BytesIO()
    try:
        merger.write(output)
        output.seek(0)  # Reset the buffer position to the beginning
        return output.getvalue()
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar o PDF: {e}")
    finally:
        merger.close()

def mesclar_pdfs(uploaded_files, paginas, nome_arquivo="pdf_merged.pdf"):
    merger = PyPDF2.PdfMerger()
    paginas = paginas.split(',')
    for file in uploaded_files:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        pdf_writer = PyPDF2.PdfWriter()
        for pagina in paginas:
            if '-' in pagina:
                start, end = pagina.split('-')
                for i in range(int(start), int(end) + 1):
                    if i <= len(pdf_reader.pages):
                        pdf_writer.add_page(pdf_reader.pages[i - 1])
            else:
                try:
                    page_number = int(pagina)
                    if page_number <= len(pdf_reader.pages):
                        pdf_writer.add_page(pdf_reader.pages[page_number - 1])
                except ValueError:
                    st.error(f"O número da página '{pagina}' não é válido.")
                    return
        if pdf_writer.pages:
            temp_output = io.BytesIO()
            pdf_writer.write(temp_output)
            temp_output.seek(0)
            temp_pdf_reader = PyPDF2.PdfReader(temp_output)
            merger.append(temp_pdf_reader)

    output = io.BytesIO()
    try:
        merger.write(output)
        output.seek(0)  # Reset the buffer position to the beginning
        return output.getvalue()
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

st.write("Faça o upload dos PDFs que você deseja mesclar:")
uploaded_files = st.file_uploader("Escolha arquivos PDF", type="pdf", accept_multiple_files=True)

if st.button("Mesclar"):
    if uploaded_files:
        if opcoes == 'Juntar todas as páginas de todos os PDFs':
            pdf_data = todo_pdf(uploaded_files)
        elif opcoes == 'Juntar pelo menos uma página de todos os PDFs':
            if not re.fullmatch(r'[0-9,-]+', paginas):
                st.write('A sequência de páginas que você informou não é compatível com as instruções. Reescreva-a corretamente.')
                pdf_data = None
            else:
                pdf_data = mesclar_pdfs(uploaded_files, paginas)
        if pdf_data:
            st.download_button(
                label="Baixar PDF Mesclado",
                data=pdf_data,
                file_name="pdf_merged.pdf",
                mime="application/pdf"
            )
    else:
        st.write("Por favor, faça o upload de pelo menos um arquivo PDF.")

# streamlit run C:\Users\bserpellone\Desktop\Python\github\pdf_merger\pdf_merger.py