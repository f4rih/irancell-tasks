import pytest
from django.db import connection
from django.urls import reverse


@pytest.fixture
def kpi_url():
    return reverse("kpi")


@pytest.fixture
def seed_database(db):
    with connection.cursor() as cursor:
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS kpi_2_aggregations (
                id SERIAL PRIMARY KEY,
                field_type VARCHAR(50),
                field_name VARCHAR(255),
                value NUMERIC(20, 8),
                agg_type VARCHAR(10)
            );
        """)
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS kpi_6_aggregations (
                id SERIAL PRIMARY KEY,
                field_type VARCHAR(50),
                field_name VARCHAR(255),
                value NUMERIC(20, 8),
                agg_type VARCHAR(10)
            );
        """)

        cursor.executescript("""
            INSERT INTO kpi_2_aggregations (field_type, field_name, value, agg_type)
            VALUES
                ('city', 'ABADAN', 100.5, 'avg'),
                ('city', 'SARI', 200.75, 'avg');
        """)
        cursor.executescript("""
            INSERT INTO kpi_6_aggregations (field_type, field_name, value, agg_type)
            VALUES
                ('province', 'TEHRAN', 50.0, 'sum'),
                ('province', 'ALBORZ', 300.0, 'sum');;
        """)


@pytest.mark.django_db
def test_kpi_view_valid_request(client, kpi_url, seed_database):
    payload = {
        "layer": "city",
        "elements": ["ABADAN", "SARI"],
        "kpi": "100 * kpi_2"
    }
    response = client.post(kpi_url, data=payload, content_type="application/json")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "result": {
            "ABADAN": '10050.0000000000',
            "SARI": '20075.0000000000'
        }
    }

# Test for a different layer and KPI expression
@pytest.mark.django_db
def test_kpi_view_province_request(client, kpi_url, seed_database):
    payload = {
        "layer": "province",
        "elements": ["ALBORZ", "TEHRAN"],
        "kpi": "(kpi_6 + 50) / 2"
    }
    response = client.post(kpi_url, data=payload, content_type="application/json")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "result": {
            "ALBORZ": '175.000000000000',
            "TEHRAN": '50.0000000000000'
        }
    }
