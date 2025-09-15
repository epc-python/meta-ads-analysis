# determine which account is which based on the ad name

def extract_dates(df):
    df['Report Start Date'] = df['Report start date'].str.split(' ').str[0]
    df['Report End Date'] = df['Report end date'].str.split(' ').str[0]
    return df

def map_account(ad_name):

    if "AEF" in ad_name:
        return "AEF"
    elif "FLA" in ad_name:
        return "FLA"
    elif "FLD" in ad_name:
        return "FLD"
    else:
        return "unknown"

def map_creative_type(ad_name):

    if "Image" in ad_name:
        return "Image"
    elif "Video" in ad_name:
        return "Video"

    else:
        return "unknown"

def create_hook(ad_name):

    try:

        if "Image" in ad_name:

            try:
                return ad_name.split('V')[1].split(' - ')[0]

            except:
                return ad_name.split('V')[1]

        
        if "Video" in ad_name:

            try:    
                return ad_name.split('V')[2].split(' - ')[0]

            except:
                return ad_name.split('V')[2]

    except:
        return "unknown or no hook"

def creative_name(ad_name):

    try:

        if "Image" in ad_name:
            return "Image " + ad_name.split('Image')[1].split(' ')[1]

        if "Video" in ad_name:
            return "Video " + ad_name.split('Video')[1].split(' ')[1]

    except:
        return "unknown"

    
def create_metrics(df):
    df['ROAS'] = (df['revenue'] / df['amount_spent']).round(2)
    df['CTR'] = ((df['link_clicks'] / df['impressions']) * 100).round(2)
    df['Conversion Rate'] = ((df['results'] / df['link_clicks']) * 100).round(2)
    df['Thumbstop Rate'] = ((df['three_second_video_plays'] / df['impressions']) * 100).round(2)
    return df

def GroupByAccount(df, account, creative_type, group_by):
    # filter first
    df = df[
        (df['Account Name'] == account)
        & (df['Creative Type'] == creative_type)
    ]

    # aggregate just what you need
    grouped = df.groupby(group_by).agg(
        account_name=('Account Name', 'first'),
        amount_spent=('Amount spent (USD)', 'sum'),
        impressions=('Impressions', 'sum'),
        link_clicks=('Link clicks', 'sum'),
        results=('Results', 'sum'),
        revenue=('Purchases conversion value', 'sum'),
        three_second_video_plays=('3-second video plays', 'sum'),
    )

    # calculate metrics
    grouped = create_metrics(grouped)

    grouped = grouped.sort_values(by='amount_spent', ascending=False)
    # then format
    grouped['amount_spent'] = grouped['amount_spent'].apply(lambda x: f"${x:,.2f}")
    grouped['revenue'] = grouped['revenue'].apply(lambda x: f"${x:,.2f}")


    # keep only final columns (instead of aggregating then dropping)
    grouped = grouped[['account_name', 'amount_spent', 'revenue', 'ROAS', 'CTR', 'Conversion Rate', 'Thumbstop Rate']]

    return grouped