import pytest
import pandas as pd
import numpy as np
from datetime import date
from app import easter_sunday, get_holidays, generate_date_dimension

# --- TESTE 1: CÁLCULO DA PÁSCOA ---
@pytest.mark.parametrize("year, expected", [
    (2024, date(2024, 3, 31)),
    (2025, date(2025, 4, 20)),
    (2026, date(2026, 4, 5)),
])
def test_easter_sunday(year, expected):
    assert easter_sunday(year) == expected

# --- TESTE 2: LÓGICA DE DIAS DA SEMANA (DOMINGO = 1) ---
def test_weekday_logic():
    # 05/01/2025 é reconhecidamente um Domingo
    start = date(2025, 1, 5)
    df = generate_date_dimension(start, start, {}, [])
    
    assert df.loc[0, "DiaSemana"] == 1
    assert df.loc[0, "NomeDiaSemana"] == "Domingo"
    assert df.loc[0, "EhFimDeSemana"] == True

# --- TESTE 3: DUPLA SEMANA (CIVIL VS ISO) ---
def test_week_numbering():
    # 29/12/2025 é uma Segunda-feira.
    # No padrão Civil (%U - começando domingo), é a última semana (53) de 2025.
    # No padrão ISO, já é considerada a Semana 1 de 2026.
    test_date = date(2025, 12, 29)
    df = generate_date_dimension(test_date, test_date, {}, [])
    
    assert df.loc[0, "SemanaAno"] == 53
    assert df.loc[0, "SemanaAnoISO"] == 1

# --- TESTE 4: TIMESTAMPS (EXCEL EPOCH E UNIX) ---
def test_epochs_and_timestamps():
    # 01/01/1970 
    # Unix Posix deve ser 0
    # Excel Epoch deve ser 25569
    test_date = date(1970, 1, 1)
    df = generate_date_dimension(test_date, test_date, {}, [])
    
    assert df.loc[0, "DataUnixPosix"] == 0
    assert df.loc[0, "DataEpoch"] == 25569

# --- TESTE 5: DIA DO ANO ---
def test_day_of_year():
    # Em ano bissexto (2024), 31/12 é o dia 366
    df = generate_date_dimension(date(2024, 12, 31), date(2024, 12, 31), {}, [])
    assert df.loc[0, "DiaDoAno"] == 366

# --- TESTE 6: INTEGRIDADE DA TABELA ---
def test_dataframe_integrity():
    start = date(2024, 1, 1)
    end = date(2024, 12, 31)
    df = generate_date_dimension(start, end, {"incluir_carnaval": True}, ["São Paulo"])
    
    # Verifica se gerou o número correto de dias em um ano bissexto
    assert len(df) == 366
    # Verifica se colunas de feriado existem
    assert "Feriado" in df.columns
    assert "Feriado Estadual" in df.columns
    # Verifica feriado estadual de SP
    sp_hol = df[df["Data"] == "2024-07-09"]
    assert sp_hol["Feriado Estadual"].values[0] == "Revolução Constitucionalista"

# --- TESTE 7: FERIADOS NACIONAIS MÓVEIS ---
def test_national_movable_holidays():
    # Natal sempre 25/12
    df = generate_date_dimension(date(2024, 12, 25), date(2024, 12, 25), {}, [])
    assert df.loc[0, "Feriado"] == "Natal"