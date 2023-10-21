import os

from openapi_core import Spec
from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator

spec = Spec.from_file_path(
    os.path.join("config", "openapi.json")
)
openapi = FlaskOpenAPIViewDecorator.from_spec(spec)
