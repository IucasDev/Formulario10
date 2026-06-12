# Documentação Técnica — Formulário de Viabilidade EKT

**Arquivo:** `index.html` (single page application)
**Versão:** EKT-FRG-EXE-001 · Rev.06
**Público:** Desenvolvedor sênior — integração com banco de dados corporativo

---

## 1. Visão Geral

Trata-se de um formulário de viabilidade técnica 100% front-end, executado inteiramente no navegador (cliente). O arquivo único `index.html` contém todo o HTML, CSS e JavaScript necessários para seu funcionamento.

### Dependências externas (CDN)

> ⚠️ Na primeira carga é necessária conexão com a internet para baixar esses assets. Após o cache, o formulário funciona offline.

| Biblioteca | Finalidade |
|---|---|
| jsPDF 2.5.1 | Geração do PDF em paisagem |
| jspdf-autotable 3.8.2 | Tabelas no PDF |
| html2canvas 1.4.1 | Captura da tela para JPG |
| Google Fonts (DM Sans / DM Mono) | Tipografia |

---

## 2. Estrutura e Fluxo de Navegação

O formulário utiliza um sistema de **blocos progressivos**: cada seção só é exibida após a seção anterior ser totalmente preenchida.

### Mecanismo de progressão

Cada bloco relevante possui um `id` (ex: `sub-aterramento`, `sub-lv-campo`, `sub-logistica`, etc.) e as classes CSS `.progressive-section.hidden`. A função `verificarProgressao()` controla a visibilidade:

```javascript
// Lógica central: disparada a cada mudança de input
function verificarProgressao() {
  // 1. Verifica gate fotovoltaico
  // 2. Se FV=SIM → mostra dados FV, oculta não-FV
  // 3. Se FV=NÃO → avança por 13 estágios
  //    Cada estágio verifica se o anterior foi
  //    completamente respondido antes de liberar o próximo
}
```

### Validação de bloco completo

A função `secaoCompleta(id)` verifica se **todos os grupos de radio button** dentro de um bloco foram respondidos:

```javascript
function radiosCompletos(container) {
  // Agrupa inputs[type=radio] por name
  // Retorna true apenas se TODOS os grupos
  // possuem ao menos um radio checked
}
```

Isso garante que nenhuma pergunta fique sem resposta antes de liberar o próximo bloco.

### Árvore de navegação (fluxo FV=NÃO)

```
Identificação (sempre visível)
└── Pedido de Fotovoltaico?
    ├── SIM → libera dados FV + calculadora SIGFI
    └── NÃO → libera sequencialmente:
        1. Tensão da Rede
        2. Regime de Linha Viva
        3. Aterramento
        4. LV Campo (Fotos, Manobra, Big Jumper, ..., Chave Faca)
        5. Risco Eminente + Período de Execução
        6. Ambiental
        7. Local da Intervenção
        8. Logística
        9. Checklist
        10. Projeto & Diversos
        11. Executar Obra
        12. Atenção
        13. Anotações Gerais
        └── (fim) → barra de ações visível
```

---

## 3. Persistência de Dados

### Estado atual: localStorage

Atualmente, **todos os dados do formulário são armazenados exclusivamente no `localStorage` do navegador do usuário**.

```javascript
// Estrutura de armazenamento
localStorage.setItem('formularios', JSON.stringify(lista));

// Cada item na lista
{
  id: 1712345678901,           // timestamp único
  nome_arquivo: "OBRA JOAO",  // nome dado pelo usuário
  nome_cliente: "...",
  codigo_projeto: "...",
  fotovoltaico_gate: "sim",
  tensao_345_chk: "sim",
  modelo_aterramento: "B_Linear",
  // ... todos os campos do formulário
}
```

### Limitações do localStorage

| Aspecto | Detalhe |
|---|---|
| Capacidade | ~5-10 MB por domínio |
| Persistência | Apenas no navegador do usuário |
| Compartilhamento | Não há — cada dispositivo tem seus próprios dados |
| Backup | Nenhum — limpeza de cache apaga tudo |
| Acesso servidor | Inexistente — o servidor não vê esses dados |

> **Conclusão:** O `localStorage` é adequado para rascunhos temporários, mas **não substitui um banco de dados corporativo**.

---

## 4. Recomendação de Integração com Banco de Dados Corporativo

Para que os dados sejam armazenados no banco de dados do site da empresa, é necessário **enviar as informações do formulário para o backend via requisição HTTP (API REST)**.

### Arquitetura sugerida

```
[Navegador]              [Servidor Web]            [Banco de Dados]
    │                          │                         │
    │  POST /api/viabilidade   │                         │
    ├─────────────────────────►│                         │
    │  { todos os campos }    │  INSERT INTO             │
    │                          │  viabilidade (...)       │
    │                          ├────────────────────────►│
    │                          │                         │
    │◄─────────────────────────┤                         │
    │  { id: 42, status: "ok"}│                         │
    │                          │                         │
    │  localStorage.clear()   │                         │
    │  (opcional)             │                         │
```

