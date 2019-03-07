# lesgislative-votes-parser

In progress...

## O projeto

Você já entendeu como funciona a eleição para o legislativo no Brasil? Para os cargos deste poder (Deputados Federais e Estaduais e Vereadores), o sistema é o do voto proporcional. Para informações mais detalhadas, convido a você a ler o texto do [Politize](https://www.politize.com.br/deputados-como-sao-eleitos/).

O objetivo deste repositório é, dado uma eleição para análise - aqui será abordada primeiro a de 2018 - gerarmos as informações para cada deputado, se o mesmo foi eleito via maioria de votos ou pelo famoso "puxadinho".

O objetivo é ser totalmente agnóstico a eleição, de maneira que comecemos com a de 2018, mas também venhamos analisar a de 2014, e assim por diante. Como objetivo final sendo de fornecer dados para outras análises ou aplicações

## Como rodar o projeto

Antes de mais nada, é necessário um arquivo gerado pelo repositório do turicas. Mas porque usar este arquivo? Haja vista os problemas de formatação dos dados do TSE, tal repositório visa resolver. Sendo assim, teremos os dados limpinhos e prontos para serem consumidos. Por isso desde já, o meu agradecimento.

O arquivo de interesse, é o gerado pela linha de comando `python tse.py votacao-zona --years=2018`. Com o dataset gerado, copie-o para a pasta `data/input`

Um outro arquivo necessário a esse projeto, foi gerado pelo notebook que se encontra em `notebooks/deputados-eleitos.ipynb`. Tal CSV será gerado por scrapping da [página da Câmara Legislativa Nacional](https://www.camara.leg.br/internet/agencia/infograficos-html5/DeputadosEleitos/index.html).

## A API

O JSON de dados gerado pelo script `parser-to-json.py` é lido na API no repositório [legislative-votes-api](https://github.com/emanuelgsouza/legislative-votes-api). Em breve teremos uma aplicação web :)
