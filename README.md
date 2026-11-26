# Simulador Turing Airlines

Este projeto contém o simulador em Python para testar as Máquinas de Turing projetadas para resolver o problema dos horários de voos com conexão da **Turing Airlines**.

O simulador testa e gera o traço de execução (fita passo a passo) para as duas variações projetadas:
- **MT1**: Máquina de Turing padrão de fita única (determinística).
- **MT2**: Variação da Máquina de Turing com 2 fitas.

## Requisitos
O projeto não possui nenhuma dependência externa. Basta ter o **Python 3** instalado.

## Estrutura do Projeto
- `tm.py`: Contém a definição formal das máquinas, estados, alfabeto, funções de transição e o núcleo de simulação das fitas.
- `test.py`: Rotina de bateria de testes extensiva. Compara a execução das máquinas com a fórmula matemática em mais de 17.000 entradas geradas aleatoriamente e em casos de borda extremos.
- `demo.py`: Executa uma entrada de fita específica e exibe no terminal a fita e os estados passo a passo para ambas máquinas.

## Como Utilizar

### 1. Rodar os Testes Extensos (Verificação de Correção)
Para comprovar que as máquinas funcionam para qualquer caso, execute:
```bash
python test.py
```
*Isto irá validar os Exemplos 1 e 2 do enunciado e rodar a bateria de testes.*

### 2. Simular uma Fita Customizada (Passo a Passo)
Para ver as máquinas trabalhando em tempo real, use o arquivo `demo.py` passando a entrada codificada como argumento.

```bash
python demo.py "L####1|#"
```
*Se executado sem argumentos (`python demo.py`), ele rodará automaticamente o exemplo mínimo presente no relatório.*

### Entendendo a Codificação da Entrada
A entrada na fita deve respeitar o formato criado no projeto (unário) para representar os horários de voos e conexões. A codificação é a seguinte:
`[Origem] # [Hub] # [Destino] # [h0] # [d1] | [w] # [d2]`

Onde:
- **Origem, Hub, Destino**: Letra `L` ou `O` repetida a cada 15º de longitude (Ex: `OOO` = 45º Oeste). Se for 0º, deixa vazio.
- **h0**: Hora de partida, usando o símbolo `p` (Ex: `ppp` = 03h).
- **d1, w, d2**: Durações, usando o símbolo `1` (Ex: `11` = 2 horas).
- **#**: Separador de campos
- **|**: Marca especial de chegada ao hub (no lugar do separador após `d1`).
