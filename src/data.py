"""Load and audit the five original course workbooks without modifying raw files."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
FILES = {name: RAW / f'Telco_customer_churn_{name}.xlsx' for name in
         ('demographics','location','population','services','status')}


def load_tables() -> dict[str, pd.DataFrame]:
    """Read the original workbooks; preserve the category 'None' and text ZIP codes."""
    tables = {}
    for name, filename in FILES.items():
        if not filename.exists():
            raise FileNotFoundError(f'Missing raw data file: {filename}')
        dtypes = {'Zip Code': str} if name in {'location', 'population'} else None
        tables[name] = pd.read_excel(filename, keep_default_na=False, dtype=dtypes)
    return tables


def validate_tables(tables: dict[str, pd.DataFrame]) -> None:
    """Fail loudly if the intended one-row-per-customer grain is violated."""
    for name in ('demographics', 'location', 'services', 'status'):
        df = tables[name]
        if df['Customer ID'].duplicated().any():
            raise ValueError(f'Duplicate Customer ID in {name}')
        if df['Customer ID'].isna().any() or (df['Customer ID'] == '').any():
            raise ValueError(f'Missing Customer ID in {name}')
    if tables['population']['Zip Code'].duplicated().any():
        raise ValueError('Duplicate Zip Code in population')
    customer_sets = [set(tables[k]['Customer ID']) for k in ('demographics','location','services','status')]
    if not all(ids == customer_sets[0] for ids in customer_sets[1:]):
        raise ValueError('Customer ID coverage differs across the four primary tables')
    if not set(tables['location']['Zip Code']).issubset(set(tables['population']['Zip Code'])):
        raise ValueError('Some customer ZIP Codes are not in the Population table')
    if not (tables['services']['Quarter'].eq('Q3').all() and tables['status']['Quarter'].eq('Q3').all()):
        raise ValueError('Unexpected quarter labels')


def load_customers() -> pd.DataFrame:
    """Join source tables with validated cardinality, returning one row per customer."""
    t = load_tables()
    validate_tables(t)
    merged = t['demographics'].merge(t['location'].drop(columns=['Count']), on='Customer ID',validate='one_to_one')
    merged = merged.merge(t['services'].drop(columns=['Count']),on='Customer ID',validate='one_to_one')
    merged = merged.merge(t['status'].drop(columns=['Count','Quarter']),on='Customer ID',validate='one_to_one')
    merged = merged.merge(t['population'].drop(columns=['ID']),on='Zip Code',validate='many_to_one')
    if len(merged) != len(t['demographics']):
        raise ValueError('Join unexpectedly changed the customer row count')
    return merged


def load_core_population() -> pd.DataFrame:
    """Return only Stayed/Churned rows eligible for the assigned binary task."""
    df = load_customers()
    return df.loc[df['Customer Status'].isin(('Stayed','Churned'))].copy()


if __name__ == '__main__':
    t = load_tables()
    validate_tables(t)
    all_customers = load_customers()
    core = load_core_population()
    print('Source tables:', {k: v.shape for k, v in t.items()})
    print('Joined:', all_customers.shape)
    print('Core modeling population:', core.shape)
    print('Statuses:', all_customers['Customer Status'].value_counts().to_dict())
    print('Churn rate in core population:', round(core['Customer Status'].eq('Churned').mean(), 4))
    print('Offer categories:', t['services']['Offer'].value_counts().to_dict())
    print('Internet categories:', t['services']['Internet Type'].value_counts().to_dict())
