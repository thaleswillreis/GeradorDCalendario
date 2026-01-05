# Gerador Multiformato de Arquivos de Tabelas Dimensão de Data

Este projeto parte da necessidade de gerar arquivos contendo Tabelas Dimensão de Data para cerem utilizadas em diferentes projetos de Business Intelligence e compatíveis com diferentes ferramentas de BI e contendo diferentes granularidades de valores de tempo, concebidos a partir cálculos matemáticos testados e obedecendo as legislações estaduais e federais vigentes que regulamentam feriados e dias úteis no Brasil.

O resultado final é um software capaz de ser rodado em nuvem ou local, que gera **Tabelas Dimensão de Data** em diferentes formatos de arquivos e permite a inclusão de feriados estaduais e federais de forma dinâmica a partir de uma interface gráfica simples e funcional.

## Objetivo do Projeto

Oferecer um software capaz de:

- Gerar arquivos para serem utilizados como Tabelas Dimensão de Data nos formatos mais populares do mercado;  
- Oferecer ao usuário a opção de customizar o arquivo a ser gerado em relação ao formato e conteúdo;
- Ser executado stand alone ou na nuvem;
- Oferecer pré-visualização antes de fazer o download dos arquivos gerados;
- Ser facilmente reproduzível, copiável, adaptável ou modificável.

## Tipos de Arquivos de Saída

**Os seguintes formatos de arquivos de saída são suportados:** 

- Arquivo de dados no formato texto (`.csv`);
- Arquivo de planilhas do Microsoft Excel (`.xlsx`);
- Arquivo de dados no formato JSON (*JavaScript Object Notation*) (`.json`);
- Arquivo de script executável SQL (`.sql`).


## Estrutura do Dataset Final
 

| Coluna | Descrição | Formato | Exemplo |
|------|----------|----------|----------|
| `Data` | Data no formato ISO 8601 ("yyyy-MM-ddTHH:mm:ssZ") | Date | 2025-12-31 00:00:00 |
| `Ano` | Ano numérico com quatro dígitos | Int | 2025 |
| `Mes` | Mês numérico com dois dígitos | Int | 12 |
| `Dia` | Dia numérico com dois dígitos  | Int | 31 |
| `DiaSemana` | Posição do dia na semana numérico com um dígito  | Int | 3 |
| `NomeDiaSemana` | Dia da semana por extenso | String | Quarta-feira |
| `NomeMes` | Mês por extenso  | String | Dezempbro |
| `AnoMes` | Ano e mês no formato de texto | String | "2025-12" |
| `Trimestre` | Trimestre numérico com um dígito | Int | 4 |
| `Semestre` | Semestre numérico com um dígito | Int | 2 |
| `SemanaAno` | Semana do ano numérico com dois dígitos | Int | 52 |
| `EhFimDeSemana` | Valor lógico indicativo de fim de semana | Boolean | FALSO |
| `DataInt` | Data no formato de número inteiro sem espaço | Int | 20251231 |
| `Feriado` | Nome do feriado por extenso (caso seja um feriado) | String | Véspera de Ano Novo |
| `Feriado Estadual` | Nome do feriado por extenso (caso seja um feriado estadual) | String | Revolução Constitucionalista |
| `Estado` | Nome do Estado do feriado Estadual | String | São Paulo |
| `EhFeriado` | Valor lógico indicativo de feriado nacional ou estadual| Boolean | VERDADEIRO |



> [!NOTE]
> As colunas `Feriado Estadual` e `Estado` só são incluídas no dataset quando pelo menos um Estado é selecionado na lista de Estados onde há feriados estaduais.

## Requisitos e Versões das Principais Bibliotecas

- **python** 3.13.5 (ou compatível)
- **streamlit** 1.52.2 (ou compatível)
- **pandas** 2.3.3 (ou compatível)
- **numpy** 2.4.0 (ou compatível)
- **xlsxwriter** 3.2.9 (ou compatível)


## Como Utilizar

`OBS:` Instruções de utilização baseadas em sistemas Linux derivados do Debian (Ubuntu, Linux Mint, Elementary OS, Pop!_OS, etc).

### 1 - Criar ambiente virtual

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```
### 2 - Instalar dependências e bibliotecas auxiliares
```bash
$ python3 -m pip install --upgrade pip
$ pip install pandas streamlit numpy xlsxwriter black
```

### 3 - Crie o script `app.py` na raiz do projeto usando o código fonte desse repositório e execute-o.
```bash
$ streamlit run app.py
```
### Resultado (Execução Local)

Uma aba do navegador abrirá com o seguinte endereço: `http://localhost:8501`



> [!NOTE]
> Para saber mais sobre o deploy e execução na nuvem, consulte a [documentação do Streamlit](https://docs.streamlit.io/).

## Casos de Uso

- Servir como tabela dimensão em projetos de **Business Inteligence** para análises temporais complexas;
- Utilizar em análises de dados que incluem múltiplas tabelas fato contendo datas, granularidades diferentes ou períodos sem dados de transações;
- Análises regionais ou com requisitos de negócio específicos como feriados, dias úteis, etc;
- Pré-calcular e indexar atributos da dimensão de data em **data warehouses** com grandes volumes de dados nas tabelas fato para ganho de performance em agregações.

## Observações Importantes

Esse é um projeto em estágio experimental. Antes de utilizar os arquivos de dados gerados através desse projeto em produção, verifique a consistência e a precisão dos dados gerados. O autor original desse projeto não se responsabiliza pelo uso indevido dos dados gerados através do projeto original ou por forks ou clones do mesmo.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/thaleswillreis/GeradorDCalendario/blob/main/LICEN%C3%87A_PT-BR.md) para mais detalhes.