# Regras do Projeto Pastro

## Objetivo
O objetivo do projeto é ser um sistema organizador de pastas construído em Python, com interface gráfica que permite a seleção de pastas específicas para organização automática por categorias.

## Funcionalidades Implementadas
1. Interface Gráfica (PyQt6)
   - Seleção de pastas
   - Visualização em árvore
   - Preview de alterações
   - Barra de progresso
   - Splash screen

2. Organização Automática
   - Classificação por extensão
   - Categorização inteligente
   - Backup automático
   - Logs detalhados

3. Distribuição
   - Executável standalone
   - Ícone personalizado
   - Recursos embutidos

## Regras de Desenvolvimento
1. Código
   - Manter código em inglês
   - Documentação em português
   - Seguir PEP 8
   - Usar type hints

2. Interface
   - Design responsivo
   - Feedback visual claro
   - Mensagens em português
   - Ícones intuitivos

3. Organização
   - Estrutura modular
   - Separação de responsabilidades
   - Código reutilizável
   - Documentação atualizada

4. Recursos
   - Manter arquivos de recursos em `src/resources`
   - Usar PNG para imagens com transparência
   - Usar ICO para ícones do Windows
   - Incluir recursos no executável

5. Distribuição
   - Gerar executável com PyInstaller
   - Incluir todos os recursos necessários
   - Manter arquivo .spec atualizado
   - Testar em diferentes ambientes

## Próximos Passos
1. Melhorias de Performance
   - Otimização do classificador
   - Cache de resultados
   - Processamento assíncrono

2. Novas Funcionalidades
   - Regras personalizadas
   - Filtros avançados
   - Plugins/extensões

3. Documentação
   - Manual do usuário
   - Guia de desenvolvimento
   - Exemplos de uso