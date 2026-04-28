## Como rodar o projeto

### Versão das tecnologias utilizadas:

**Python: v3.10.19**
**uv: v0.9.15**

Clone o repositório
```
git clone https://github.com/williamdev20/chec-ai-backend.git
cd chec-ai-backend
```

Instale as dependências

```
uv sync
```

> [!WARNING]
> ATENÇÃO: é preciso ter o Python3.10 e o uv instalado em sua máquina

Configure as variáveis de ambiente

```
cp .env.example .env

# Entre no .env e preencha as variáveis
API_KEY=change-me
SERPER_API_KEY=change-me
GROQ_API_KEY=change-me
```

Rode o projeto

```
uv run uvicorn app.main:app --reload --port 8080
```

Acesse http://localhost:8080/docs