"""
.. include:: ../../README.md
"""

from bioimageio.spec import build_description as build_description
from bioimageio.spec import dump_description as dump_description
from bioimageio.spec import load_dataset_description as load_dataset_description
from bioimageio.spec import load_description as load_description
from bioimageio.spec import (
    load_description_and_validate_format_only as load_description_and_validate_format_only,
)
from bioimageio.spec import load_model_description as load_model_description
from bioimageio.spec import save_bioimageio_package as save_bioimageio_package
from bioimageio.spec import (
    save_bioimageio_package_as_folder as save_bioimageio_package_as_folder,
)
from bioimageio.spec import save_bioimageio_yaml_only as save_bioimageio_yaml_only
from bioimageio.spec import validate_format as validate_format

from . import digest_spec as digest_spec
from ._prediction_pipeline import PredictionPipeline as PredictionPipeline
from ._prediction_pipeline import (
    create_prediction_pipeline as create_prediction_pipeline,
)
from ._resource_tests import load_description_and_test as load_description_and_test
from ._resource_tests import test_description as test_description
from ._resource_tests import test_model as test_model
from ._settings import settings as settings
from .axis import Axis as Axis
from .axis import AxisId as AxisId
from .block_meta import BlockMeta as BlockMeta
from .common import MemberId as MemberId
from .prediction import predict as predict
from .prediction import predict_many as predict_many
from .sample import Sample as Sample
from .tensor import Tensor as Tensor
from .utils import VERSION

__version__ = VERSION

# aliases
test_resource = test_description
load_resource = load_description
load_model = load_model_description
