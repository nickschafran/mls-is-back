"""Predict who will advance from group stage of MLS is Back tournament."""
import csv
import pandas as pd


def get_groups(filename):
    """Create lookup where each key is a team and each value is a group."""
    with open(filename) as f:
        reader = csv.DictReader(f)
        return {row[k]: k for row in reader for k in row if row[k] != ''}


def transform_spi(groups, filename):
    """Filter SPI data to MLS & suppplement with group data."""
    spi = pd.read_csv(filename)
    mls = spi.loc[spi['league'] == 'Major League Soccer']
    mls['group'] = mls['name'].map(lambda x: groups[x.upper()])
    averages = mls.groupby(by=['group']).mean()
    mls = mls.merge(averages, on='group', suffixes=('', '_group_avg'))
    mls['diff'] = mls.apply(lambda row: row.spi - row.spi_group_avg, axis=1)
    return mls


def predict_mls_is_back(mls):
    """Pick top two/three from each group and add next three best teams."""
    groups = mls.groupby(['group'])
    top_twelve = groups.apply(lambda x: x.nlargest(2, columns='diff'))

    # updated rule: top three from group a advance
    group_a = mls.loc[mls['group'] == 'A']
    third = group_a.groupby(['group']).apply(lambda x: x.nlargest(3, columns='diff'))[2:3]
    top_thirteen = pd.concat([top_twelve, third])

    # next best three also qualify
    thirteen_names = top_thirteen.to_dict('l')['name']
    remaining_teams = mls[~mls['name'].isin(thirteen_names)].dropna()
    next_three = remaining_teams.groupby(['group']).apply(lambda x: x.nlargest(1, columns='diff')).nlargest(3, ['diff'])

    return pd.concat([top_thirteen, next_three])


def main(groups_file, mls_file):
    groups = get_groups(groups_file)
    mls = transform_spi(groups, mls_file)
    mls_is_back = predict_mls_is_back(mls)
    return mls_is_back


if __name__ == '__main__':
    mls_is_back = main('groups.csv', 'soccer-spi/spi_global_rankings.csv')
    mls_is_back.to_csv('mls_is_back.csv')
