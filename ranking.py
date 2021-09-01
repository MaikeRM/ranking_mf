import numpy as np
import pandas as pd
import string
import warnings
import requests
warnings.filterwarnings('ignore')

import requests

#A url que você quer acesssar
url = 'https://www.fundamentus.com.br/resultado.php'

#Informações para fingir ser um navegador
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
#juntamos tudo com a requests
r = requests.get(url, headers=header)
#E finalmente usamos a função read_html do pandas
df = pd.read_html(r.text,  decimal=',', thousands='.')[0]

for coluna in ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Cresc. Rec.5a']:
  df[coluna] = df[coluna].astype(str).str.replace('.', '')
  df[coluna] = df[coluna].astype(str).str.replace(',', '.')
  df[coluna] = df[coluna].astype(str).str.rstrip('%').astype('float') / 100

df = df[df['Liq.2meses'] > 1000000]

ranking = pd.DataFrame()
ranking['pos'] = range(1,151)
ranking['EV/EBIT'] = df[df['EV/EBIT'] >0].sort_values(by=['EV/EBIT'])['Papel'][:150].values
ranking['ROIC'] = df.sort_values(by=['ROIC'], ascending=False)['Papel'][:150].values
ranking['ROE'] = df.sort_values(by=['ROE'], ascending=False)['Papel'][:150].values
ranking['P/L'] = df[df['P/L'] >0].sort_values(by=['P/L'])['Papel'][:150].values
ranking['Mrg. Líq.'] = df.sort_values(by=['Mrg. Líq.'], ascending=False)['Papel'][:150].values

a = ranking.pivot_table(columns='EV/EBIT', values='pos')
b = ranking.pivot_table(columns='ROIC', values='pos')
c = ranking.pivot_table(columns='ROE', values='pos')
d = ranking.pivot_table(columns='P/L', values='pos')

t = pd.concat([a,b,c,d])

rank = t.dropna(axis=1)

a = pd.DataFrame(data=ranking.values, index = ranking['EV/EBIT'])
a.columns = ['EV/EBIT', '1', '1','1','1','1' ]
a.drop(columns=['1'], inplace=True)
a.index.names = ['Ticker']

b = pd.DataFrame(data=ranking.values, index = ranking['ROIC'])
b.columns = ['ROIC', '1', '1','1','1','1' ]
b.drop(columns=['1'], inplace=True)
b.index.names = ['Ticker']

c = pd.DataFrame(data=ranking.values, index = ranking['P/L'])
c.columns = ['P/L', '1', '1','1','1','1' ]
c.drop(columns=['1'], inplace=True)
c.index.names = ['Ticker']

d = pd.DataFrame(data=ranking.values, index = ranking['ROE'])
d.columns = ['ROE', '1', '1','1','1','1' ]
d.drop(columns=['1'], inplace=True)
d.index.names = ['Ticker']

y = a.merge(b,left_on=a.index, right_on=b.index, suffixes=('_left', '_right'))
y.set_index('key_0', inplace=True)
y = y.merge(c,left_on=y.index, right_on=c.index, suffixes=('_left', '_right'))
y.set_index('key_0', inplace=True)
y = y.merge(d,left_on=y.index, right_on=d.index, suffixes=('_left', '_right'))
y.set_index('key_0', inplace=True)
y.index.names = ['Ticker']

y['Geral'] = y['EV/EBIT']+y['ROIC']+y['P/L']+y['ROE']

print(y.sort_values(by='Geral').head(10))