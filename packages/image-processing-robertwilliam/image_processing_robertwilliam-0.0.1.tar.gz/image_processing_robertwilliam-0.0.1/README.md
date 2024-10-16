# Projeto: Pacote de Processamento de Imagens

## Autora Original: Karina Kato  
### Desafio de Projeto - Digital Innovation One  
[Veja meu perfil na plataforma](https://www.dio.me/users/rwilliam634)

#### Tecnologia Utilizada: Python  

---

## Descrição

O pacote **image_processing** oferece diversas funcionalidades para manipulação e análise de imagens, distribuídas em dois módulos principais:

### Módulo "Processing":
- Correspondência de histograma (histogram matching);
- Similaridade estrutural entre imagens (structural similarity);
- Redimensionamento de imagens (resize).

### Módulo "Utils":
- Leitura de imagens (read);
- Salvamento de imagens (save);
- Exibição de imagens (plot);
- Geração de gráficos (plot results);
- Plotagem de histogramas (plot histogram).

---

## Como Configurar e Hospedar um Pacote no Test PyPi

### 1. Instalar Dependências

Certifique-se de ter as versões mais recentes de `setuptools` e `wheel` instaladas:

```bash
py -m pip install --user --upgrade setuptools wheel
```

### 2. Construir o Pacote

Certifique-se de que você está no diretório onde o arquivo `setup.py` está localizado, e execute:

```bash
py setup.py sdist bdist_wheel
```

Após a execução, os seguintes diretórios devem ser gerados:
- `build/`
- `dist/`
- `image-processing-nome.egg-info/`

### 3. Subir o Pacote para o Test PyPi

Utilize o Twine para fazer o upload dos arquivos gerados no passo anterior para o Test PyPi:

```bash
py -m twine upload --repository testpypi dist/*
```

Você será solicitado a fornecer suas credenciais de login do Test PyPi. Após isso, o pacote será hospedado no ambiente de testes.

> **Nota**: O Test PyPi é um ambiente de testes. Para que o pacote esteja disponível publicamente, você precisará hospedá-lo no PyPi oficial.


### Aqui o objetivo não é utilizar o projeto da Karina para postar em meu perfil do Pypi pessoal, visto que o projeto é dela. Ainda não tenho nenhum projeto que possa ser utilizado como pacote.

### No entanto, tenha em mente que o Test Pypi, como o próprio nome diz, é apenas um ambiente de testes. Para que o projeto esteja disponível como um pacote para ser usado publicamente, é necessário hospedá-lo no site oficial do Pypi.
---

## Instalação Local Após Hospedagem no Test PyPi

### 1. Instalar Dependências

Para instalar as dependências do projeto:

```bash
pip install -r requirements.txt
```

### 2. Instalar o Pacote

Para instalar o pacote a partir do Test PyPi:

```bash
pip install -i https://test.pypi.org/simple/image-processing-robertwilliam
```

---

## Como Usar o Pacote em Qualquer Projeto

Aqui está um exemplo de como utilizar o pacote no seu projeto:

```python
from image_processing.processing import combination
combination.find_difference(image1, image2)
```

---

## Autor(a) do Pacote no Test PyPi

- **Robert William**

---

## Licença

Este projeto está licenciado sob os termos da [Licença MIT](https://choosealicense.com/licenses/mit/).