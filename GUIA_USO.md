# 📱 Guia de Uso — Formulário de Viabilidade EKT (Offline no Celular)

## 🔧 Como salvar o formulário no celular para usar sem internet

### 1. Baixar os arquivos
Você precisa de **3 arquivos** na pasta `aaaa/`:

| Arquivo | Descrição |
|---------|-----------|
| `index.html` | O formulário em si |
| `manifest.json` | Para instalar como app |
| `.devcontainer/` | (opicional, ignore) |

> ⚠️ **Importante:** Na primeira vez que usar, você PRECISA de internet para carregar as fontes e bibliotecas (jsPDF, html2canvas). Depois da primeira carga, o navegador guarda em cache e funciona offline.

### 2. Instalar no celular

**Android — Google Chrome:**

1. Abra o arquivo `index.html` no Chrome
2. Toque nos **3 pontinhos** ⋮ (canto superior direito)
3. Toque em **"Adicionar à tela inicial"**
4. Confirme — o ícone "SISTEMA EKT" aparecerá na sua tela inicial
5. Pronto! Use como se fosse um app 📲

**iPhone — Safari:**

1. Abra o arquivo `index.html` no Safari
2. Toque no **ícone de compartilhar** 📤 (parte inferior)
3. Role para baixo e toque em **"Adicionar à Tela de Início"**
4. Confirme — o ícone aparecerá na tela inicial

> ✅ Depois de aberto uma vez com internet, o formulário funciona **completamente offline** (os dados ficam salvos no próprio celular).

---

## 🧭 Navegando pelo formulário

O formulário foi dividido em **blocos progressivos**: você só vê a próxima seção depois de responder a atual.

```
Identificação → [sempre visível]
  └─ Pedido de Fotovoltaico? (SIM / NÃO)
       ├── SIM → mostra dados de Fotovoltaico + SIGFI
       └── NÃO → mostra blocos na sequência abaixo
```

### Fluxo completo (quando NÃO é fotovoltaico)

```
  1️⃣ Tensão da Rede       → escolha 34,5kV ou 13,8kV
  2️⃣ Linha Viva            → SIM ou NÃO
  3️⃣ Aterramento           → preencha o modelo
  4️⃣ Campo                 → Fotos, Manobra, Big Jumper, etc.
  5️⃣ Risco + Período       → Risco eminente + Prazo + Período execução
  6️⃣ Ambiental             → Faixa, poda, corte, intervenção
  7️⃣ Local da Intervenção  → descreva o local
  8️⃣ Logística             → postes, acesso, sinal, etc.
  9️⃣ Checklist             → abelha, rocha, gás, cercas, etc.
  🔟 Projeto & Diversos    → transformador, barramento, etc.
  1️⃣1️⃣ Executar Obra        → medidores, clientes, etc.
  1️⃣2️⃣ Atenção              → caixa, tubulação, fibra, etc.
  1️⃣3️⃣ Anotações            → observações finais
```

> ✅ Após o último bloco, a **barra de ações** aparece com os botões Salvar / PDF / JPG.

---

## 💾 Salvando e recuperando formulários

### Salvar um rascunho
1. Toque em **"💾 Salvar"** (barra inferior)
2. Digite um nome para o registro (ex: "OBRA JOAO SILVA")
3. Confirme — aparece a mensagem "✅ Salvo"

### Carregar um salvo
1. Toque em **"📋 Salvos"** (cabeçalho ou barra inferior)
2. Uma janela abre com a lista de formulários salvos
3. Toque em **"Abrir"** no registro desejado
4. O formulário é preenchido automaticamente

### Excluir um salvo
1. Abra **"📋 Salvos"**
2. Toque em **"Excluir"** no registro
3. Confirme a exclusão

> 💡 Os dados ficam salvos no **armazenamento local do celular** (localStorage). Eles permanecem mesmo sem internet.

---

## 📄 Gerando PDF

1. Responda **todas as perguntas** dos blocos liberados
2. A barra inferior aparecerá com o botão **"📄 Gerar PDF"**
3. Toque no botão — o PDF será baixado automaticamente
4. O PDF sai no formato **paisagem (horizontal)** com todos os dados

> ⚠️ O PDF só pode ser gerado quando todos os blocos obrigatórios forem respondidos.

---

## 📸 Salvando como JPG

1. Complete o formulário
2. Toque em **"📸 Salvar JPG"**
3. A imagem será gerada em **formato paisagem (horizontal)**
4. O JPG é baixado com o código do projeto no nome

---

## 🆕 Começar um novo formulário

1. Toque em **"🆕 Novo"** (cabeçalho ou barra inferior)
2. Confirme que deseja limpar
3. O formulário é resetado

---

## ⚡ Dicas rápidas

- **Campos em maiúsculo** automaticamente — não precisa usar Shift
- **Telefone**: digite o DDD (2 dígitos) — o cursor pula para o número automaticamente
- **Datas**: use o seletor de data nativo
- **Código do projeto**: fica em destaque laranja (obrigatório)
- **N/A**: use a opção "N/A" quando a pergunta não se aplicar
- **Tensão**: as opções são exclusivas (uma desmarca a outra)

---

## 🐛 Problemas comuns

| Problema | Solução |
|----------|---------|
| "O PDF não gerou" | Verifique se todos os blocos foram respondidos |
| "Perdi meus dados" | Os dados ficam no celular — não limpe o cache do navegador |
| "Não aparece a barra de ações" | Complete todos os blocos liberados |
| "A fonte está diferente" | Conecte-se à internet e recarregue a página uma vez |
| "O botão Salvar JPG não funciona" | Pode ser bloqueado pelo navegador — permita downloads |
