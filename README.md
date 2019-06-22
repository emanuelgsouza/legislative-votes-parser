# lesgislative-votes-parser

In progress...

## O projeto

Você já entendeu como funciona a eleição para o legislativo no Brasil? Para os cargos deste poder (Deputados Federais e Estaduais e Vereadores), o sistema é conhecido como voto proporcional. Para informações mais detalhadas, convido a você a ler o texto do [Politize](https://www.politize.com.br/deputados-como-sao-eleitos/).

O objetivo deste repositório é, dado uma eleição para análise - aqui será abordado primeiro a de 2018 - gerarmos as informações para cada deputado, se o mesmo foi eleito via maioria de votos ou pelo famoso "puxadinho".

O objetivo é ser totalmente agnóstico a eleição, de maneira que comecemos com a de 2018, mas também venhamos analisar a de 2014, e assim por diante. Como objetivo final sendo de fornecer dados para outras análises ou aplicações

## Pre Requisitos

* Python >= 3.x
* pip
* virtualenv

## Instalando

Recomendamos fortemente o uso de virtualenv para criação do ambiente de desenvolvimento, para tanto, use os seguintes comandos:

```sh
# substitua o caminho do binário do python, caso necessário use o comando which python
# criando o ambiente
virtualenv --python=/usr/bin/python3 .

# ativando o ambiente
source bin/activate

# instalando as dependencias
pip install -r requirements.txt

# para desativar o ambiente
deactivate
```

## Rodando localmente o projeto

Antes de mais nada, é necessário um arquivo gerado pelo repositório do [turicas - Álvaro Justen](https://github.com/turicas). Ele tem um repositório massa, que é o [eleicoes-brasil](https://github.com/turicas/eleicoes-brasil). Através deste repositório, teremos acesso aos dados do TSE de maneira mais padronizada, e em CSV prontos para análise.

O arquivo de interesse, é o gerado pela linha de comando `python tse.py votacao-zona --years=2018`. O dataset será gerado na pasta `data/output`. Copie-o para a pasta `data/input` neste repositório.

Um outro arquivo necessário a esse projeto, foi gerado pelo notebook que se encontra em `notebooks/deputados-eleitos.ipynb`. Tal CSV será gerado por scrapping da [página da Câmara Legislativa Nacional](https://www.camara.leg.br/internet/agencia/infograficos-html5/DeputadosEleitos/index.html).

Tendo as dependencias já instaladas e os CSVs acima gerados e constando na pasta `data/input`, basta rodar o parser para JSON:

```sh
python parser-to-json.py
```

Rodando o código acima, perceba que aparecerá um arquivo em `data/output` com os JSONs já parseados e devidamente trabalhados

## Licença

Este código está licenciado sobre a licença [MIT](./LICENSE).
