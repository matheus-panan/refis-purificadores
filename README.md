# Sistema de Gestão de Leads para Refis e Purificadores

## 📋 Visão Geral

Este é um sistema automatizado desenvolvido em Google Apps Script para gerenciar vendas de refis e purificadores. Ele organiza, classifica e distribui leads (clientes potenciais) entre duas funcionárias (Maria e Gabrielly), automatizando todo o processo operacional.

## 🏗️ Estrutura do Sistema

### Componentes Principais:
- **Google Sheets (Planilhas)**: Armazena todos os dados
- **Google Apps Script**: Executa as automações
- **Sistema de Pontuação**: Classifica clientes por potencial de compra
- **Gatilhos Automáticos**: Executa tarefas em horários específicos

---

## 📊 Planilhas do Sistema

### 1. **"Base de dados BI"**
**O que é:** Planilha principal com todos os clientes e suas informações
**Colunas principais:**
- A: ID do cliente
- B: Nome do cliente
- C: Data da última compra
- D: Dias sem compra
- F: Descrição do produto
- G: Status (Ligar/Não ligar/Aguardar)
- H: Número de compras (notas)
- I: Data da última ligação
- J: Status da última ligação
- K: Observações
- L: Score (pontuação calculada)

### 2. **"Historico ligações"**
**O que é:** Registra todas as ligações feitas para os clientes
**Informações guardadas:**
- ID do cliente
- Nome
- Status da ligação (Venda, Não atende, etc.)
- Data da ligação
- Observações

### 3. **"Lista Maria" e "Lista Gabrielly"**
**O que são:** Listas individuais de 40 clientes para cada funcionária ligar
**Como funciona:** O sistema distribui automaticamente os melhores clientes entre elas

---

## 🔄 Como o Sistema Funciona (Passo a Passo)

### **Fase 1: Preparação dos Dados**
1. **Atualização da Base** (`atualizaBase.js`)
   - Pega informações do histórico de ligações
   - Atualiza a base principal com os dados mais recentes
   - Remove duplicatas e organiza os status

2. **Cálculo de Pontuação** (`calculaScore.js`)
   - Analisa cada cliente e dá uma nota de 0 a 100
   - Considera fatores como:
     - Tempo sem comprar
     - Resultado da última ligação
     - Número de compras anteriores
   - Classifica em cores:
     - 🟢 Verde: Clientes bons (score > 35)
     - 🟡 Amarelo: Clientes médios (score 5-35)
     - 🔴 Vermelho: Clientes ruins (score < 5)

### **Fase 2: Geração das Listas** (`geraListas.js`)
1. **Seleção de Clientes Válidos**
   - Filtra apenas clientes com status "Ligar"
   - Embaralha a lista para distribuição aleatória

2. **Distribuição**
   - Divide 80 clientes entre Maria (40) e Gabrielly (40)
   - Limpa as listas antigas
   - Insere os novos clientes

### **Fase 3: Cópia para Planilhas Individuais**
1. **Envio para Funcionárias** (`atualizaListaFunc.js`)
   - Copia a lista da Maria para sua planilha individual
   - Copia a lista da Gabrielly para sua planilha individual
   - Mantém formatação e cores

2. **Cópia de Cores** (`copiaCores.js`)
   - Transfere as cores da classificação (verde/amarelo/vermelho)
   - Facilita identificação visual dos melhores clientes

### **Fase 4: Registro do Trabalho**
1. **Histórico de Ligações** (`copiaHistorico.js`)
   - Quando as funcionárias preenchem o resultado das ligações
   - Sistema copia automaticamente para o histórico geral
   - Organiza por data para controle

---

## ⏰ Automações e Horários

### **Gatilhos Automáticos** (`configGatilhos.js`)

| Horário | Função | O que faz |
|---------|--------|-----------|
| 07:55 | Gerar Listas | Cria as listas diárias (exceto domingos) |
| 08:05 | Copiar para Funcionárias | Envia listas para planilhas individuais |
| 22:00 | Atualizar Base | Processa histórico e atualiza dados |

---

## 🎯 Sistema de Pontuação (Score)

### **Como é calculado:**

**Base:** Todo cliente começa com 10 pontos

**Status da última ligação:**
- ✅ Venda: +15 pontos
- ❌ Não atende/Caixa postal: -5 pontos
- ❌ Número incorreto/Outra cidade: -10 pontos
- ❌ Não ligar mais: -20 pontos

**Tempo sem comprar:**
- 📈 270-539 dias + status "Ligar": +25 pontos
- 📈 Status "Aguardar": +10 pontos
- 📉 540-730 dias: -5 pontos
- 📉 730-1095 dias: -10 pontos
- 📉 Mais de 1095 dias: -15 a -20 pontos

**Histórico de compras:**
- Mais compras = mais pontos (multiplicador varia com tempo)

### **Resultado Final:**
- 🟢 **Verde (>35 pontos)**: Clientes com alta chance de compra
- 🟡 **Amarelo (5-35 pontos)**: Clientes com chance média
- 🔴 **Vermelho (<5 pontos)**: Clientes com baixa chance

---

## 💼 Fluxo de Trabalho Diário

### **Para as Funcionárias:**
1. **Manhã (08:05):** Recebem automaticamente lista com 40 clientes
2. **Durante o dia:** Fazem ligações e anotam resultados
3. **Final do dia:** Preenchem status das ligações na planilha
4. **Noite (22:00):** Sistema processa automaticamente os resultados

### **Para o Gestor:**
- **Visualização:** Cores indicam prioridade dos clientes
- **Controle:** Histórico completo de todas as ligações
- **Análise:** Relatórios automáticos de performance

---

## 📈 Vantagens do Sistema

### **Eficiência:**
- ✅ Distribuição automática e equilibrada
- ✅ Priorização inteligente por potencial
- ✅ Eliminação de trabalho manual repetitivo

### **Controle:**
- ✅ Histórico completo de todas as ações
- ✅ Evita ligações para clientes que não querem ser contatados
- ✅ Rastreamento de performance individual

### **Inteligência:**
- ✅ Aprende com resultados anteriores
- ✅ Melhora recomendações com o tempo
- ✅ Identifica padrões de comportamento dos clientes

---

## 🔧 Configuração e Manutenção

### **Arquivos Principais:**
- `geraListas.js`: Motor principal do sistema
- `calculaScore.js`: Inteligência de pontuação
- `atualizaBase.js`: Processamento de dados
- `configGatilhos.js`: Automações

### **Como Adicionar Nova Funcionária:**
1. Criar nova planilha individual
2. Adicionar função em `atualizaListaFunc.js`
3. Configurar novo gatilho em `configGatilhos.js`
4. Ajustar distribuição em `geraListas.js`

### **Personalização de Horários:**
- Editar horários em `configGatilhos.js`
- Alterar critérios de pontuação em `calculaScore.js`
- Modificar quantidade de clientes por lista em `geraListas.js`


## 🆘 Troubleshooting

### **Problemas Comuns:**
- **Listas não geram:** Verificar se há clientes com status "Ligar"
- **Cores não aparecem:** Executar função `copiarCoresPorID()`
- **Gatilhos não funcionam:** Recriar triggers em `configGatilhos.js`
- **Dados não atualizam:** Verificar permissões das planilhas

### **Manutenção Regular:**
- Limpar histórico antigo periodicamente
- Revisar critérios de pontuação mensalmente
- Backup das configurações importantes
