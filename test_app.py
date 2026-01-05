import pytest
from datetime import date
import pandas as pd
from app import easter_sunday, get_holidays, generate_date_dimension


# Teste do cálculo da Páscoa (Datas conhecidas)
@pytest.mark.parametrize(
    "year, expected",
    [
        (2024, date(2024, 3, 31)),
        (2025, date(2025, 4, 20)),
        (2026, date(2026, 4, 5)),
    ],
)
def test_easter_sunday(year, expected):
    assert easter_sunday(year) == expected


# Teste se os feriados opcionais estão sendo respeitados
def test_optional_holidays_config():
    year = 2024
    # Configuração 1: Sem Carnaval
    config_no_carnival = {"incluir_carnaval": False}
    hols_1 = get_holidays(year, config_no_carnival)
    assert not any("Carnaval" in h["holiday"] for h in hols_1)

    # Configuração 2: Com Carnaval
    config_with_carnival = {"incluir_carnaval": True}
    hols_2 = get_holidays(year, config_with_carnival)
    assert any("Carnaval" in h["holiday"] for h in hols_2)


# Teste da estrutura do DataFrame gerado
def test_generate_date_dimension_structure():
    start = date(2024, 1, 1)
    end = date(2024, 1, 10)
    config = {"incluir_carnaval": True}
    states = ["São Paulo"]

    df = generate_date_dimension(start, end, config, states)

    # Verifica se colunas essenciais existem
    assert "Data" in df.columns
    assert "NomeMes" in df.columns
    assert "Feriado Estadual" in df.columns
    assert "Estado" in df.columns
    # Verifica a quantidade de dias (1 a 10 = 10 dias)
    assert len(df) == 10
    # Verifica se a tradução manual funcionou (1 de Janeiro de 2024 foi Segunda-feira)
    assert (
        df.loc[df["Data"] == "2024-01-01", "NomeDiaSemana"].values[0] == "Segunda-feira"
    )


# Teste de Feriado Estadual específico
def test_state_holiday_sp():
    start = date(2024, 7, 1)
    end = date(2024, 7, 10)
    config = {}
    states = ["São Paulo"]

    df = generate_date_dimension(start, end, config, states)

    # 9 de Julho deve ser feriado em SP
    sp_holiday = df[df["Data"] == "2024-07-09"]
    assert sp_holiday["Feriado Estadual"].values[0] == "Revolução Constitucionalista"
    assert sp_holiday["Estado"].values[0] == "São Paulo"
