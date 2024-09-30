# bsky-post-counter

Count bsky posts and record with pixela..

## Require

* Python 3.9
* Poetry
* Your Bluesky Account
  * handle
  * app password
* [Optional] Your Pixela Account and Graph
  * Pixela API document: https://docs.pixe.la/

## Usage

1. Clone this repository
2. Install dependencies
3. Set environment variables
4. Run!

```console
$ git clone https://github.com/ryosms/bsky-post-counter.git
$ cd bsky-post-counter
$ poetry install
$ export BSKY_PASSWORD=<your-bsky-app-password>
$ export PIXELA_API_TOKEN=<your-pixela-token>
$ poetry run bsky-counter  \
    -u <your-handle> \
    -t <your-timezone> \
    -p <your-pixela-username> \
    -g <your-pixela-graph-id> \
    --post-summary
```

## Run on GitHub Actions

1. Fork this repository
2. Set Actions Variables
  * open: `settings` -> `Secrets and variables` -> `Actions`
  * At `Secrets` tab, click `New repository secret` and register below
    * `BSKY_PASSWORD`: your Bluesky App password
    * `PIXELA_API_TOKEN`: [Optional] your Pixela token if you want to record with Pixela
  * At `Variables` tab, click `New repository variables` and register below
    * `BSKY_HANDLE`: your Bluesky handle (or email address or did)
    * `TIMEZONE`: [Optional] your timezone(eg. `Asia/Tokyo` / `utc` / etc...)
    * `PIXELA_USER`: [Optional] your Pixela username if you want to record with Pixela
    * `PIXELA_GRAPH_ID`: [Optional] your Pixela graph id if you want to record with Pixela
    * `POST_FLAG`: [Optional] set `--post-summary` if you want to post aggregated summary to Bluesky
    * `LOGGING_FLAG`: [Optional] set `-vv` for debug log
3. Edit `schedule cron` option on `.github/workflows/scheduled_aggreagte.yml` 
4. Invoke Actions or wait scheduled Actions

See [Actions yaml file](.github/workflows/scheduled_aggregate.yml) for detail
