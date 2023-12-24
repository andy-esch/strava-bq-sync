.PHONY: test local

function_name = stravabqsync_listener
verify_token = desire-lines-cycling
project_id = progressor-341702
GCP_PUBSUB_TOPIC = "strava-webhook-events"
GCP_BIGQUERY_DATASET = "strava"

test:
	poetry run pytest tests/

local:
	poetry run functions-framework --target $(function_name) --debug

deploy:
	gcloud functions deploy $(function_name) \
	  --project=$(project_id) \
	  --runtime=python311 \
	  --trigger-topic=$(GCP_PUBSUB_TOPIC) \
	  --region=us-central1 \
	  --gen2 \
	  --memory=1024MB \
	  --set-env-vars='GCP_PROJECT_ID=$(project_id),GCP_BIGQUERY_DATASET=$(GCP_BIGQUERY_DATASET)' \
	  --set-secrets='GH_TOKEN=projects/79853619583/secrets/GitHubToken:latest,STRAVA_CLIENT_ID=projects/79853619583/secrets/StravaClientID:latest,STRAVA_CLIENT_SECRET=projects/79853619583/secrets/StravaClientSecret:latest,STRAVA_REFRESH_TOKEN=projects/79853619583/secrets/StravaRefreshToken:latest'


create-webhook:
	curl -X POST \
	  https://www.strava.com/api/v3/push_subscriptions \
	  -F client_id=$$(gcloud secrets versions access latest --secret=StravaClientID) \
	  -F client_secret=$$(gcloud secrets versions access latest --secret=StravaClientSecret) \
	  -F callback_url=$$(gcloud functions describe $(function_name) | yq '.url') \
	  -F verify_token=$(verify_token)


view-subscription:
	curl \
	  -G https://www.strava.com/api/v3/push_subscriptions \
	  -d client_id=$$(gcloud secrets versions access latest --secret=StravaClientID) \
	  -d client_secret=$$(gcloud secrets versions access latest --secret=StravaClientSecret)


delete-subscription:
	curl \
	  -X DELETE \
	  "https://www.strava.com/api/v3/push_subscriptions/252940?client_id=$$(gcloud secrets versions access latest --secret=StravaClientID)&client_secret=$$(gcloud secrets versions access latest --secret=StravaClientSecret)"
