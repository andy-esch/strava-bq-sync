# Strava to BigQuery Sync

Sync Strava data to Google BigQuery using Strava's Webhooks.

This Cloud Function appends created (new) activities to an activities table. It also
maintains a separate table that keeps track of the state of activies (e.g., updates
and deletes). For updates, titles (and other attributes) can change. For deletes,
deleted activities have their IDs logged so that a final view will give the current
state of Strava Activities in an account.


```sql
SELECT a.id, a.distance, coalesce(c.title, a.title) as title
  FROM activities as a
LEFT JOIN changes as c
  ON a.id = c.id
WHERE c.was_deleted is not true
```


## Bootstrap project

You should be able to bootstrap for yourself by running `make bootstrap`.


1. Provision GCP project?
2. Create BQ dataset
3. Create BQ tables with schema
