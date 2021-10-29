import argparse
from pathlib import Path

import mistune

# Lê todos os arquivos markdown dentro de input_dir
# Depois disso converte os arquivos markdown para html e salva
# a conversão dentro da pasta output_dir com a mesma organização
# relativa de pastas encontrada em input_dir
# Ou seja: input_dir/a/b/file.md -> output_dir/a/b/file.html
def main(input_dir, output_dir):
    """For each markdown file in input_dir convert it to html in output_dir and print the file name if the markdown file is more recent than the html"""
    for markdown_file in Path(input_dir).glob('**/*.md'):
        html_file = Path(output_dir, markdown_file.relative_to(input_dir)).with_suffix('.html')
        html_file.parent.mkdir(parents=True, exist_ok=True)
        if not html_file.exists() or markdown_file.stat().st_mtime > html_file.stat().st_mtime:
            print("Converted: " + markdown_file.name)
            with open(markdown_file, 'r', encoding='utf-8') as file:
                content = file.read()
            html = mistune.html(content)
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(html)



if __name__ == "__main__":
    """Collects the input_dir and output_dir from command line"""
    parser = argparse.ArgumentParser(description='Convert markdown files to html')
    parser.add_argument('input_dir', help='the directory containing the markdown files')
    parser.add_argument('output_dir', help='the directory to save the html files')
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
    print('Converted all markdown files to html')
