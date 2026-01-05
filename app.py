import io
import json
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
import streamlit as st


# --- CÁLCULO DE PÁSCOA ---
def easter_sunday(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    n = (h + l - 7 * m + 114) // 31
    o = (h + l - 7 * m + 114) % 31
    return date(year, n, o + 1)


# --- LÓGICA DE FERIADOS ---
def get_holidays(year: int, config: dict) -> List[Dict]:
    easter = easter_sunday(year)
    hols = [
        {"date": date(year, 1, 1), "holiday": "Confraternização Universal"},
        {"date": date(year, 4, 21), "holiday": "Tiradentes"},
        {"date": date(year, 5, 1), "holiday": "Dia do Trabalho"},
        {"date": date(year, 9, 7), "holiday": "Independência do Brasil"},
        {"date": date(year, 10, 12), "holiday": "Nossa Sra. Aparecida"},
        {"date": date(year, 11, 2), "holiday": "Finados"},
        {"date": date(year, 11, 15), "holiday": "Proclamação da República"},
        {"date": date(year, 11, 20), "holiday": "Consciência Negra"},
        {"date": date(year, 12, 25), "holiday": "Natal"},
        {"date": easter - timedelta(days=2), "holiday": "Paixão de Cristo"},
        {"date": easter, "holiday": "Domingo de Páscoa"},
    ]

    if config.get("incluir_carnaval"):
        hols.append(
            {"date": easter - timedelta(days=48), "holiday": "Carnaval (Segunda)"}
        )
        hols.append(
            {"date": easter - timedelta(days=47), "holiday": "Carnaval (Terça)"}
        )
    if config.get("incluir_cinzas"):
        hols.append(
            {"date": easter - timedelta(days=46), "holiday": "Quarta-feira de Cinzas"}
        )
    if config.get("incluir_corpus"):
        hols.append({"date": easter + timedelta(days=60), "holiday": "Corpus Christi"})
    if config.get("incluir_vespera_natal"):
        hols.append({"date": date(year, 12, 24), "holiday": "Véspera de Natal"})
    if config.get("incluir_vespera_ano_novo"):
        hols.append({"date": date(year, 12, 31), "holiday": "Véspera de Ano Novo"})

    return hols


def get_state_holidays(year: int, selected_states: List[str]) -> List[Dict]:
    easter = easter_sunday(year)
    state_data = {
        "São Paulo": [
            {"date": date(year, 7, 9), "holiday": "Revolução Constitucionalista"}
        ],
        "Rio de Janeiro": [
            {"date": easter - timedelta(days=47), "holiday": "Carnaval (Feriado RJ)"},
            {"date": date(year, 4, 23), "holiday": "Dia de São Jorge"},
            {"date": date(year, 10, 20), "holiday": "Dia do Comerciário"},
        ],
        "Minas Gerais": [{"date": date(year, 4, 21), "holiday": "Data Magna de MG"}],
        "Rio Grande do Sul": [
            {"date": date(year, 9, 20), "holiday": "Revolução Farroupilha"}
        ],
        "Bahia": [{"date": date(year, 7, 2), "holiday": "Independência da Bahia"}],
        "Pernambuco": [
            {"date": date(year, 3, 6), "holiday": "Data Magna de PE"},
            {"date": date(year, 6, 24), "holiday": "Dia de São João"},
        ],
        "Pará": [{"date": date(year, 8, 15), "holiday": "Adesão do Grão-Pará"}],
        "Amazonas": [
            {"date": date(year, 9, 5), "holiday": "Elevação do AM"},
            {"date": date(year, 12, 8), "holiday": "Nossa Sra. da Conceição"},
        ],
        "Ceará": [
            {"date": date(year, 3, 19), "holiday": "Dia de São José"},
            {"date": date(year, 3, 25), "holiday": "Data Magna do CE"},
        ],
        "Distrito Federal": [
            {"date": date(year, 4, 21), "holiday": "Fundação de Brasília"},
            {"date": date(year, 11, 30), "holiday": "Dia do Evangélico"},
            {"date": easter + timedelta(days=60), "holiday": "Corpus Christi (DF)"},
        ],
        "Espírito Santo": [
            {"date": easter + timedelta(days=8), "holiday": "Nossa Sra. da Penha"}
        ],
        "Maranhão": [{"date": date(year, 7, 28), "holiday": "Adesão do Maranhão"}],
        "Mato Grosso do Sul": [
            {"date": date(year, 10, 11), "holiday": "Criação do MS"}
        ],
        "Acre": [
            {"date": date(year, 1, 20), "holiday": "Dia do Católico"},
            {"date": date(year, 1, 25), "holiday": "Dia do Evangélico"},
            {"date": date(year, 6, 15), "holiday": "Aniversário do AC"},
            {"date": date(year, 9, 5), "holiday": "Dia da Amazônia"},
            {"date": date(year, 11, 17), "holiday": "Tratado de Petrópolis"},
        ],
        "Sergipe": [{"date": date(year, 7, 8), "holiday": "Emancipação de Sergipe"}],
        "Tocantins": [
            {"date": date(year, 1, 1), "holiday": "Instalação de TO"},
            {"date": date(year, 9, 8), "holiday": "Nossa Sra. da Natividade"},
            {"date": date(year, 10, 5), "holiday": "Criação de TO"},
        ],
        "Rondônia": [
            {"date": date(year, 1, 4), "holiday": "Criação de RO"},
            {"date": date(year, 6, 18), "holiday": "Dia do Evangélico"},
        ],
        "Alagoas": [
            {"date": date(year, 6, 24), "holiday": "Dia de São João"},
            {"date": date(year, 6, 29), "holiday": "Dia de São Pedro"},
            {"date": date(year, 9, 16), "holiday": "Emancipação de AL"},
        ],
        "Roraima": [{"date": date(year, 10, 5), "holiday": "Elevação de RR"}],
        "Amapá": [
            {"date": date(year, 3, 19), "holiday": "Dia de São José"},
            {"date": date(year, 7, 25), "holiday": "Dia de São Tiago"},
        ],
        "Paraíba": [{"date": date(year, 8, 5), "holiday": "Fundação da Paraíba"}],
        "Piauí": [
            {"date": date(year, 3, 13), "holiday": "Batalha do Jenipapo"},
            {"date": date(year, 10, 19), "holiday": "Dia do Piauí"},
        ],
    }

    state_hols = []
    for state in selected_states:
        if state in state_data:
            for h in state_data[state]:
                h_copy = h.copy()
                h_copy["Estado"] = state
                state_hols.append(h_copy)
    return state_hols


# --- GERAÇÃO DO DATAFRAME ---
def generate_date_dimension(start: date, end: date, config: dict, states: List[str]) -> pd.DataFrame:
    dates = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({"Data": dates})
    
    # Mapeamentos manuais para dias da semana e meses em português
    dias_pt = {
        0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 
        3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"
    }
    meses_pt = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    # Colunas de data
    df["Ano"] = df["Data"].dt.year
    df["Mes"] = df["Data"].dt.month
    df["Dia"] = df["Data"].dt.day
    df["DiaSemana"] = df["Data"].dt.dayofweek + 1
    
    # Mapeamento manual em vez de usar locale="pt_BR"
    df["NomeDiaSemana"] = df["Data"].dt.dayofweek.map(dias_pt)
    df["NomeMes"] = df["Data"].dt.month.map(meses_pt)
    
    df["AnoMes"] = df["Data"].dt.to_period("M").astype(str)
    df["Trimestre"] = df["Data"].dt.quarter
    df["Semestre"] = np.where(df["Mes"] <= 6, 1, 2)
    df["SemanaAno"] = df["Data"].dt.isocalendar().week.astype(int)
    df["EhFimDeSemana"] = df["DiaSemana"].isin([6, 7])
    df["DataInt"] = df["Data"].dt.strftime("%Y%m%d").astype(int)

    # Nacionais
    all_nacionais = []
    for y in range(start.year, end.year + 1):
        all_nacionais.extend(get_holidays(y, config))

    if all_nacionais:
        nac_df = pd.DataFrame(all_nacionais)
        nac_df["Data"] = pd.to_datetime(nac_df["date"])
        df = df.merge(nac_df[["Data", "holiday"]], on="Data", how="left")
        df.rename(columns={"holiday": "Feriado"}, inplace=True)
    else:
        df["Feriado"] = np.nan

    # Estaduais
    if states:
        all_estaduais = []
        for y in range(start.year, end.year + 1):
            all_estaduais.extend(get_state_holidays(y, states))

        if all_estaduais:
            est_df = pd.DataFrame(all_estaduais)
            est_df["Data"] = pd.to_datetime(est_df["date"])
            est_grouped = (
                est_df.groupby("Data")
                .agg(
                    {
                        "holiday": lambda x: " / ".join(list(dict.fromkeys(x))),
                        "Estado": lambda x: ", ".join(list(dict.fromkeys(x))),
                    }
                )
                .reset_index()
            )
            df = df.merge(est_grouped, on="Data", how="left")
            df.rename(columns={"holiday": "Feriado Estadual"}, inplace=True)
        else:
            df["Feriado Estadual"] = np.nan
            df["Estado"] = np.nan

    df["EhFeriado"] = df["Feriado"].notna() | (
        df["Feriado Estadual"].notna() if "Feriado Estadual" in df.columns else False
    )
    return df.sort_values("Data").reset_index(drop=True)


# --- FUNÇÕES DE EXPORTAÇÃO ---
def to_csv_bytes(df: pd.DataFrame, sep: str = ";") -> bytes:
    return df.to_csv(index=False, sep=sep, encoding="utf-8-sig").encode("utf-8-sig")


def to_xlsx_bytes(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="dCalendario")
    return buffer.getvalue()


def to_json_bytes(df: pd.DataFrame) -> bytes:
    records = df.copy()
    records["Data"] = records["Data"].dt.strftime("%Y-%m-%d")
    return json.dumps(
        records.to_dict(orient="records"), ensure_ascii=False, indent=2
    ).encode("utf-8")


def to_sql_script(df: pd.DataFrame, table_name: str = "dCalendario") -> bytes:
    cols = df.columns.tolist()

    def map_sql_type(col_name):
        if "Data" in col_name and "Int" not in col_name:
            return "DATE"
        if df[col_name].dtype in [np.int64, np.int32, "int64"]:
            return "INT"
        if df[col_name].dtype == bool:
            return "BOOLEAN"
        return "VARCHAR(255)"

    create_cols = [f"{c} {map_sql_type(c)}" for c in cols]
    create_stmt = (
        f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(create_cols) + "\n);"
    )

    inserts = []
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = row[col]
            if pd.isna(val):
                vals.append("NULL")
            elif isinstance(val, (date, datetime, pd.Timestamp)):
                vals.append(f"'{val.strftime('%Y-%m-%d')}'")
            elif isinstance(val, str):
                vals.append(f"'{val.replace(chr(39), chr(39)+chr(39))}'")
            elif isinstance(val, bool):
                vals.append("TRUE" if val else "FALSE")
            else:
                vals.append(str(val))

        inserts.append(
            f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(vals)});"
        )

    return (create_stmt + "\n\n" + "\n".join(inserts)).encode("utf-8")


