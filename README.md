# Chamado Ágil

O **Chamado Ágil** é um sistema de Help Desk desenvolvido para simular um ambiente corporativo real. O foco principal deste projeto não foi apenas a interface, mas a construção de um backend robusto com regras de negócio rígidas, controle de permissões e integridade de dados.

O projeto demonstra o domínio de uma stack moderna e a capacidade de resolver problemas comuns em sistemas empresariais, como hierarquia de acesso e automação de fluxos.

##  Por que este projeto?
Diferente de um CRUD comum, o Chamado Ágil foi estruturado para validar decisões de arquitetura:
*   **Regras de Negócio no Backend:** O frontend é estritamente uma camada de visualização; toda a lógica de permissão e validação reside na API.
*   **Modelagem Relacional:** Estrutura consistente para suportar históricos de alterações e relacionamentos complexos.
*   **Segurança e Acesso:** Implementação de autenticação via JWT com controle baseado em Roles (RBAC).











##  O que o sistema faz

O **Chamado Ágil** foi projetado para resolver problemas reais de organização em help desks, indo além do básico e implementando fluxos de trabalho dinâmicos:

*   **Abertura e Acompanhamento:** Interface dedicada para clientes registrarem incidentes e monitorarem o progresso em tempo real.
*   **Gestão via Kanban:** Visualização clara do fluxo de trabalho com movimentação de status (Pendente, Em Andamento, Concluído).
*   **Hierarquia de Suporte:** Sistema de permissões que diferencia níveis de acesso entre técnicos Junior, Mid, Senior e Enginner.
*   **Reatribuição Inteligente:** Lógica de negócio que valida automaticamente se o técnico destino possui a senioridade necessária para o ticket e se ele tem disponibilidade na agenda.
**Gestão de Carga (Load Balancing):** Algoritmo que impede a sobrecarga de técnicos, limitando o recebimento a 3 tickets ativos por vez. Caso a equipe esteja com capacidade máxima, o sistema mantém novos chamados na fila de espera automaticamente.
*   **Controle de Disponibilidade (Availability):** Regra de negócio que valida o status operacional do suporte. Apenas técnicos marcados como "Ativos" podem receber atribuições, garantindo que ausências (férias, licenças ou desligamentos) não interrompam o fluxo de atendimento.
*   **Audit Trail (Rastreabilidade):** Histórico completo de todas as alterações feitas em cada chamado, garantindo transparência no atendimento.
*   **Segurança:** Autenticação e proteção de rotas implementadas com **JWT (JSON Web Token)**.

##  Desafios e Decisões de Engenharia

Minha meta foi construir uma aplicação que exigisse soluções além de um CRUD comum, focando em:

*   **Modelagem Relacional Consistente:** Estruturação de banco de dados para suportar relacionamentos complexos e integridade referencial.
*   **Arquitetura em Camadas:** Separação clara de responsabilidades entre **Rotas, Serviços e Queries**, facilitando a manutenção e a legibilidade do código.
*   **Backend-First:** Toda a inteligência e as regras de negócio residem no servidor, garantindo que o frontend não tenha autoridade sobre o fluxo de dados.
*   **Full Deployment:** Integração contínua e deploy real utilizando **Render** (API), **Vercel** (Frontend) e **Railway** (Database).









---

##  Acesso ao Sistema (Importante)
Para facilitar a avaliação técnica e o teste das diferentes regras de permissão, **este projeto não utiliza senhas**. A autenticação é realizada informando apenas o **ID do usuário** e sua respectiva **Role** (`client` ou `support`).

Essa foi uma decisão consciente para permitir que recrutadores e desenvolvedores naveguem rapidamente entre os diferentes níveis de acesso (Junior, Senior, Client) sem a fricção de criação de contas.

### Contas de Teste - Clients (role: client)
*Nota: Os clientes abaixo possuem tickets no momento.*


| ID | Nome | ID | Nome |
| :--- | :--- | :--- | :--- |
| 1 | Marcos Silva | 14 | Patrícia Gomes |
| 2 | Julia Pereira | 15 | Rodrigo Martins |
| 3 | Ricardo Alves | 17 | Bruno Cardoso |
| 4 | Fernanda Costa | 18 | Daniela Carvalho |
| 5 | Gabriel Souza | 19 | Eduardo Melo |
| 6 | Amanda Rocha | 20 | Fabiana Teixeira |
| 7 | Lucas Mendes | 32 | Simone Moraes |
| 8 | Beatriz Oliveira | 35 | Vitor Cavalcanti |
| 9 | Andre Ferreira | 38 | Yara Farias |
| 10 | Carla Santos | 39 | Zeca Moura |
| 11 | Thiago Lima | 42 | Denise Lins |
| 12 | Vanessa Ribeiro | 48 | Joana Hipólito |
| 13 | Felipe Castro | 50 | Lúcia Valente |

### Contas de Teste - Supports (role: support)


| ID | Nome | Nível | Ativo |
| :--- | :--- | :--- | :--- |
| 1 | Lucas Oliveira | junior | ✔ |
| 2 | Mariana Souza | junior | ✔ |
| 3 | Pedro Henrique | junior | ✔ |
| 4 | Ana Clara Lima | junior | ✔ |
| 5 | João Victor Silva | junior | ✔ |
| 6 | Beatriz Mendes | junior | ✖ |
| 7 | Rafael Costa | junior | ✔ |
| 8 | Carla Ferreira | mid_level | ✔ |
| 9 | Diego Santos | mid_level | ✔ |
| 10 | Fernanda Rocha | mid_level | ✔ |
| 11 | Gabriel Alves | mid_level | ✔ |
| 12 | Ricardo Gomes | senior | ✔ |
| 13 | Patrícia Ribeiro | senior | ✔ |
| 14 | Thiago Martins | senior | ✖ |
| 15 | Helena Castro | engineer | ✔ |

---

##  Regras de Permissão
O sistema aplica restrições baseadas na senioridade do técnico:

*   **Client:** Cria chamados e visualiza apenas o seu próprio histórico.
*   **Support Junior / Mid Level:** Alteram o status apenas de tickets que já estão atribuídos a eles. Não possuem permissão para reatribuir chamados.
*   **Support Senior / Engineer:** Controle total. Podem reatribuir tickets e alterar qualquer status.
    *   *Regra de Ouro:* Uma reatribuição só é aceita pelo backend se o nível do técnico for compatível com a exigência do ticket e se ele tiver menos de 3 chamados em aberto.


---

###  Tecnologias e Infraestrutura
**Backend:** Python (FastAPI), PyMySQL, JWT, Uvicorn.  
**Frontend:** React, Vite, Axios, React Router.  
**Banco de Dados:** MySQL hospedado no Railway.  
**Deploy:** Render (API) e Vercel (Frontend).


---

### Execução Local

**Backend:**
```bash
python -m venv venv
# Windows: venv\Scripts\activate | Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

**Frontend:**
```
bash

cd chamados_web
npm install
npm run dev
```
---

###  Links e Contato
Aplicação Online: Vercel App
Documentação API: Swagger UI
Desenvolvedor: Carlos Matheus

---

### Nota do Desenvolvedor
Este projeto marca minha consolidação no desenvolvimento backend profissional. O maior desafio técnico foi estruturar as regras de reatribuição e controle de permissões de forma consistente no backend, garantindo que o frontend nunca tivesse autoridade sobre a regra de negócio. A separação de responsabilidades (rotas, serviços e queries) foi mantida para facilitar a manutenção e testes futuros.