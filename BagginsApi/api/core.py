import pandas as pd


def cloud(x):
    if x in ['Облаков нет.', 'Небо не видно из-за тумана и/или других метеорологических явлений.']:
        return 0
    else:
        return 1


def state_cloud(x):
    if x in ['Облаков нет.']:
        return 0
    elif x in ['0', '10%  или менее, но не 0', '20–30%.']:
        return 1
    elif x in ['40%.', '50%.', '60%.']:
        return 2
    else:
        return 3


def rainfall(x):
    if x in ['Осадков нет', 'Следы осадков']:
        return 0
    else:
        return x


def wind(x):
    if x == 'Штиль, безветрие':
        return 0
    else:
        return 1


def transform_data(df):
    df['Местное время в Санкт-Петербурге'] = pd.to_datetime(df['Местное время в Санкт-Петербурге'])
    df = df[~df['Местное время в Санкт-Петербурге'].dt.time.isin([
        pd.to_datetime('00:00:00').time(),
        pd.to_datetime('03:00:00').time(),
        pd.to_datetime('06:00:00').time()
    ])]

    df = df.rename(columns={'Местное время в Санкт-Петербурге': 'time'})

    df.RRR.fillna(0, inplace=True)
    df.Nh.fillna(0, inplace=True)
    df.N.fillna(0, inplace=True)
    df.Pa.fillna(df.Pa.median(), inplace=True)

    df['cloud'] = df.N.apply(cloud)
    df.drop('N', axis=1, inplace=True)

    df['Nh'] = df.Nh.apply(state_cloud)
    df['RRR'] = df.RRR.apply(rainfall).astype('float')

    df['DD'] = df.DD.apply(wind)

    col_to_drop = ['ff10', 'Tg', 'P', 'WW', 'Td', 'E', 'sss', 'ff3', 'Tx',
                   'Tn', 'W1', 'W2', 'tR', 'H', 'Ch', 'Cm', 'Cl', "E'"]
    df = df.drop(col_to_drop, axis = 1)

    df['time'] = df['time'].dt.date
    df = df.groupby('time').mean().reset_index()
    df['time'] = pd.to_datetime(df['time']).dt.date

    df['time'] = pd.to_datetime(df['time'])
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.day
    df['day_of_week'] = df['time'].dt.dayofweek

    holidays = pd.to_datetime([
        '2022-01-01', '2022-01-07', '2022-02-23', '2022-03-08', '2022-05-01',
        '2022-05-09', '2022-06-12', '2022-11-04', '2022-05-27', '2022-06-01',
        '2023-01-01', '2023-01-07', '2023-02-23', '2023-03-08', '2023-05-01',
        '2023-05-09', '2023-06-12', '2023-11-04', '2023-05-27', '2023-06-01'
    ])
    df['is_holiday'] = df['time'].isin(holidays).astype(int)

    return df