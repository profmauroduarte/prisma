# Instruções para agentes — PRISMA

## Objetivo do projeto

P.R.I.S.M.A. — Plataforma de Recursos Interativos para Simulação,
Modelagem e Aprendizagem.

Slogan: Transformando código em experiência.

O PRISMA é uma aplicação desktop educacional e um projeto integrador
para formação técnica. Permite explorar programação, algoritmos,
estruturas de dados, APIs e bancos de dados enquanto os participantes
aprendem a construir a própria aplicação.

O código também serve como material didático. Priorize clareza,
organização e soluções simples, fáceis de explicar.

## Tecnologias e arquitetura

- Python 3.10+ e PySide6 / Qt Widgets.
- Estrutura de pacote em `src/prisma/`.
- Instalação em modo editável com `pip install -e .`.
- Interfaces construídas no Qt Designer em arquivos `.ui`.
- Carregamento dinâmico das interfaces com `QUiLoader`.
- Navegação entre páginas com `QStackedWidget`.
- Comunicação HTTP com `QNetworkAccessManager`.
- Banco de dados SQLite com a biblioteca padrão `sqlite3`.

Inspecione os arquivos reais antes de propor mudanças. Não presuma
que uma descrição da estrutura substitui a implementação existente.

## Responsabilidades dos componentes

- `app.py`: inicializa a aplicação, carrega a interface, registra
  widgets personalizados e integra os componentes.
- `controllers/`: conectam ações da interface aos serviços e
  atualizam as mensagens e visualizações.
- `services/`: concentram regras de negócio, processamento e acesso
  a recursos, como APIs e bancos de dados.
- `views/`: implementam widgets personalizados, como `CodeEditor`.
- `ui/`: contém as interfaces construídas no Qt Designer.

Preserve a separação de responsabilidades nas novas implementações.
No Playground, o `PlaygroundController` cuida da interface e o
`CodeRunner` executa o código recebido como texto e retorna o resultado.
Não realize refatorações por iniciativa própria.

## Decisões a preservar

- Utilize `QUiLoader`; não converta arquivos `.ui` para Python com
  `pyside6-uic`.
- Preserve o Qt Designer como ferramenta de construção da interface.
- Altere arquivos `.ui` somente quando necessário para a tarefa.
- Não introduza QSS enquanto essa etapa não for solicitada.
  O trabalho de estilos pertence à Trilha 2.
- O DB Lab utiliza somente SQLite. Não implemente suporte a MySQL
  ou PostgreSQL sem uma nova decisão discutida com o usuário.
- Preserve o uso de `QStandardPaths.AppLocalDataLocation` para o
  diretório padrão dos bancos.
- Preserve a reutilização de `CodeEditor` no Playground e no DB Lab.
- O destaque de sintaxe SQL foi adiado. Não o implemente sem solicitação.

## Convenções de desenvolvimento

- Responda em português brasileiro.
- Siga o estilo e os padrões do módulo que estiver sendo alterado.
- Antes de modificar uma funcionalidade, consulte como os demais
  módulos resolvem necessidades semelhantes.
- Prefira soluções simples e compatíveis com a arquitetura atual.
- Evite abstrações excessivas, refatorações desnecessárias e
  alterações de formatação fora do escopo da tarefa.
- Use comentários e explicações que contribuam para a aprendizagem,
  especialmente quando o comportamento não for evidente.
- Preserve validações, tratamento de erros e mensagens educativas.
- Não implemente funcionalidades que o usuário ainda não solicitou.
- Respeite alterações locais existentes. Não as descarte nem
  sobrescreva sem autorização.

## Metodologia incremental

Trabalhe uma etapa por vez.

1. Compreenda o pedido e examine o código relacionado.
2. Explique brevemente o objetivo e o motivo da mudança.
3. Implemente somente a etapa solicitada ou combinada.
4. Faça verificações proporcionais à alteração e informe o resultado.
5. Quando houver validação manual, explique como testar.
6. Aguarde a confirmação dos testes pelo usuário antes de avançar
   para a próxima etapa.

Não agrupe várias evoluções independentes em uma única alteração.

## Preservação e decisões arquiteturais

Preserve as funcionalidades existentes de navegação, Playground,
algoritmos, estruturas de dados, API Explorer e DB Lab.

Não realize uma reestruturação geral do projeto por iniciativa própria.

Consulte o usuário antes de mudanças arquiteturais relevantes, como
alterar a divisão de responsabilidades, substituir tecnologias,
introduzir dependências estruturais ou mudar a estratégia de
carregamento da interface.

Apresente o motivo e o impacto da proposta antes de implementá-la.

## Verificação e comunicação

- Verifique os comportamentos afetados pela mudança.
- Diferencie inspeção do código, testes automatizados e testes manuais.
- Não declare que algo foi testado se apenas leu o código.
- Informe limitações ou verificações que dependam do usuário.
- Ao concluir uma etapa, resuma o que mudou e como foi verificado.
