# PRISMA

**P.R.I.S.M.A. --- Plataforma de Recursos Interativos para Simulação,
Modelagem e Aprendizagem**

> **Transformando código em experiência.**

O **PRISMA** é uma aplicação desktop educacional desenvolvida em Python
com PySide6. Seu objetivo é oferecer um ambiente visual e interativo
para explorar conceitos de programação, permitindo acompanhar
algoritmos, estruturas de dados, execução de código, APIs e bancos de
dados de forma prática.

O projeto também serve como aplicação-base para uma formação em
desenvolvimento de interfaces desktop com Python e Qt, evoluindo ao
longo do curso conforme novos conceitos são apresentados.

## Recursos atuais

Nesta etapa do desenvolvimento, o PRISMA já possui:

-   navegação entre as principais áreas da aplicação, com cards clicáveis
    no Dashboard e botões disponíveis em todas as páginas;
-   Playground para escrita e execução de código Python;
-   editor de código customizado com numeração de linhas e destaque da
    linha atual, compartilhado pelo Playground e pelo DB Lab;
-   mensagens amigáveis para erros comuns de execução;
-   visualização passo a passo de algoritmos;
-   simulação visual de estruturas de dados;
-   API Explorer para realizar requisições HTTP;
-   DB Lab para executar comandos SQL em bancos SQLite persistentes;
-   laboratório de Concorrência com uma tarefa em segundo plano e progresso;
-   catálogo de atividades práticas para Playground, DB Lab e API Explorer;
-   configurações persistentes, temas claro/escuro e janela Sobre o PRISMA.

### Algoritmos disponíveis

-   Busca Linear
-   Busca Binária
-   Bubble Sort
-   Selection Sort
-   Insertion Sort

### Estruturas de dados disponíveis

-   Lista
-   Pilha
-   Fila

Os laboratórios de algoritmos e estruturas de dados permitem acompanhar
a execução por etapas e reiniciar as demonstrações.

### API Explorer

-   Requisições GET, POST, PUT e DELETE.
-   Validação da URL e do corpo JSON para POST e PUT.
-   Comunicação assíncrona com `QNetworkAccessManager`.
-   Exibição do status HTTP e da resposta, com formatação de JSON.
-   Tratamento de erros de comunicação e confirmação antes de exclusões.
-   Mensagens educativas para orientar o uso.

### DB Lab — SQLite

-   Conexão com um arquivo SQLite existente ou criação de um novo banco.
-   Campo para visualizar e informar o caminho do banco.
-   Editor SQL com o mesmo `CodeEditor` utilizado no Playground.
-   Execução de comandos como CREATE TABLE, INSERT, SELECT, UPDATE e DELETE.
-   Resultados em `QTableWidget`, com nomes das colunas e registros.
-   Contagem de registros retornados ou linhas afetadas.
-   Indicadores separados para conexão e execução SQL.
-   Tratamento de erros de conexão e execução.

O banco padrão é `laboratorio.db`, armazenado no diretório de dados da
aplicação obtido por `QStandardPaths.AppLocalDataLocation`. No ambiente
Linux de desenvolvimento, o caminho padrão é:

``` text
~/.local/share/PRISMA/laboratorio.db
```

O DB Lab utiliza somente SQLite. MySQL e PostgreSQL poderão ser abordados
comparativamente no material didático. O destaque de sintaxe SQL está
adiado.

### Laboratório de Concorrência

Uma tarefa simulada de vinte segundos por padrão utiliza `QThread`
e informa o progresso por sinais do Qt. Durante a execução, é possível
navegar entre as páginas. O botão Iniciar tarefa fica desabilitado até
o término, quando uma nova execução pode ser iniciada.

O botão Cancelar solicita a interrupção cooperativa da tarefa. O progresso
permanece no último valor exibido, e uma nova execução começa em 0%.

Ao fechar a janela, a aplicação solicita a interrupção da tarefa e aguarda
seu encerramento antes de liberar os componentes.

A duração pode ser configurada entre 5 e 30 segundos, valendo para a
próxima execução.

### Atividades práticas

A tela apresenta 42 atividades, com numeração automática,
filtro por módulo, objetivo, instruções e resultado esperado. O aluno
realiza os desafios nos laboratórios; não há correção automática.

- **Playground — 26 atividades:** saída e comentários, variáveis, tipos,
  conversões, operadores, strings, condições, laços, listas, tuplas,
  dicionários, conjuntos, compreensões, funções, exceções e módulos.
- **DB Lab — 8 atividades:** criação, inserção, consulta, filtros,
  ordenação, atualização, agregação, agrupamento, exclusão e NULL.
- **API Explorer — 8 atividades:** GET, POST, PUT, DELETE, validações,
  recurso inexistente e um ciclo CRUD completo.

