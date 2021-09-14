import argparse
import os
import mistune
from pathlib import Path









# Lê todos os arquivos markdown dentro de input_dir
# Depois disso converte os arquivos markdown para html e salva
# a conversão dentro da pasta output_dir com a mesma organização
# relativa de pastas encontrada em input_dir
# Ou seja: input_dir/a/b/file.md -> output_dir/a/b/file.html
def main(input_dir, output_dir):
    # Acha todos os arquivos markdown em input_dir recusivamente
    md_list = Path(f"{input_dir}").glob("**/*.md")

    for md_path in md_list:
      # Caminho relativo a partir de input_dir das páginas
      # dir = pasta, path = arquivo
      md_relative_dir = str(Path(f"{os.path.dirname(md_path)}")).replace(input_dir + "/", "")
      md_relative_path = str(Path(md_relative_dir + "/" + os.path.basename(md_path))).replace(input_dir + "/", "")

      print("Arquivo convertido:", md_relative_path)



      # Cria a pasta se ela não existe
      if not os.path.exists(str(Path(f"{output_dir}/{md_relative_dir}"))):
          os.makedirs(str(Path(f"{output_dir}/{md_relative_dir}")))



      # Lê o arquivo markdown
      with open(str(Path(f"{input_dir}/{md_relative_path}")), 'r') as md_file:
          text = md_file.read()



      # Faz a conversão
      html = mistune.html(text)



      # Salva o arquivo na pasta output_dir
      with open(str(Path(f"{output_dir}/{md_relative_path.replace('.md', '.html')}")), 'w') as html_file:
          html_file.write(html)










if __name__ == "__main__":
    # Coleta os argumentos input_dir e output_dir
    parser = argparse.ArgumentParser(description='Converter Markdown para HTML')
    parser.add_argument("input_dir", help="Caminho para ser convertido")
    parser.add_argument("output_dir", help="Caminho para salvar")
    args = parser.parse_args()

    input_dir, output_dir = args.input_dir, args.output_dir



    main(input_dir, output_dir)
