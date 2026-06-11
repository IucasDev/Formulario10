# ⚡ Sistema EKT — Formulário de Viabilidade

Formulário digital para técnicos de campo da Neoenergia / Elektro.

**EKT-FRG-EXE-001 · Revisão 06**

## 🚀 Como usar (Streamlit Cloud)

Acesse o app em: [link gerado pelo Streamlit Cloud]

## 📁 Estrutura do projeto

```
ekt-viabilidade/
├── app.py           ← App Streamlit (abre o formulário)
├── index.html       ← Formulário completo (HTML/CSS/JS)
├── requirements.txt ← Dependências Python
└── README.md
```

## 💻 Rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/ekt-viabilidade.git
cd ekt-viabilidade

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
streamlit run app.py
```

## 📋 Funcionalidades

- Formulário de viabilidade técnica completo
- Layout mapa mental (dois blocos: Identificação/Ambiental | Execução/Logística)
- Botões SIM/NÃO para cada item
- Geração de PDF profissional
- Salvamento local (localStorage do browser)
- Exportação JPG do formulário
- Alertas para perguntas sem resposta antes de gerar PDF
- Linha Viva destacada em vermelho no PDF
