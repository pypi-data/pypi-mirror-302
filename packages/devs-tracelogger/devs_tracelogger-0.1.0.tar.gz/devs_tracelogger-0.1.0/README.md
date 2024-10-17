# GrupoB Trace Logger

**GrupoB Trace Logger** é uma biblioteca Python fácil de usar para registrar exceções e enviar mensagens diretamente para um canal do Discord via Webhook. Ideal para monitorar e gerenciar erros em aplicações de forma prática, com integração automática ao Discord.

## Instalação

Instale a biblioteca usando `pip`:

```bash
pip install devs_tracelogger
```

## Como Usar

Abaixo estão exemplos de como usar a biblioteca para capturar exceções e enviar notificações ao Discord.

### Uso Básico

O exemplo a seguir mostra como criar uma instância da classe `Log` e registrar uma exceção diretamente no Discord:

```python
from devs_tracelogger import Log

try:
    marionette = Marionette()  # Exemplo de código que pode gerar uma exceção
except Exception as ex:
    log = Log(
        webhook={"id": 123456789012345678, "token": "exemploDeToken12345"},
        default_user="Gelson Júnior",  # Nome do responsável
        bot_name="Calculadora"  # Nome do robô ou serviço executando
    )
    log.register(ex)  # Registra a exceção e envia a mensagem para o Discord
```

Caso você não deseje enviar a mensagem ao Discord, defina o parâmetro `send_notification` como `False`. Por padrão, ele está definido como `True`.

### Uso com Parâmetros Dinâmicos

Os parâmetros também podem ser passados diretamente no método `register`. Quando valores são passados tanto no construtor quanto no método, os valores passados no `register` serão priorizados:

```python
from devs_tracelogger import Log

try:
    marionette = Marionette()  # Exemplo de código que pode gerar uma exceção
except Exception as ex:
    log = Log(
        webhook={"id": 123456789012345678, "token": "exemploDeToken12345"}
    )
    log.register(
        ex,
        {
            "bot_name": "Projeto Z",  # Nome do robô ou serviço
            "default_user": "Gelson Júnior"  # Nome do responsável pelo código
        }
    )
```

### Retorno

O método `register` retorna um objeto JSON contendo informações detalhadas sobre o erro e o status da mensagem enviada:

```json
{
    "status": 200,
    "data": {
        "filename": "...",
        "function": "...",
        "type_error": "...",
        "error": "...",
        "line": "...",
        "created_at": "...",
        "bot_name": "...",
        "default_user": "..."
    },
    "message": "Mensagem enviada com sucesso para o Discord"
}
```

### Parâmetros

- **webhook** (obrigatório): Um dicionário contendo o `id` e `token` do webhook do Discord.

```json
{"id": int, "token": str}
```

Esses dados podem ser obtidos diretamente no Discord em: `https://discord.com/api/webhooks/<id>/<token>`.

- **default_user** (opcional): Nome do responsável pelo robô ou código.
- **bot_name** (opcional): Nome do robô ou aplicação que está rodando.
- **send_notification** (opcional): Define se a notificação será enviada ao Discord (padrão: `True`). Se definido como `False`, apenas registrará o erro sem enviar a mensagem.

## Exemplo de Mensagem no Discord

Quando um erro é registrado, a mensagem enviada para o canal do Discord incluirá detalhes como o tipo de erro, o nome do robô e o responsável:

```
[Erro] O robô Calculadora encontrou um problema:
Exception: divisão por zero
Responsável: Gelson Júnior
```

## Contribuindo

Contribuições são sempre bem-vindas! Se encontrar algum problema ou tiver sugestões de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto é licenciado sob a licença MIT. Para mais informações, consulte o arquivo [LICENSE](LICENSE).

---

**Grupo Bachega**

