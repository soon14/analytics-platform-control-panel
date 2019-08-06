import requests
import json


class Concourse:

    def __init__(self, config, team):
        self.config = config
        self.team = team
        self.base_url = config['base_url']
        self.api_url = f'{self.base_url}/api/v1'

    def get_token(self):
        response = requests.get(
            f'{self.api_url}/teams/{self.team}/auth/token',
            auth=(
                self.config[self.team]['username'],
                self.config[self.team]['password'],
            ),
        )
        return response.json()['value']

    def _request(self, method, url, token=None, **kwargs):
        token = self.get_token()
        return requests.request(
            method,
            f'{self.api_url}/teams/{self.team}/{url}',
            cookies={
                'ATC-Authorization': f'Bearer {token}',
            },
            **kwargs,
        )

    def get_pipelines(self):
        return self._request('GET', 'pipelines').json()

    def get_jobs(self, pipeline):
        return self._request('GET', f'pipelines/{pipeline}/jobs').json()

    def get_deploy_status(self, pipeline):
        jobs = self.get_jobs(pipeline)
        deploy = next(job for job in jobs if job['name'] == 'deploy')
        return deploy.get('finished_build', {}).get('status', 'unknown')
