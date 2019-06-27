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

## Dependências

### Dados eleitorais por candidato

Antes de mais nada, é necessário um arquivo gerado pelo repositório do [turicas - Álvaro Justen](https://github.com/turicas). Ele tem um repositório massa, que é o [eleicoes-brasil](https://github.com/turicas/eleicoes-brasil). Através deste repositório, teremos acesso aos dados do TSE de maneira mais padronizada, e em CSV prontos para análise.

Execute a extração com:

```sh
# não esqueça de estar em um ambiente virtual com virtualenv e já tenha instalado as dependências
python tse.py votacao-zona --years=2018
```

O arquivo resultante compactado estará na pasta `data/output`. Extraia o conteúdo dele em `data/input` neste repositório.

### Dados eleitorais por partido

Após a geração de dados acima, será necessário termos os dados consolidados por partido. Para tanto, criou-se um [fork](https://github.com/emanuelgsouza/eleicoes-brasil) do projeto de Turicas, para a extração os dados por partido do TSE. (Pull request em breve...)

Para tanto, siga as mesmas instruções do repositório do turicas, mas com a linha de comando de extração diferente, como a seguir:

```sh
# não esqueça de estar em um ambiente virtual com virtualenv e já tenha instalado as dependências
python tse.py votacao-partido-zona --years=2018
```

### Lista de deputados eleitos

A lista de deputados eleitos, por Estado, você encontra na [página da Câmara Legislativa Nacional](https://www.camara.leg.br/internet/agencia/infograficos-html5/DeputadosEleitos/index.html). Não será necessário extrair esses dados, pois isso já foi feito no notebook `notebooks/deputados-eleitos.ipynb`, e colocado na pasta `data/output/deputados_eleitos.csv`.

## Rodando localmente o projeto

Tendo as dependencias já instaladas e os CSVs acima gerados e constando na pasta `data/input`, será necessário extrair consolidar os dados dos CSVs, com o comando:

```sh
# não esqueça do ambiente virtual
python consolidate.py
```

**Atenção**: em minha máquina, com 12GB de RAM e um Intell i5, o script acima consumiu toda a memória para fazer a extração, pois o Pandas, por padrão, traz todos os dados para a memória e um dos CSVs do TSE possui cerca de 2.8 GB de tamanho. Atenção a execução desse script.

Tendo finalizado a consolidação, para transformar os dados para JSON, execute o comando:

```sh
# não esqueça do ambiente virtual
python generate.py
```

O comando acima irá gerar um arquivo `data.json` em `data/output`. Este arquivo já trará os dados consolidados por eleição.

Para fazer o split do arquivo acima em cada estado, use o comando:

```sh
# não esqueça do ambiente virtual
python generate-state-jsons.py
```

Ele vai gerar a seguinte estrutura em `data/output`:

```sh
elections/
  - elections.json # arquivo com o dado da eleição
  - 2018/ # para cada estado, um JSON com os dados da eleição
    - ac.json
    - rj.json
    ...
```

Também é possível gerar arquivos para cada uma das entidades do projeto, a saber:

* Eleição
* Estado
* Coligação
* Partido
* Candidato

Para tanto, é necessário executar o comando:

```sh
# não esqueça do ambiente virtual
python generate-entities.py
```

Ele terá como output a criação de uma pasta em `data/output/entities`, com os JSONs para as respectivas entidades.

Por fim, ainda é possível salvar os dados de `data.json` para um banco de dados Postgres. Para tanto, certifique-se que os dados de conexão no arquivo parser-data-to-sql.py estão corretas e as tabelas também estão criadas. Com o banco de dados de pé, execute o comando abaixo:

```sh
# não esqueça do ambiente virtual
python parser-data-to-sql.py
```

## Fazendo o upload para o Firestore

Antes de mais nada, é necessário ter o pacote firebase-admin instalado, para tanto, execute:

```sh
# não esqueça do ambiente virtual
pip install firebase-admin
```

Para fazer o upload das entidades geradas pelo script `generate-entity.py` para o Firestore do Firebase, certifique-se de ter um arquivo firebase.json na raiz desse repositório. Este arquivo será gerado pelo Firebase quando solicitado para gerar as permissões de Firebase Admin SDK. Após isso, é só executar o comando abaixo:

```sh
# não esqueça do ambiente virtual
python upload-firebase.py
```

Ele vai iterar sobre cada uma das entidades e salvando no Firestore, com cada entidade sendo uma *collection*.

## Licença

Este código está licenciado sobre a licença [MIT](./LICENSE).