def export_dataframe(
    df: pd.DataFrame, fmt: str, csv_sep: str, filename: str
) -> Tuple[bytes, str]:
    fmt = fmt.lower()
    if fmt == "csv":
        return to_csv_bytes(df, sep=csv_sep), "text/csv"
    if fmt == "xlsx":
        return (
            to_xlsx_bytes(df),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    if fmt == "json":
        return to_json_bytes(df), "application/json"
    if fmt == "sql":
        return to_sql_script(df, table_name=filename), "application/sql"
    raise ValueError("Formato inválido.")


# --- INTERFACE ---
def main():
    st.set_page_config(page_title="Calendário Brasil BI", page_icon="📅", layout="wide")
    st.title("📅 Gerador de Tabela Dimensão Calendário")

    with st.sidebar:
        st.header("1. Período")
        start_date = st.date_input("Início", value=date(2024, 1, 1))
        end_date = st.date_input("Fim", value=date(2025, 12, 31))

        st.divider()
        st.header("2. Feriados Opcionais")
        config = {
            "incluir_carnaval": st.checkbox("Carnaval (Seg/Ter)", value=True),
            "incluir_cinzas": st.checkbox("Quarta de Cinzas", value=False),
            "incluir_corpus": st.checkbox("Corpus Christi", value=True),
            "incluir_vespera_natal": st.checkbox("Véspera Natal", value=False),
            "incluir_vespera_ano_novo": st.checkbox("Véspera Ano Novo", value=False),
        }

    st.subheader("Feriados Estaduais")
    lista_estados = [
        "Acre",
        "Alagoas",
        "Amapá",
        "Amazonas",
        "Bahia",
        "Ceará",
        "Distrito Federal",
        "Espírito Santo",
        "Maranhão",
        "Mato Grosso do Sul",
        "Minas Gerais",
        "Pará",
        "Paraíba",
        "Pernambuco",
        "Piauí",
        "Rio de Janeiro",
        "Rio Grande do Sul",
        "Rondônia",
        "Roraima",
        "Sergipe",
        "São Paulo",
        "Tocantins",
    ]

    sel_est = st.multiselect(
        "Selecione os Estados:", options=["Todos os Estados"] + lista_estados
    )
    final_states = lista_estados if "Todos os Estados" in sel_est else sel_est

    st.divider()
    st.subheader("Configurações de Exportação")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filename = st.text_input("Nome da tabela/arquivo", value="dCalendario")
    with col_f2:
        fmt = st.selectbox("Formato", options=["csv", "xlsx", "json", "sql"])
    with col_f3:
        csv_sep = (
            st.text_input("Separador (se CSV)", value=";") if fmt == "csv" else ";"
        )

    if st.button("Gerar e Visualizar", use_container_width=True):
        df = generate_date_dimension(start_date, end_date, config, final_states)
        st.success(f"Tabela gerada com {len(df)} linhas.")
        st.dataframe(df.head(50), use_container_width=True)

        data_bytes, mime = export_dataframe(df, fmt, csv_sep, filename)
        st.download_button(
            label=f"Baixar arquivo .{fmt}",
            data=data_bytes,
            file_name=f"{filename}.{fmt}",
            mime=mime,
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
