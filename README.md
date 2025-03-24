# EasyDash

O **EasyDash** é uma aplicação de dashboard interativo construída com **Streamlit** e **Pandas** para análise de dados.

## Como Rodar o Projeto

### 1. Criar e Ativar o Ambiente Virtual

Antes de rodar o projeto, é recomendável criar um ambiente virtual para garantir que as dependências sejam instaladas de forma isolada.

**Para criar o ambiente virtual**:
```bash
python -m venv venv
```

**Para ativar o ambiente virtual**:

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

### 2. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências necessárias usando o `pip`:

```bash
pip install -r requirements.txt
```

### 3. Rodar o Projeto

Para rodar o projeto, utilize o comando:

```bash
streamlit run main.py
```

Isso abrirá a aplicação no seu navegador, onde você poderá interagir com o dashboard e visualizar os gráficos gerados.

## Sobre o Projeto

O **EasyDash** permite que os usuários escolham entre diferentes tipos de análises de dados, como:

- Distribuição de Compras por Usuário
- Tendência de Gasto por Usuário
- Impacto por % de Desconto nas Vendas
- Produtos Mais Comprados (Usuários com 2+ Compras)

A interface interativa foi construída com o **Streamlit**, e os gráficos são gerados utilizando a biblioteca **Matplotlib** para visualização de dados.

## Dependências

As dependências principais do projeto são:

- `streamlit`: Para criar a interface web interativa.
- `pandas`: Para manipulação e análise de dados.
- `matplotlib`: Para geração dos gráficos.

As versões específicas dessas bibliotecas estão listadas no arquivo `requirements.txt`.