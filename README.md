# Strava to BigQuery Sync

Sync Strava data to Google BigQuery using Strava's Webhooks. Currently, this function
receives PubSub messages from a Push Subscription. The messages on that subscription
come from a PubSub topic that is published from a Cloud Function that essentially
only relays Strava Webhook messages to the PubSub topic. That project, `desire-lines`,
will be open-sourced separately.

## Description

This Cloud Function appends created (new) activities to an activities table. It will
also maintain a separate table that will keep track of the state of activies (e.g.,
updates and deletes). For updates, titles (and other attributes) can change. For
deletes, deleted activities have their IDs logged so that a final view will give the
current state of Strava Activities in an account.


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
