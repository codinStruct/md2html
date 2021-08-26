import argparse
import glob
import xml.etree.ElementTree as ET
import os
# import markdown
import gh_md_to_html.core_converter
from pathlib import Path









# Lê todos os arquivos */estrutura.xml dentro de input_dir
# e acha o caminho de todas as páginas cujo xml segue assim:
# categoria>assunto>page.md (usando os atributos 'caminho')
# Depois disso converte os arquivos markdown para html e salva
# a conversão dentro da pasta output_dir com a mesma organização
# relativa de pastas encontrada em input_dir
# Ou seja: input_dir/a/b/file.md -> output_dir/a/b/file.html
def main(input_dir, output_dir):
    # Acha todos os arquivos estrutura.xml dentro de uma pasta em input_dir
    xml_list = glob.glob(f"{input_dir}/*/estrutura.xml")



    # Loop por todos os arquivos
    for xml_path in xml_list:
        root = ET.parse(xml_path).getroot()

        # Encontrando todos as páginas
        for categoria in root.findall("categoria"):
            for assunto in categoria.findall("assunto"):
                for page in assunto.findall("page"):

                    # Caminho relativo a partir de input_dir das páginas
                    # dir = pasta, path = arquivo
                    md_relative_dir = f"{os.path.basename(os.path.dirname(xml_path))}\\{categoria.attrib['caminho']}\\{assunto.attrib['caminho']}"
                    md_relative_path = f"{md_relative_dir}\\{page.attrib['caminho']}"

                    print(md_relative_path)



                    # Cria a pasta se ela não existe
                    if not os.path.exists(f"{output_dir}\\{md_relative_dir}"):
                        os.makedirs(f"{output_dir}\\{md_relative_dir}")

                    # # Lê o arquivo markdown
                    with open(f"{input_dir}\\{md_relative_path}", 'r') as md_file:
                        text = md_file.read()
                    


                    # Faz a conversão
                    # TODO: Achar uma maneira melhor de converter para html
                    # html = markdown.markdown(text, extensions=['extra','abbr','attr_list','def_list','fenced_code','footnotes','md_in_html','tables','admonition','codehilite','legacy_attrs','legacy_em','meta','nl2br','sane_lists','smarty','toc','wikilinks'])
                    html = gh_md_to_html.core_converter.markdown(text)


                    # Salva o arquivo na pasta output_dir
                    with open(f"{output_dir}\\{md_relative_path.replace('.md', '.html')}", 'w') as html_file:
                        html_file.write(html)










if __name__ == "__main__":
    # Coleta os argumentos input_dir e output_dir
    parser = argparse.ArgumentParser(description='Converter Markdown para HTML')
    parser.add_argument("input_dir", help="Caminho para ser convertido")
    parser.add_argument("output_dir", help="Caminho para salvar")
    args = parser.parse_args()

    input_dir, output_dir = args.input_dir, args.output_dir



    main(input_dir, output_dir)