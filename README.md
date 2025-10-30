# Fintual Challenge


https://github.com/user-attachments/assets/0d16ba32-6109-4bab-98a9-c339c6040689


Portfolio con stocks, aplicando rebalance strategy.

## Requisitos:

- Python 3.13
- Instalar [uv como package manager](https://docs.astral.sh/uv/#installation)

```bash
# En macOs o Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instalacion

Clonar el repositorio o [ver en Replit](https://replit.com/@vicentematus/fintual-challenge-1?v=1)

```
git clone https://github.com/vicentematus/fintual-challenge.git
cd fintual-challenge
```

Instalar dependencias con uv

```bash
uv sync

# Activar enviroment. Si tienes zsh
source .venv/bin/activate

# Si tienes fish
source .venv/bin/activate.fish
```

Para iniciar el portafolio y ver que acciones vender/comprar:

```
uv run src/challenge.py
```

Para correr los tests con distintos escenarios

```python
uv run pytest -v
```

> [!TIP]
> El entrypoint del programa es el archivo `challenge.py`

## Estructura

### Stock

Un stock representa la accion de una empresa[^1].

```python
class Stock(BaseModel):
    symbol: StockSymbol
    name: str
    price: float
```

Cada Stock es representado por un Symbol[^2].

```Python
StockSymbol = Literal["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META"]
```

Para instanciar un Stock

```python
Stock(symbol="META", name="Meta Platforms, Inc.", price=234.22)
```

### Share

Un share es la cantidad de acciones que tiene una persona de un stock.[^3]

### Allocation

Es el porcentaje de distribucion de un Stock que apunta tener un Portfolio.

Se representa como un dictionary, en el cual la key es el StockSymbol. El value representa el porcentaje.

```python
Allocation = dict[StockSymbol, float]
```

El portafolio tiene `allocations` que representa cuanto porcentaje de stocks quiere tener un usuario.

Por ejemplo el portafolio apunta a tener 70% de acciones en META, y 30% en AAPL

```python
class Portfolio:
    allocations = {
        "META": 0.7,
        "AAPL": 0.3
    }
```

Ejemplo de asignar 70% para el Stock de Meta en el Portafolio

```python
portfolio.add_allocation("META", 0.7)
```

### Holdings

Holding es la cantidad de shares que tiene una persona en un Stock.[^4]

Se representa como un dictionary, en el cual el key es el StockSymbol. El value es la cantidad de shares

```python
Holding = dict[StockSymbol, int]
```

El portafolio tiene `Holdings`, que representan los shares que tiene un usuario.

Por ejemplo tengo 25 `shares` de `META`, y 4 de `AAPL`

```python
class Portfolio:
    holdings = {
        "META": 25,
        "AAPL": 4
    }
```

### Portfolio

Un portafolio representa una coleccion de stocks que un usuario posee.

El portafolio agrupa:

- **Stocks**: Los stocks disponibles y sus precios.
- **Holdings**: La cantidad de shares que tiene cada stock.
- **Allocation**: El porcentaje objetivo que el usuario quiere de cada stock.

```python
class Portfolio:
    stocks: Stocks
    allocations: Allocation
    holdings: Holding
```

### Rebalance

El rebalance es el proceso de ajustar el portafolio en base a porcentajes deseados de ciertos stocks.

Si quiero apuntar que mi portafolio sea 70% META, Y 30% AAPL, debo ajustar mi portafolio vendiendo o comprando las acciones que ya tengo para llegar a ese objetivo.

El algoritmo esta en el metodo `_calculate_rebalance` del `portfolio.py`.

El resultado de `rebalance` me devuelve un listado de que acciones deberia vender o comprar, especificando el monto.

```python
class Rebalance(BaseModel):
    action: RebalanceAction
    symbol: StockSymbol
    amount: float
```

Cada action me dice si deberia vender, comprar o mantener.

```python
class RebalanceAction(Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
```

Por ejemplo, si mi portafolio tiene:

```
Al dia de hoy:
- META vale 100 por cada share
- AAPL vale 100 por cada share

Mi portafolio tiene el total de 10_000. Se compone de:
5_000 de META
5_000 de AAPL

Mi objetivo (allocation) es tener
40%  de META
60% de AAPL

Cuando rebalancee, deberia devolverme:
- Vende 1000 de META
- Compra 1000 de AAPL
```

El resultado de rebalance se veria asi:

```python
result = portfolio.rebalance()

# Cuanto tienes que vender
print(result.to_sell)
[
    RebalanceAction(
        action=RebalanceAction.SELL,
        symbol="META",
        amount=1000,
    )
]

# Cuanto tienes que comprar
print(result.to_buy)
[
    RebalanceAction(
        action=RebalanceAction.BUY,
        symbol="AAPL",
        amount=1000,
    )
]
```

En `test_portfolio_rebalance.py` hay ejemplos de mas escenarios.

## Chats con LLMs

Le pregunte a Claude por conceptos de alto nivel. Por ejemplo, que es un stock, que es un reallocation strategy, que significa tener shares.

Tambien agregue Claude como co-autor en los commits que me ayudo con la implementacion.

### Sobre el rebalance strategy

Para el rebalance strategy le pregunte a Claude que me explicara https://claude.ai/share/33dbc0de-3325-4837-b6fe-7a375a922d6b https://claude.ai/share/4daa155a-922c-4bd1-b6e7-4e6bcd709dc0

Para entenderlo mejor, la logica de rebalance la hice a mano en un cuaderno, y despues lo escribi en el codigo probandolo con los casos de tests.

En base al escenario que me paso Claude, se lo pase a Claude Code para ayudarme a escribir el test de rebalance (aplique ""TDD"" para saber el output final del rebalance). Cuando escribi el test le promptee especificamente en que se enfocara en que acciones deberia comprar o vender en base a un escenario.

## Supuestos

- Definiciones de Holdings, Allocations.
- Holdings y Allocations usan el mismo key de StockSymbol, pero lo unico diferencia es el value: int/float. Es valido tener 0.xx shares de un Stock. Lo deje como int en el codigo. Aun que semanticamente son distintos.

## Pensamientos

- Un portfolio consiste de una serie de stocks. Cada stock existen tantos shares dentro de un portfolio?
- Dudas de como tipar Allocations, como un dictionary?
- Debria instanciar el portfolio de una vez con sus allocations correspondientes?
- Allocations debe ser un dictionary si <STOCK_SYMBOL> , percentage. Las operaciones con dictionaries son raras, le pido al LLM que me ayude.
- Stocks originalmente lo pienso como un <array>, pero puede ser tambien un diccionario. Todo nace en base a de un <STOCK_SYMBOL>. Se comparte harto la interfaz de STOCK_SYMBOL.
- Para los tests le pido a Claude que me ayude en base a un escenario de reallocation strategy. Asi verifico que el algoritmo funcione con distintos escenarios.

## Observaciones

- Hay manejo de excepciones.
- Hay validaciones en algunos casos, como no agregar shares negativos, o asignar un porcentaje de un stock que no existe(?).

## Validaciones que quedaron afuera

- No se puede allocar un stock que no existe en un portfolio (?)
- Rebalance de Stocks que no existen?

[^1]: [Stock Investopedia](https://www.investopedia.com/terms/s/stock.asp)
[^2]: [Ticker Symbol - Wikipedia](https://en.wikipedia.org/wiki/Ticker_symbol)
[^3]: [Share - Wikipedia](<https://en.wikipedia.org/wiki/Share_(finance)>)
[^4]: [Holding Investopedia](https://www.investopedia.com/terms/h/holdings.asp)