O catálogo fica em `src/prisma/resources/activities.json`. Cada atividade
possui `id`, `modulo`, `titulo`, `objetivo`, `instrucoes` e
`resultado_esperado`. Os módulos são `playground`, `database` e `api`.
O serviço valida o catálogo antes de disponibilizá-lo à interface.

Os dados estão separados da apresentação para permitir uma futura
integração com uma API colaborativa. Atualmente, o catálogo é local.

### Configurações e Sobre

As preferências são salvas automaticamente com `QSettings`:

- Tema claro ou escuro, definido por arquivos QSS em `styles/`.
- Fonte dos editores Playground e DB Lab, de 8 a 24 pontos.
- Duração da demonstração de concorrência, de 5 a 30 segundos.
- Caminho padrão do banco SQLite, utilizado na próxima inicialização.

Tema e fonte são aplicados imediatamente. O botão Restaurar padrões
pede confirmação; ele não exclui bancos nem atividades. Sobre o PRISMA
abre uma janela modal definida em `ui/about_dialog.ui`, carregada com
`QUiLoader`, com informações do projeto e um botão Fechar.

## Tecnologias

O projeto utiliza atualmente:

-   **Python 3.10+**
-   **PySide6**
-   **Qt Designer**
-   **Qt Widgets**
-   **QUiLoader**
-   **QStackedWidget** para navegação
-   **QNetworkAccessManager** para comunicação HTTP
-   **SQLite**, com a biblioteca padrão **sqlite3**
-   **Git**

A interface é construída visualmente no Qt Designer e carregada
dinamicamente pela aplicação, mantendo a definição visual separada da
lógica Python.

## Arquitetura

O projeto utiliza o layout `src/` e separa as principais
responsabilidades da aplicação:

``` text
PRISMA/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── src/
│   └── prisma/
│       ├── controllers/
│       ├── resources/
│       ├── services/
│       │   ├── algorithms/
│       │   ├── activities/
│       │   ├── api/
│       │   ├── concurrency/
│       │   ├── data_structures/
│       │   ├── database/
│       │   ├── playground/
│       │   └── settings/
│       ├── styles/
│       ├── ui/
│       ├── views/
│       ├── __init__.py
│       ├── __main__.py
│       └── app.py
└── tests/
```

### Responsabilidades principais

-   **`app.py`** --- inicialização e composição da aplicação.
-   **`controllers/`** --- interação entre a interface e o comportamento
    das páginas.
-   **`services/`** --- lógica e regras dos recursos da aplicação.
-   **`views/`** --- componentes visuais customizados em Python.
-   **`ui/`** --- interfaces criadas no Qt Designer.
-   **`resources/`** --- recursos utilizados pela aplicação.
-   **`styles/`** --- temas claro e escuro definidos em QSS.

O diretório `resources/` contém o catálogo JSON de atividades.
O diretório `tests/` está atualmente vazio.
O projeto ainda não possui testes automatizados.

## Instalação

Clone o repositório:

``` bash
git clone https://github.com/profmauroduarte/prisma.git
cd prisma
```

Crie um ambiente virtual:

``` bash
python3 -m venv .venv
```

Ative o ambiente no Linux/macOS:

``` bash
source .venv/bin/activate
```

Instale o projeto e suas dependências em modo editável:

``` bash
pip install -e .
```

## Executando

Com o ambiente virtual ativado:

``` bash
python -m prisma
```

## Interface com Qt Designer

O arquivo principal da interface está em:

``` text
src/prisma/ui/main_window.ui
```

Para abrir o Qt Designer a partir do ambiente do projeto:

``` bash
pyside6-designer
```

As alterações salvas no arquivo `.ui` são carregadas pela aplicação sem
a necessidade de gerar manualmente um arquivo Python com `pyside6-uic`.
O carregamento utiliza `QUiLoader`, com registro do widget personalizado
`CodeEditor`.

## Desenvolvimento

O desenvolvimento é incremental: uma etapa por vez, preservando as
funcionalidades existentes e priorizando código simples e didático.
Mudanças arquiteturais devem ser discutidas antes da implementação.
As instruções para agentes estão em [AGENTS.md](AGENTS.md).

O trabalho está organizado em trilhas:

-   **Trilha 0:** Boas-vindas, Python, ambiente e Git.
-   **Trilha 1:** Interface e Arquitetura.
-   **Trilha 2:** Design e Experiência.
-   **Trilha 3:** Lógica, Dados e Recursos.
-   **Trilha 4:** Performance e Concorrência.
-   **Trilha 5:** Finalização e Distribuição.

A aplicação utiliza QSS para os temas claro e escuro. O estudo dos estilos
visuais integra a Trilha 2, com preferências persistidas por `QSettings`.

## Status do projeto

O PRISMA está **em desenvolvimento**.

Novos módulos, recursos visuais e funcionalidades serão incorporados
progressivamente conforme a evolução do projeto e do conteúdo
educacional associado.

## Licença

A licença do projeto ainda será definida.
