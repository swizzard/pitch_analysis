import os

import pandas as pd

from voros import Scraper


def scrape_and_save(start, end):
    df = pd.DataFrame(Scraper().run(start, end))
    df = pd.concat([df] + [pd.get_dummies(getattr(df, col), prefix=col)
                           for col in ('type', 'pitch_type', 'event')],
                   axis=1)
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
