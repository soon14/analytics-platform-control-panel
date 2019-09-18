from fly import Fly


class Concourse:

    def __init__(self):
        self._fly = Fly(concourse_url=settings.CONCOURSE['url'], **kwargs)
        self._fly.get_fly()
        self._fly.login(
            username=settings.CONCOURSE['username'],
            password=settings.CONCOURSE['password'],
            team_name=settings.CONCOURSE['team_name'],
        )

    def set_pipeline(name, yaml_filepath, vars={}):
        vars = [
            f'--var={name}={value}'
            for name, value in vars.items()
        ]
        self._fly.run(
            'set-pipeline',
            f'--pipeline={name}',
            f'--config={yaml_filepath}',
            f'--non-interactive',
            *vars,
        )

    def destroy_pipeline(name):
        self._fly.run(
            'destroy-pipeline',
            f'--pipeline={name}',
            f'--non-interactive',
        )

