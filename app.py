import io
import json
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
import streamlit as st


# Cálculo de Páscoa e feriados
def easter_sunday(year: int) -> date:
    """
    Calcula o Domingo de Páscoa usando o Anonymous Gregorian Algorithm.
    Retorna um objeto datetime.date.
    """
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


# Feriados
def fixed_holidays(year: int) -> List[Dict[str, str]]:
    """
    Feriados fixos regulamentados por lei federal no Brasil.
    """
    return [
        {"date": date(year, 1, 1), "holiday": "Ano Novo"},
        {"date": date(year, 4, 21), "holiday": "Tiradentes"},
        {"date": date(year, 5, 1), "holiday": "Dia do Trabalho"},
        {"date": date(year, 9, 7), "holiday": "Independência do Brasil"},
        {"date": date(year, 10, 12), "holiday": "Nossa Sra. Aparecida"},
        {"date": date(year, 11, 2), "holiday": "Finados"},
        {"date": date(year, 11, 15), "holiday": "Proclamação da República"},
        {"date": date(year, 12, 25), "holiday": "Natal"},
    ]


# Datas comemorativas móveis
def movable_holidays(year: int) -> List[Dict[str, str]]:
    """
    Datas comemorativas móveis baseadas na Páscoa.
    """
    easter = easter_sunday(year)
    return [
        {"date": easter - timedelta(days=47), "holiday": "Carnaval"},
        {"date": easter - timedelta(days=2), "holiday": "Paixão de Cristo"},
        {"date": easter, "holiday": "Domingo de Páscoa"},
        {"date": easter + timedelta(days=60), "holiday": "Corpus Christi"},
    ]


# Feriados em um intervalo de datas
def all_holidays_in_range(start: date, end: date) -> pd.DataFrame:
    years = range(start.year, end.year + 1)
    records = []
    for y in years:
        for h in fixed_holidays(y) + movable_holidays(y):
            if start <= h["date"] <= end:
                records.append(
                    {"Data": pd.to_datetime(h["date"]), "Feriado": h["holiday"]}
                )
    return pd.DataFrame(records).sort_values("Data").reset_index(drop=True)


# Geração da dimensão de datas
def generate_date_dimension(start: date, end: date) -> pd.DataFrame:
    """
    Gera uma tabela dimensão de datas com colunas úteis para BI.
    Inclui feriados fixos e móveis brasileiros.
    """
    # Série de datas
    dates = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({"Data": dates})

    # Atributos de data
    df["Ano"] = df["Data"].dt.year
    df["Mes"] = df["Data"].dt.month
    df["Dia"] = df["Data"].dt.day
    df["DiaSemana"] = df["Data"].dt.dayofweek + 1  # 1=Segunda ... 7=Domingo
    df["NomeDiaSemana"] = df["Data"].dt.day_name(locale="pt_BR")
    df["NomeMes"] = df["Data"].dt.month_name(locale="pt_BR")
    df["AnoMes"] = df["Data"].dt.to_period("M").astype(str)
    df["Trimestre"] = df["Data"].dt.quarter
    df["Semestre"] = np.where(df["Mes"] <= 6, 1, 2)
    df["SemanaAno"] = df["Data"].dt.isocalendar().week.astype(int)
    df["EhFimDeSemana"] = df["DiaSemana"].isin([6, 7])

    # Chave inteira (YYYYMMDD)
    df["DataInt"] = df["Data"].dt.strftime("%Y%m%d").astype(int)

    # Feriados
    feriados_df = all_holidays_in_range(start, end)
    df = df.merge(feriados_df, on="Data", how="left")
    df["EhFeriado"] = df["Feriado"].notna()

    # Ordenação final
    df = df.sort_values("Data").reset_index(drop=True)
    return df


# Validação do intervalo de datas
def validate_date_range(
    start: date, end: date, max_years: int = 10
) -> Tuple[bool, str]:
    """
    Valida o intervalo de datas:
    - start <= end
    - intervalo máximo de 10 anos
    """
    if start > end:
        return False, "A data inicial deve ser menor ou igual à data final."
    # Considera diferença em dias e converte para anos aproximados
    delta_days = (end - start).days
    if delta_days > max_years * 366:  # tolerância para anos bissextos
        return False, f"O intervalo máximo permitido é de {max_years} anos."
    return True, ""


# Exportação de arquivos em vários formatos
def to_csv_bytes(df: pd.DataFrame, sep: str = ";") -> bytes:
    """
    Converte DataFrame para CSV em bytes com separador customizável.
    """
    return df.to_csv(index=False, sep=sep).encode("utf-8")


def to_xlsx_bytes(df: pd.DataFrame) -> bytes:
    """
    Converte DataFrame para XLSX em bytes.
    """
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="dCalendario")
    return buffer.getvalue()


def to_json_bytes(df: pd.DataFrame) -> bytes:
    """
    Converte DataFrame para JSON (records) em bytes.
    """
    records = df.copy()
    # Converter Data para string ISO
    records["Data"] = records["Data"].dt.strftime("%Y-%m-%d")
    return json.dumps(
        records.to_dict(orient="records"), ensure_ascii=False, indent=2
    ).encode("utf-8")


