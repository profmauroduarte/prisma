# PRISMA

**P.R.I.S.M.A. --- Plataforma de Recursos Interativos para Simulação,
Modelagem e Aprendizagem**

> **Transformando código em experiência.**

O **PRISMA** é uma aplicação desktop educacional desenvolvida em Python
com PySide6. Seu objetivo é oferecer um ambiente visual e interativo
para explorar conceitos de programação, permitindo acompanhar
algoritmos, estruturas de dados e execução de código de forma prática.

O projeto também serve como aplicação-base para uma formação em
desenvolvimento de interfaces desktop com Python e Qt, evoluindo ao
longo do curso conforme novos conceitos são apresentados.

## Recursos atuais

Nesta etapa do desenvolvimento, o PRISMA já possui:

-   navegação entre as principais áreas da aplicação;
-   Playground para escrita e execução de código Python;
-   editor de código customizado com numeração de linhas;
-   mensagens amigáveis para erros comuns de execução;
-   visualização passo a passo de algoritmos;
-   simulação visual de estruturas de dados.

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

## Tecnologias

O projeto utiliza atualmente:

-   **Python 3.10+**
-   **PySide6**
-   **Qt Designer**
-   **Qt Widgets**
-   **QUiLoader**
-   **Git**

A interface é construída visualmente no Qt Designer e carregada
dinamicamente pela aplicação, mantendo a definição visual separada da
lógica Python.

## Arquitetura

O projeto utiliza o layout `src/` e separa as principais
responsabilidades da aplicação:

``` text
PRISMA/
├── pyproject.toml
├── src/
│   └── prisma/
│       ├── controllers/
│       ├── resources/
│       ├── services/
│       │   ├── algorithms/
│       │   ├── data_structures/
│       │   └── playground/
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
-   **`styles/`** --- estilos visuais do projeto.

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

## Status do projeto

O PRISMA está **em desenvolvimento**.

Novos módulos, recursos visuais e funcionalidades serão incorporados
progressivamente conforme a evolução do projeto e do conteúdo
educacional associado.

## Licença

A licença do projeto ainda será definida.
