# URL site
https://www.choretronicswebservices.com/

Usuario: Junior
Senha: Junior1281

#Aviario 1282
https://www.choretronicswebservices.com/connect/00b6f4c3-d40f-1a6f-5f74-b779a048f4f5/2/CurrentConditions
#Aviario 1283
https://www.choretronicswebservices.com/connect/00b6f4c3-d40f-1a6f-5f74-b779a048f4f5/3/CurrentConditions
 
# Stack
## Hardware
- Raspberry Pi 3B com dietpi

## Software    
- Docker
    - Postgres
    - Python
    - Sqlite
    

# Premissas:

-Criar um scraper em python
    Rodar no cron a cada 10 minutos
        Prever lentidao na atualizacaoo dos dados
    Salvar em sqlite
        Aviario + Timestamp UNIQUE
    Verbosidade com salvamento em log dos eventos
- Prever a limpeza dos logs semanal via cron


- Dados a serem colhidos pelo scraper (com xpath): Temperatura, Umidade, Amonia, Idade, Quantidade de Água Consumida, Pressão Estatica
    - temperatura {/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[1]/div/div[1]/button/span/div/div/text()[1]}
    - Umidade {/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[2]/div[2]/div/div[5]/span
    - Amonia {/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[2]/div[2]/div/div[14]/span/text())
    - Idade {/html/body/div[2]/span[2]/text()[3]}
    - Quantidade de Água Consumida {/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[1]/div/div[2]/button/span/div/div/text()[1]}
    - Pressão Estatica {/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/span}


- Deverá haver um codigo python para registar o numero do aviario e link para o scraping para que possa ser replicado em outro docker caso seja preciso, registrar em uma tabela em sqlite
- Transferir (commit dados) do Sqlite para o Postgresql (em um disco externo - pendrive) a cada 4 horas (rodando em docker)
- O Postgresql devera prever salvar em sandbox ou em um endpoint externo (mqtt ou mesmo postgres) a cada 12 horas

- Enviar os dados na forma de .csv (select dos dados da ultima semana) no inicio da semana as 8 da manha, por script python rodando em cron

Criar um codigo para analisar se está offline
    Sem comunicacao por 30 minutos
    Enviar por email
    Enviar por telegram

Relatorio Diario
    Inicio do dia
    Final da Tarde
    
Criar um codigo em python para criar o lote, data de alojamento e abate
    para definir a idade do lote

