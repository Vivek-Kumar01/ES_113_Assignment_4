import fitz
import pandas as pd


def to_date(date):
    month_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12',
    }
    d, m, y = date.strip().split('/')
    return y + '-' + month_dict[m] + '-' + d


pdf_doc = fitz.open('Bonds_Redeemed.pdf')

data = []
for page in pdf_doc.pages():
    df = page.find_tables()[0].to_pandas()
    for column in ['Date of\nEncashment']:
        df[column] = pd.Series([to_date(d) for d in list(df[column])])
    data.append(df)

pd.concat(data).to_csv('Bonds_Redeemed.csv')
