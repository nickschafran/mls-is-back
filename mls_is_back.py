"""Predict who will advance from group stage of MLS is Back tournament."""
import csv
import pandas as pd


def get_groups(filename):
    """Create lookup where each key is a team and each value is a group."""
    groups = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k in row:
                if row[k] != '':
                    groups[row[k]] = k
    return groups


def transform_spi(groups, mls):
    """Filter SPI data to MLS & suppplement with group data."""
    df = pd.read_csv(mls)
    mls = df.loc[df['league'] == 'Major League Soccer']
    mls['group'] = mls['name'].map(lambda x: groups[x.upper()])
    averages = mls.groupby(by=['group']).mean()
    mls = mls.merge(averages, on='group', suffixes=('', '_group_avg'))
    mls['diff'] = mls.apply(lambda row: row.spi - row.spi_group_avg, axis=1)
    return mls


def predict_mls_is_back(mls):
    """Pick top two from each group and add next four best teams."""
    top_twelve = mls.groupby(['group']).apply(lambda x: x.nlargest(2, columns='diff'))
    next_four = mls.groupby(['group']).apply(lambda x: x.nlargest(3, columns='diff')[-1:]).nlargest(4, ['diff'])
    return pd.concat([top_twelve, next_four])


def main(groups_file, mls_file):
    groups = get_groups(groups_file)
    mls = transform_spi(groups, mls_file)
    mls_is_back = predict_mls_is_back(mls)
    mls_is_back.to_csv('mls_is_back.csv')


if __name__ == '__main__':
    main('groups.csv', 'soccer-spi/spi_global_rankings.csv')
