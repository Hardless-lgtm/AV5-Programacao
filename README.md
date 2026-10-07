# Como executar o projeto

1. Clonar o repositório:
git clone https://github.com/Hardless-lgtm/AV5-Programacao.git

2. Entrar na pasta do projeto:
cd AV5-Programacao

3. Criar o arquivo .env na raiz do projeto com o conteúdo:
DB_HOST=seu_host_aqui
DB_USER=seu_usuario_aqui
DB_PASS=sua_senha_aqui
DB_PORT=12960
DB_NAME=seu_banco_aqui

4. Sincronizar as dependências:
uv sync

5. Executar a aplicação:
uv run python main.py