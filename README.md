# NewsBOT

[![My Skills](https://skillicons.dev/icons?i=discord, py, git)](https://skillicons.dev)

NewsBOT é um projeto que começou com o curso de Python da plataforma Codedéx. Inicialmente, foi desenvolvido um BOT para o Discord que enviava uma imagem engraçada para o usuário quando solicitado. O projeto foi aprimorado e agora está se encaminhando para a criação de um BOT utilitário para o Discord.

## Funcionalidades

O NewsBOT oferece as seguintes funcionalidades:

- **Boas-vindas:**
  - 'Olá, eu sou o NewsBOT! :smile:'
  - 'Estou aqui para te ajudar com algumas coisas.'

- **Lista de comandos disponíveis:**
  - `$info <termo>` - Mostra informações sobre o termo pesquisado. Fonte: Wikipédia.
  - `$news <termo>` - Mostra as últimas notícias sobre o termo pesquisado. :newspaper2:
  - `$cotacao` - Mostra a cotação atual do dólar. :moneybag:
  - `$conversao <quantidade> <moeda_origem> <moeda_destino>` - Converte a quantidade de uma moeda para outra. :moneybag:
  - `$qrcode <link>` - Mostra o QR Code do link fornecido.
  - `$clima <cidade>` - Mostra o clima atual da cidade. :white_sun_rain_cloud:

## Status do Projeto

O projeto ainda está em fase de desenvolvimento e atualmente só roda localmente.

## Como Executar Localmente

Para executar o NewsBOT localmente, siga os seguintes passos:

1. Clone o repositório:
    ```sh
    git clone <URL_DO_REPOSITORIO>
    ```
2. Navegue até o diretório do projeto:
    ```sh
    cd NewsBOT
    ```
3. Instale as dependências necessárias:
    ```sh
    pip install -r requirements.txt
    ```
4. Configure o token do seu BOT no arquivo de configuração (config.json ou .env):
    ```json
    {
      "TOKEN": "SEU_DISCORD_BOT_TOKEN"
    }
    ```
5. Execute o BOT:
    ```sh
    python bot.py
    ```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorar o NewsBOT.

---

Feito com ❤️ pela equipe NewsBOT (AlanthiasCO)