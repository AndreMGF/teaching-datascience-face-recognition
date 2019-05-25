# Projeto de Reconhecimento Facial

Este é um projeto para ensino de ciência de dados. O objetivo do projeto é criar uma aplicação para reconhecimento facial usando a biblioteca `face_recognition`. Nesta aplicação é possível cadastrar `Pessoas` em uma base de reconhecimento facial e também verificar se uma pessoa está na base de dados de pessoas cadastras ou não.

## Pré-requisitos

* Cliente Git (https://git-scm.com). Verifique a instalação digitando em um terminal:
```bash
$ git --version
```

* Anaconda (https://www.anaconda.com/). Verifique a instalação digitando em um terminal:
```bash
$ conda --version
```

## Instalação

Clonar o repositório do GitHub e entrar na pasta
```bash
$ git clone https://github.com/anfer86/learning-datascience-face-recognition.git
$ cd learning-datascience-face-recognition
```

Criar o ambiente (*environment*) do conda usando o arquivo `face-recognition-spec.yml`, que contém as configurações e dependências do projeto. Além de criar o ambiente, também vamos ativá-lo
```bash
$ conda env create -n face-recognition -f face-recognition-spec.yml
$ conda activate face-recognition
```

## Utilização

Com o ambiente criado e ativo, vamos iniciar a nossa aplicação. Entramos na pasta `app/backend/` e executamos o arquivo `server.py` para deixar nossa aplicação rodando na porta `3000`.
```bash
$ cd app/backend
$ python server.py
```

Pronto. Agora tem um servidor aguardando por requisições HTTP que realiza as operações da nossa aplicação. As requisições suportadas pela aplicação são:
* `/person/add` (POST) que adiciona uma *Pessoa* à base de dados
* `/person/edit` (POST) que edita uma *Pessoa* da base de dados (em desenvolvimento)
* `/person/delete` (POST) que remove uma *Pessoa* da base de dados (em desenvolvimento)
* `/person/get` (POST) que recupera uma *Pessoa* da base de dados (em desenvolvimento)
* `/recognizer/get` (POST) que retorna uma *Pessoa* da base de dados para uma imagem enviada via POST.

Também foram desenvolvidas as páginas seguintes páginas para mostrar como ocorrem essas requisições.
* `views/person_add.html`
* `views/person_edit.html` (em desenvolvimento)
* `views/person_list.html` (em desenvolvimento)
* `views/person_get.html` (em desenvolvimento)
* `views/recognizer.html`

## Desenvolvimento

O projeto foi desenvolvido com:

* [Anaconda](https://www.anaconda.com/) - Framework de Datascience em Python
* [Sublime Text](https://www.sublimetext.com/) - Editor de texto para programação
* [face_recognition](https://github.com/ageitgey/face_recognition) - Face recognition Library by [ageitgey](https://github.com/ageitgey)

## Autores

* **Carlos Andres Ferrero** - [anfer86](https://github.com/anfer86)