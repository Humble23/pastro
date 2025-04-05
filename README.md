# Sistema Organizador de Pastas (Pastro)

Um aplicativo desktop desenvolvido em Python para organização automática de pastas e arquivos.

## 🚀 Funcionalidades

- **Interface Gráfica Intuitiva**
  - Seleção de pastas para organização
  - Visualização em árvore dos arquivos
  - Preview das alterações antes de aplicar
  - Barra de progresso para acompanhamento

- **Classificação Automática**
  - Identificação de tipos de arquivos
  - Categorização por extensão
  - Suporte para múltiplos formatos

## 📋 Pré-requisitos

- Python 3.13 ou superior
- PyQt6
- Outras dependências listadas em `requirements.txt`

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd pastro
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

1. Execute o programa:
```bash
python src/main.py
```

2. Na interface:
   - Selecione a pasta que deseja organizar
   - Visualize a estrutura atual
   - Clique em "Organizar" para ver o preview
   - Confirme para aplicar as alterações

## 📦 Distribuição

O projeto inclui um arquivo `pastro.spec` para gerar o executável usando PyInstaller:

```bash
cd src
pyinstaller pastro.spec
```

O executável será gerado em `src/dist/Pastro.exe`

## 📝 Notas

- O programa mantém um backup da estrutura original
- As alterações podem ser visualizadas antes de serem aplicadas
- O processo de organização é detalhado em logs

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 