### Como implementar

#### No front-end (index.html)

Acrescentar uma função de envio ao servidor:

```javascript
async function enviarParaServidor(dados) {
  const response = await fetch('https://site-da-empresa.com/api/viabilidade', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
  });
  if (!response.ok) throw new Error('Falha ao salvar no servidor');
  return response.json();
}
```

Essa função deve ser chamada **após o usuário confirmar o salvamento**, por exemplo no final da função `salvarFormulario()` (atualmente linha ~1455):

```javascript
function salvarFormulario() {
  var dados = coletarDados();
  // ... salva no localStorage (rascunho local) ...
  
  // NOVO: enviar também para o servidor
  enviarParaServidor(dados)
    .then(resp => console.log('Salvo no BD:', resp.id))
    .catch(err => console.warn('Falha no servidor, dados mantidos localmente:', err));
}
```

#### Modelo de dados sugerido (tabela `viabilidade`)

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | SERIAL PK | Identificador único |
| `nome_cliente` | VARCHAR(255) | Nome do cliente |
| `codigo_projeto` | VARCHAR(50) | Código EKT do projeto |
| `telefone_cliente` | VARCHAR(15) | Telefone com DDD |
| `data_cadastro` | DATE | Data preenchida no form |
| `projetista_1` | VARCHAR(255) | Nome projetista 1 |
| `projetista_2` | VARCHAR(255) | Nome projetista 2 |
| `fotovoltaico_gate` | CHAR(3) | 'sim' / 'nao' |
| `ligacao_nova_fv` | CHAR(3) | 'sim' / 'nao' / 'na' |
| `alteracao_carga_fv` | CHAR(3) | 'sim' / 'nao' / 'na' |
| `sigfi_atual` | VARCHAR(20) | SIGFI atual |
| `sigfi_alteracao` | VARCHAR(20) | Novo SIGFI |
| `tensao_345_chk` | CHAR(3) | 'sim' / '' |
| `tensao_138_chk` | CHAR(3) | 'sim' / '' |
| `linha_viva` | CHAR(3) | 'sim' / 'nao' |
| `modelo_aterramento` | VARCHAR(30) | Modelo de aterramento |
| `obs_aterramento` | TEXT | Observações de aterramento |
| `foto_obrigatoria` | CHAR(3) | 'sim' |
| `manobra` | CHAR(3) | 'sim' / 'nao' |
| `big_jumper` | CHAR(3) | 'sim' / 'nao' |
| `bt_energizado` | CHAR(3) | 'sim' / 'nao' |
| `proj_estrutura_trabalhar` | CHAR(3) | 'sim' / 'nao' |
| `estrutura_canadense` | CHAR(3) | 'sim' / 'nao' |
| `fio_caz` | CHAR(3) | 'sim' / 'nao' |
| `poste_podre` | CHAR(3) | 'sim' / 'nao' |
| `cf_provisoria` | CHAR(3) | 'sim' / 'nao' |
| `risco_eminente` | CHAR(3) | 'sim' / 'nao' |
| `prazo_risco` | VARCHAR(15) | '30 dias' / '45 dias' / '60 dias' / 'Urgente' / 'N/A' |
| `periodo_execucao` | VARCHAR(15) | 'semana' / 'fimsemana' / 'indiferente' |
| `amb_abertura_faixa` | CHAR(3) | 'sim' / 'nao' |
| `amb_poda_qtd` | INTEGER | Quantidade de podas |
| `amb_corte_qtd` | INTEGER | Quantidade de cortes |
| `aut_prop_poda` | CHAR(3) | 'sim' / 'nao' |
| `aut_prop_corte` | CHAR(3) | 'sim' / 'nao' |
| `padrao_terreno_3` | CHAR(3) | 'sim' / 'nao' |
| `autorizacao_passagem` | CHAR(3) | 'sim' / 'nao' |
| `travessia_ocup` | CHAR(3) | 'sim' / 'nao' |
| `formular_ocupar` | CHAR(3) | 'sim' / 'nao' |
| `amb_app` | CHAR(3) | 'sim' / 'nao' |
| `amb_unidade_conservacao` | CHAR(3) | 'sim' / 'nao' |
| `licenca_ambiental` | CHAR(3) | 'sim' / 'nao' |
| `intervencao_em` | TEXT | Descrição do local |
| `distribuir_postes` | CHAR(3) | 'sim' / 'nao' |
| `apoio_distribuicao` | CHAR(3) | 'sim' / 'nao' |
| `sinaliza_transito` | CHAR(3) | 'sim' / 'nao' |
| `sinal_celular` | CHAR(3) | 'sim' / 'nao' |
| `acesso_chuva` | CHAR(3) | 'sim' / 'nao' |
| `acesso_caminhao` | CHAR(3) | 'sim' / 'nao' |
| `porteira_cadeada` | CHAR(3) | 'sim' / 'nao' |
| `possui_nome_rua` | CHAR(3) | 'sim' / 'nao' |
| `abelha_poste` | CHAR(3) | 'sim' / 'nao' |
| `cava_rocha` | CHAR(3) | 'sim' / 'nao' |
| `cava_profunda` | CHAR(3) | 'sim' / 'nao' |
| `tubulacao_gas` | CHAR(3) | 'sim' / 'nao' |
| `piquetespray` | CHAR(3) | 'sim' / 'nao' |
| `reparo_calcada` | CHAR(3) | 'sim' / 'nao' |
| `reparo_calcada_especial` | CHAR(3) | 'sim' / 'nao' |
| `indicado_dxf` | CHAR(3) | 'sim' / 'nao' |
| `efeito_montante_jusante` | CHAR(3) | 'sim' / 'nao' / 'na' |
| `substituir_trafo` | CHAR(3) | 'sim' / 'nao' |
| `barramento` | CHAR(3) | 'sim' / 'nao' |
| `ligacao_cc_pr` | CHAR(3) | 'sim' / 'nao' |
| `pintar_conf_tomb` | CHAR(3) | 'sim' / 'nao' |
| `possui_glv` | CHAR(3) | 'sim' / 'nao' |
| `instalar_protetor` | CHAR(3) | 'sim' / 'nao' |
| `verificado_adequacao` | CHAR(3) | 'sim' / 'nao' |
| `doar_padrao` | CHAR(3) | 'sim' / 'nao' |
| `trocar_medidores` | CHAR(3) | 'sim' / 'nao' |
| `medidor_ligado` | CHAR(3) | 'sim' / 'nao' |
| `num_medidor` | VARCHAR(50) | Número do medidor |
| `cc_reta_guarda` | VARCHAR(50) | Confiabilidade RetaGuarda |
| `num_clientes` | INTEGER | Número de clientes |
| `apoio_caixa` | CHAR(3) | 'sim' / 'nao' |
| `apoio_tubulacao` | CHAR(3) | 'sim' / 'nao' |
| `verificou_rede_ip` | CHAR(3) | 'sim' / 'nao' |
| `telefonica` | CHAR(3) | 'sim' / 'nao' |
| `apoio_drops` | CHAR(3) | 'sim' / 'nao' |
| `apoio_fibra` | CHAR(3) | 'sim' / 'nao' |
| `anotacoes` | TEXT | Observações gerais |
| `created_at` | TIMESTAMP | Data/hora do preenchimento |
| `updated_at` | TIMESTAMP | Data/hora da última alteração |
| `usuario_id` | INTEGER FK | (opcional) vínculo com tabela de usuários |

