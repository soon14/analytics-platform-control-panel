from controlpanel.settings.common import *


# Enable debugging
DEBUG = True

# Allow all hostnames to access the server
ALLOWED_HOSTS = "*"

# Reduce log level of Django internals
LOGGING["loggers"]["django"] = {"handlers": ["console"], "level": "WARNING"}

# Enable Django debug toolbar
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS.extend([
    "debug_toolbar",
    "requests_toolbar",
    "elastic_panel",
])
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # Jinja2 not supported
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'requests_toolbar.panels.RequestsDebugPanel',
    'elastic_panel.panel.ElasticDebugPanel',
]
INTERNAL_IPS = ['127.0.0.1']