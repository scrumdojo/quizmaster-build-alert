import requests
import time
from playsound import playsound

with open('github-token.txt', 'r') as file:
    GITHUB_TOKEN = file.read().strip()

BASE_URL = f'https://api.github.com/repos/scrumdojo/quizmaster/actions/workflows'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

workflows = requests.get(BASE_URL, headers=headers).json()
workflow = next((workflow for workflow in workflows['workflows'] if workflow['name'] == 'CI'), None)

runs_in_progress = []
runs_failed = []

# repeat every 30 seconds
while True:
    runs = requests.get(f'{workflow['url']}/runs', headers=headers).json()['workflow_runs']

    # remove completed successful runs from runs_in_progress
    for run_id in runs_in_progress:
        run = next((run for run in runs if run['id'] == run_id), None)
        if run is None or run['status'] == 'completed' and run['conclusion'] == 'success':
            runs_in_progress.remove(run_id)

    # add failed runs to runs_failed
    for run_id in runs_in_progress:
        run = next((run for run in runs if run['id'] == run_id), None)
        if run is None or run['status'] == 'completed' and run['conclusion'] == 'failure':
            runs_failed.append(run_id)
            runs_in_progress.remove(run_id)

    # add in_progress runs to runs_in_progress
    for run in runs:
        if run['status'] == 'in_progress' and run['id'] not in runs_in_progress:
            runs_in_progress.append(run['id'])

    print(f'Runs in progress: {runs_in_progress}')
    print(f'Runs failed: {runs_failed}')

    # play sound if any runs_failed size > 0
    if runs_failed:
        playsound('fuck.mp3')
        runs_failed = []

    time.sleep(30)
