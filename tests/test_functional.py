import pytest

from src.manager import Manager
from src.models import Parameters

def test_settlement_total_due_matches_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)
    apartment_key = "apart-polanka"
    year = 2025
    month = 1

    apartment_costs = manager.get_apartment_costs(apartment_key, year, month)
    apartment_settlement = manager.get_settlement(apartment_key, year, month)

    tenants_settlements = manager.create_tenants_settlements(apartment_settlement)
    tenants_total_due = sum(ts.total_due_pln for ts in tenants_settlements)

    assert apartment_costs is not None
    assert len(tenants_settlements) > 0
    assert tenants_total_due == pytest.approx(apartment_costs, abs=0.01)

def test_get_tax():
    parameters = Parameters()
    manager = Manager(parameters)
    tax_2025_01 = manager.get_tax(year=2025, month=1, tax_rate=0.085)

    assert isinstance(tax_2025_01, int)
    assert tax_2025_01 == 638

    assert manager.get_tax(year=2024, month=1, tax_rate=0.085) == 0

    with pytest.raises(ValueError):
        manager.get_tax(year=2025, month=13, tax_rate=0.085)