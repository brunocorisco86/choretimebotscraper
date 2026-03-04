# ChoreTime Data Scraper

Este projeto é um scraper de dados para aviários ChoreTime, desenvolvido em Python com Selenium, SQLAlchemy, e orquestrado via Docker. Ele coleta dados de temperatura, umidade, amônia, idade, consumo de água e pressão estática dos aviários, armazena-os em um banco de dados SQLite local e, opcionalmente, os transfere para um PostgreSQL externo. Além disso, envia alertas via Telegram em caso de falhas.

## Estrutura do Projeto

```
chore_scraper/
├── app/
│   ├── __init__.py
│   ├── config.py       # Configurações e variáveis de ambiente
│   ├── database.py     # Modelagem de dados e funções de persistência (SQLite/PostgreSQL)
│   ├── scraper.py      # Lógica de scraping com Selenium
│   ├── notifier.py     # Funções para envio de notificações (Telegram)
│   └── main.py         # Lógica principal, agendamento de tarefas (scraper, transferência, relatórios)
├── .env                # Variáveis de ambiente (credenciais, tokens)
├── Dockerfile          # Definição da imagem Docker
├── docker-compose.yml  # Orquestração dos serviços Docker
├── requirements.txt    # Dependências Python
└── README.md           # Este arquivo
```

## Configuração

1.  **Variáveis de Ambiente:**
    Renomeie o arquivo `.env.example` para `.env` e preencha as variáveis de ambiente necessárias, seguindo o padrão fornecido no `.env.example`.

2.  **XPaths no `scraper.py`:**
    Os XPaths para extração dos dados no arquivo `app/scraper.py` foram baseados nas informações fornecidas. É **crucial** que você os verifique e ajuste, se necessário, inspecionando os elementos na página web do ChoreTime usando as ferramentas de desenvolvedor do seu navegador. O site pode ter alterações que invalidem os XPaths atuais.

## Deployment com Docker

Para rodar o projeto usando Docker, siga os passos:

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd chore_scraper
    ```

2.  **Crie o arquivo `.env`** (conforme descrito acima).

3.  **Construa e execute os containers Docker:**
    ```bash
    docker-compose up --build -d
    ```
    *   `--build`: Constrói a imagem Docker (necessário na primeira vez ou após alterações no `Dockerfile`).
    *   `-d`: Executa os containers em modo detached (em segundo plano).

## Agendamento de Tarefas

As tarefas são agendadas internamente pelo `main.py` usando a biblioteca `schedule`:

*   **Scraping e Salvamento (SQLite):** A cada 10 minutos.
*   **Transferência para PostgreSQL:** A cada 4 horas (se `PG_URI` estiver configurado).
*   **Relatório Semanal (CSV):** Toda segunda-feira às 08:00 (funcionalidade de geração e envio de CSV precisa ser implementada no `main.py` e `database.py`).

## Limpeza de Logs e Dados

*   **Limpeza de Logs:** A limpeza de logs semanais via cron não foi implementada diretamente no código Python, mas pode ser configurada no sistema operacional do Raspberry Pi. Exemplo de entrada no `crontab -e`:
    ```cron
    0 0 * * 0 find /app/data/logs -type f -name "*.log" -mtime +7 -delete
    ```
    (Assumindo que os logs são salvos em `/app/data/logs`)

*   **Limpeza de Dados SQLite:** A limpeza de dados antigos do SQLite após a transferência para o PostgreSQL pode ser ativada descomentando as linhas relevantes na função `transfer_to_postgresql` em `app/database.py`.

## Monitoramento de Offline e Alertas

O sistema envia alertas via Telegram se o login falhar ou se houver problemas na coleta de dados de um aviário. A detecção de "offline" por 30 minutos sem comunicação pode ser implementada com um mecanismo de *heartbeat* e um monitor externo, ou estendendo a lógica de `main.py` para verificar a última vez que os dados foram coletados com sucesso.

## Desenvolvimento Futuro

*   **Geração de Lote:** A funcionalidade para criar lote, data de alojamento e abate para definir a idade do lote pode ser adicionada como uma interface web (ex: Streamlit) ou um script Python separado que atualiza uma tabela de configuração.
*   **Relatórios:** Implementar a geração de relatórios diários e o envio de CSVs por e-mail.
*   **Configuração de Aviários:** Mover a lista de `aviaries_to_monitor` para um arquivo de configuração (JSON/YAML) ou banco de dados para facilitar a adição/remoção de aviários sem alterar o código.

---

**Autor:** Manus AI
**Data:** 04 de Março de 2026
