"""Define the configuration fields for the paint_manager application."""

from df_config.config.fields import CharConfigField, ChoiceConfigFile, IntegerConfigField

INI_MAPPING = [
    CharConfigField(
        "auth.remote_user_header",
        "DF_REMOTE_USER_HEADER",
        help_str='Set it if the reverse-proxy authenticates users, a common value is "HTTP_REMOTE_USER". '
        "Note: the HTTP_ prefix is automatically added, just set REMOTE_USER in the "
        "reverse-proxy configuration. ",
        env_name="REMOTE_USER_HEADER",
    ),
    CharConfigField(
        "global.admin_email",
        "ADMIN_EMAIL",
        help_str="e-mail address for receiving logged errors",
    ),
    CharConfigField(
        "global.language_code",
        "LANGUAGE_CODE",
        help_str="default to fr_FR",
        env_name="LANGUAGE_CODE",
    ),
    CharConfigField(
        "global.server_url",
        "SERVER_BASE_URL",
        help_str="Public URL of your website. \n"
        'Default to "http://{listen_address}/" but should '
        "be different if you use a reverse proxy like "
        "Apache or Nginx. Example: http://www.example.org/.",
        env_name="SERVER_URL",
    ),
    IntegerConfigField(
        None,
        "LISTEN_PORT",
        help_str="port to listen to (force to listen on 0.0.0.0:$PORT).",
        env_name="PORT",
    ),
    CharConfigField(
        "global.time_zone",
        "TIME_ZONE",
        help_str="default to Europe/Paris",
        env_name="TIME_ZONE",
    ),
    CharConfigField(None, "DATABASE_URL", help_str="URL of the database", env_name="DATABASE_URL"),
    CharConfigField(
        None,
        "EMAIL_HOST_URL",
        help_str="SMTP server for sending admin emails. \n"
        "smtp+tls://account@example.com:password@smtp.example.com:587/",
        env_name="EMAIL_HOST_URL",
    ),
    CharConfigField(
        "global.log_remote_url",
        "LOG_REMOTE_URL",
        help_str="Send logs to a syslog service. \n"
        "Examples: syslog+tcp://localhost:514/user, syslog:///local7 "
        "or syslog:///dev/log/daemon.",
        env_name="LOG_REMOTE_URL",
    ),
    CharConfigField(
        "global.log_sentry_dsn",
        "SENTRY_DSN",
        help_str="sentry DSN (see https://sentry.io/)",
        env_name="SENTRY_DSN",
    ),
    CharConfigField(
        None,
        "COMMON_REDIS_URL",
        help_str="Redis database URL, for all redis things.",
        env_name="REDIS_URL",
    ),
    CharConfigField(
        "global.log_directory",
        "LOG_DIRECTORY",
        help_str="Write all local logs to this directory.",
        env_name="LOG_DIRECTORY",
    ),
    ChoiceConfigFile(
        "global.log_level",
        "LOG_LEVEL",
        help_str="Log level (one of 'debug', 'info', 'warn', 'error' or 'critical').",
        choices={
            "debug": "DEBUG",
            "info": "INFO",
            "warn": "WARN",
            "error": "ERROR",
            "critical": "CRITICAL",
        },
        env_name="LOG_LEVEL",
    ),
]