def to_sql_script(df: pd.DataFrame, table_name: str = "dCalendario") -> bytes:
    """
    Gera script SQL (CREATE TABLE + INSERTs) para a dimensão de datas.
    Tipos genéricos compatíveis com a maioria dos bancos.
    """
    # Mapeamento simples de tipos
    create_stmt = f"""
CREATE TABLE {table_name} (
    Data DATE,
    Ano INT,
    Mes INT,
    Dia INT,
    DiaSemana INT,
    NomeDiaSemana VARCHAR(20),
    NomeMes VARCHAR(20),
    AnoMes VARCHAR(7),
    Trimestre INT,
    Semestre INT,
    SemanaAno INT,
    EhFimDeSemana BOOLEAN,
    DataInt INT,
    Feriado VARCHAR(100),
    EhFeriado BOOLEAN
);
""".strip()

    # Preparar inserts
    inserts = []
    for _, row in df.iterrows():
        data_str = row["Data"].strftime("%Y-%m-%d")
        nome_dia = (row["NomeDiaSemana"] or "").replace("'", "''")
        nome_mes = (row["NomeMes"] or "").replace("'", "''")
        feriado = row["Feriado"] if pd.notna(row["Feriado"]) else ""
        feriado = feriado.replace("'", "''")

        insert = (
            f"INSERT INTO {table_name} (Data, Ano, Mes, Dia, DiaSemana, NomeDiaSemana, NomeMes, AnoMes, "
            f"Trimestre, Semestre, SemanaAno, EhFimDeSemana, DataInt, Feriado, EhFeriado) VALUES ("
            f"'{data_str}', {int(row['Ano'])}, {int(row['Mes'])}, {int(row['Dia'])}, {int(row['DiaSemana'])}, "
            f"'{nome_dia}', '{nome_mes}', '{row['AnoMes']}', {int(row['Trimestre'])}, {int(row['Semestre'])}, "
            f"{int(row['SemanaAno'])}, {str(bool(row['EhFimDeSemana'])).upper()}, {int(row['DataInt'])}, "
            f"'{feriado}', {str(bool(row['EhFeriado'])).upper()}"
            f");"
        )
        inserts.append(insert)

    script = create_stmt + "\n\n" + "\n".join(inserts) + "\n"
    return script.encode("utf-8")


# Funções de exportação geral
def export_dataframe(
    df: pd.DataFrame, fmt: str, csv_sep: str, filename: str
) -> Tuple[bytes, str]:
    """
    Exporta o DataFrame no formato escolhido e retorna (bytes, mime_type).
    """
    fmt = fmt.lower()
    if fmt == "csv":
        return to_csv_bytes(df, sep=csv_sep), "text/csv"
    elif fmt == "xlsx":
        return (
            to_xlsx_bytes(df),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    elif fmt == "json":
        return to_json_bytes(df), "application/json"
    elif fmt == "sql":
        return to_sql_script(df, table_name=filename), "application/sql"
    else:
        raise ValueError("Formato inválido.")


# Interface Streamlit
def main():
    st.set_page_config(
        page_title="Dimensão de Datas (Brasil)", page_icon="📅", layout="centered"
    )
    st.title("Dimensão de Datas — Brasil")
    st.caption(
        "Gere uma tabela de calendário com feriados fixos e móveis, pronta para BI."
    )

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data inicial", value=date(2020, 1, 1))
    with col2:
        end_date = st.date_input("Data final", value=date(2025, 12, 31))

    valid, msg = validate_date_range(start_date, end_date, max_years=10)
    if not valid:
        st.error(msg)
        st.stop()

    st.divider()
    st.subheader("Configurações de exportação")

    filename = st.text_input(
        "Nome do arquivo (sem extensão)", value="dCalendario"
    ).strip()
    fmt = st.selectbox("Formato", options=["csv", "xlsx", "json", "sql"], index=0)

    csv_sep = ";"
    if fmt == "csv":
        csv_sep = st.text_input("Separador de coluna (CSV)", value=";")

    st.divider()
    if st.button("Gerar tabela"):
        with st.spinner("Gerando dimensão de datas..."):
            df = generate_date_dimension(start_date, end_date)

        st.success(f"Tabela gerada com {len(df)} linhas.")
        st.dataframe(df.head(20), use_container_width=True)

        # Export
        try:
            bytes_data, mime = export_dataframe(
                df, fmt=fmt, csv_sep=csv_sep, filename=filename or "dCalendario"
            )
            ext = fmt if fmt != "sql" else "sql"
            download_name = f"{filename or 'dCalendario'}.{ext}"
            st.download_button(
                label="Baixar arquivo",
                data=bytes_data,
                file_name=download_name,
                mime=mime,
            )
        except Exception as e:
            st.error(f"Erro ao exportar: {e}")


if __name__ == "__main__":
    main()
