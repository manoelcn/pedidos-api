# pedidos-api
Esta é uma API REST desenvolvida com FASTAPI para a gestão de pedidos. O projeto utiliza SQLAlchemy como ORM, Alembic para migrações de base de dados e JWT para autenticação segura.

## Como instalar e rodar
**Passo a passo**
1. Clone o repositório
```
git clone https://github.com/manoelcn/pedidos-api.git
```
2. Crie e ative um ambiente virtual:
```
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/macOS:
source .venv/bin/activate
```
3. Instale as dependências:
```
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente: Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
```
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=algoritmo_de_criptografia
ACCESS_TOKEN_EXPIRE_MINUTES=tempo_para_expirar_o_token
```
5. Execute as migrações da base de dados:
```
alembic upgrade head
```
6. Inicie o servidor:
```
uvicorn main:app --reload
```
A API estará disponível em `http://127.0.0.1:8000`.

## Documentação da API
Após iniciar o servidor, você pode acessar a documentação interativa nos seguintes endereços:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **Redoc:** `http://127.0.0.1:8000/redoc`

## Estrutura  do projeto
- `main.py`: Ponto de entrada da aplicação e configuração do FastAPI.
- `models.py`: Definição das tabelas da base de dados.
- `schemas.py`: Modelos Pydantic para validação de entrada e saída de dados.
- `auth_routes.py`: Endpoints relacionados com autenticação e criação de conta.
- `order_routes.py`: Endpoints para gestão de pedidos e itens.
- `dependencies.py`: Funções de dependência, como a sessão da base de dados e verificação de token.