import os

from openapi_core import Spec
from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from openapi_core.contrib.flask.decorators import FlaskOpenAPIResponse

from flask import current_app

spec = Spec.from_file_path(
    os.path.join("config", "openapi.json")
)
openapi = FlaskOpenAPIViewDecorator.from_spec(spec)
