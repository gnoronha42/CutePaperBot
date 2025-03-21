# 🛒 Automação de Cadastro de Produtos com Selenium e IA 🤖

Este projeto surgiu da necessidade de automatizar o cadastro de 660 produtos em uma plataforma de e-commerce, tarefa que seria extremamente tediosa e demorada se feita manualmente. Utilizando o Selenium, conseguimos automatizar esse processo, especificamente para uma papelaria online. Além disso, integramos um agente de IA local, como o Ollama, para gerar descrições de produtos de forma criativa e personalizada. ✨

## ✨ Funcionalidades

- **🔐 Automação de Login**: Realiza login automático na plataforma utilizando email e código de segurança.
- **📦 Cadastro de Produtos**: Preenche automaticamente os campos de nome, descrição e estoque dos produtos a partir de um arquivo CSV.
- **📝 Geração de Descrições**: Utiliza IA para criar descrições curtas e fofas para produtos de papelaria, incorporando emojis para um toque especial.
- **🤖 Integração com Ollama**: Executa modelos de linguagem localmente para garantir privacidade e eficiência.

## 🚀 Como Usar

1. **⚙️ Configuração do Ambiente**: Instale as dependências necessárias, incluindo Selenium, pandas, e configure o Ollama com um modelo de linguagem adequado.
2. **▶️ Execução do Script**: Execute o script `app.py` para iniciar o processo de automação.
3. **🔑 Entrada Manual do Código de Segurança**: Insira o código de segurança enviado para o seu email quando solicitado.
4. **🔍 Verificação e Ajustes**: Monitore a execução e ajuste os XPaths conforme necessário para garantir a compatibilidade com a estrutura atual da página.

## 📋 Requisitos

- Python 3.x
- Selenium
- pandas
- Ollama (para execução de IA local)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias e novas funcionalidades.
