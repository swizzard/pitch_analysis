from datetime import date
import os

import pandas as pd

from voros import Scraper


def scrape_and_save(start, end):
    df = pd.DataFrame(Scraper().run(start, end))
    df = pd.concat([df] + [pd.get_dummies(getattr(df, col), prefix=col)
                           for col in ('type', 'pitch_type', 'event')],
                   axis=1)
    df = fmt_dates(df)
    fname = 'pitch_data_{}_{}.csv'.format(start, end)
    df.to_csv(fmt_fname(start, end))
    return df


def load(start, end):
    fname = fmt_fname(start, end)
    if os.path.exists(fname):
        return pd.DataFrame.from_csv(fname)
    else:
        return scrape_and_save(start, end)


def fmt_fname(start, end):
    return 'pitch_data_{}_{}.csv'.format(start, end)


def fmt_dates(df):
    df['dates'] = df['tfs_zulu'].apply(
        lambda date_str: datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ'))
    return df


def get():
    for y in xrange(2008, 2016):
        scrape_and_save(date(y, 4, 1), date(y, 11, 2))

