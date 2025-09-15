Filters on the dashboard: had delivery

Facebook metrics:

- Day
- Ad name
- Cost
- Video avg. play time
- Revenue
- Imp
- video plays at 75%
- video plays
- Link clicks
- purchases
- date launched
- report start date
- report end date
- 3 second video plays
- Purchases
- results

Calculated metrics:

- CTR
- CPM
- CR
- Hook
- Magic Formula

Calculated columns:

- Creative type: video or image
- Website name: AEF
- Creative name: 65
- Hook: V2 or n/a if image

Types of reports:

- Image vs video
- Hook comparison for all videos
- Video comparison


So the workflow looks like this:

1. Raw data (fact table): df_raw

2. Summarize/aggregate: df_summary = summarize(df_raw, by=["account", "video_name"])

3. Add metrics: handled inside add_metrics(df_summary)

4. Slice for views: e.g. view_video_by_account(df_raw) returns a new DF ready for presentation.


def add_metrics(df):
    return df.assign(
        ctr       = lambda d: safe_div(d["clicks"], d["impressions"]),
        cpc       = lambda d: safe_div(d["spend"], d["clicks"]),
        cpm       = lambda d: safe_div(d["spend"] * 1000, d["impressions"]),
        conv_rate = lambda d: safe_div(d["results"], d["clicks"]),
        roas      = lambda d: safe_div(d["revenue"], d["spend"]),
    )