---

## 5. Pontos de Atenção para o Desenvolvedor

### 5.1. Coleta dos dados

A função `coletarDados()` (linha ~1416) retorna um objeto JavaScript com **todos os campos do formulário**, incluindo os campos de checkbox (tensão) e período de execução que não são capturados automaticamente pelo `FormData`:

```javascript
function coletarDados() {
  var form = document.getElementById('form-viabilidade');
  var fd = new FormData(form);
  var dados = {};
  for (var pair of fd.entries()) dados[pair[0]] = pair[1];
  // Campos extras não capturados pelo FormData:
  dados.tensao_345_chk = document.getElementById('tensao_345_chk').checked ? 'sim' : '';
  dados.tensao_138_chk = document.getElementById('tensao_138_chk').checked ? 'sim' : '';
  dados.periodo_execucao = document.getElementById('periodo_execucao').value || '';
  return dados;
}
```

### 5.2. Sincronização localStorage + banco

Recomenda-se uma estratégia híbrida:
- **localStorage**: rascunhos locais (já implementado)
- **Banco de dados**: registro oficial (a implementar)

Fluxo sugerido:
1. Usuário preenche o formulário
2. Ao clicar "Salvar", os dados vão para o **localStorage** (rascunho) **e** para o **banco via API**
3. Se o usuário estiver offline, os dados permanecem apenas no localStorage
4. Quando voltar online, um mecanismo de sincronização pode enviar os rascunhos pendentes

### 5.3. Geração de PDF

A função `gerarPDF()` (linha ~1546) gera o PDF diretamente no navegador usando jsPDF. O PDF é baixado automaticamente. Caso o desenvolvedor queira armazenar o PDF no servidor, pode-se converter o blob em Base64 e enviá-lo junto com os dados do formulário.

---

## 6. Resumo para Tomada de Decisão

| Item | Situação atual | Recomendação |
|---|---|---|
| Armazenamento | `localStorage` (navegador) | Manter para rascunhos + adicionar API REST |
| Compartilhamento | Nenhum | Banco de dados corporativo |
| Offline | Sim (após cache inicial) | Sim (localStorage cobre) |
| PDF | Gerado no client | Pode ser armazenado como blob no BD |
| JPG | Gerado no client | Idem |
| Dados estruturados | Objeto JS simples | Mapeamento 1:1 para tabela SQL |

---

## 7. Contato

Documentação gerada em junho de 2026.
Para dúvidas sobre a implementação ou alteração no formulário, abrir chamado com a equipe de desenvolvimento responsável.
