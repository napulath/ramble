# Copyright 2022-2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# https://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

"""Schema for application specific experiment configuration file.

.. literalinclude:: _ramble_root/lib/ramble/ramble/schema/applications.py
   :lines: 12-
"""  # noqa E501

from llnl.util.lang import union_dicts
from ramble.schema.success_criteria import success_list_def

import ramble.schema.env_vars
import ramble.schema.types
import ramble.schema.variables
import ramble.schema.success_criteria
import ramble.schema.licenses


matrix_def = {
    'type': 'array',
    'default': [],
    'items': {'type': 'string'}
}

matrices_def = {
    'type': 'array',
    'default': [],
    'items': {
        'anyOf': [
            matrix_def,
            {
                'type': 'object',
                'default': {},
                'properties': {},
                'additionalProperties': matrix_def
            }
        ]
    }
}

custom_executables_def = {
    'type': 'object',
    'properties': {},
    'additionalProperties': {
        'type': 'object',
        'default': {
            'template': [],
            'use_mpi': False,
            'redirect': '{log_file}',
            'output_capture': ramble.schema.types.OUTPUT.DEFAULT
        },
        'properties': {
            'template': ramble.schema.types.array_or_scalar_of_strings_or_nums,
            'use_mpi': {'type': 'boolean'},
            'redirect': ramble.schema.types.string_or_num,
        }
    },
    'default': {},
}

executables_def = ramble.schema.types.array_of_strings_or_nums

internals_def = {
    'type': 'object',
    'default': {},
    'properties': {
        'custom_executables': custom_executables_def,
        'executables': executables_def,
    },
    'additionalProperties': False
}

chained_experiment_def = {
    'type': 'array',
    'default': [],
    'items': {
        'type': 'object',
        'default': {},
        'properties': union_dicts(
            {
                'name': {'type': 'string'},
                'command': {'type': 'string'},
                'order': {'type': 'string'},
            },
            ramble.schema.variables.properties
        ),
        'additionalProperties': False
    }
}

sub_props = union_dicts(
    ramble.schema.variables.properties,
    ramble.schema.success_criteria.properties,
    ramble.schema.env_vars.properties,
    {
        'internals': internals_def,
        'env-vars': ramble.schema.licenses.env_var_actions,
        'chained_experiments': chained_experiment_def,
        'template': {'type': 'boolean'},
    }
)

#: Properties for inclusion in other schemas
properties = {
    'applications': {
        'type': 'object',
        'default': {},
        'properties': {},
        'additionalProperties': {
            'type': 'object',
            'default': '{}',
            'additionalProperties': False,
            'properties': union_dicts(
                sub_props,
                {
                    'workloads': {
                        'type': 'object',
                        'default': {},
                        'properties': {},
                        'additionalProperties': {
                            'type': 'object',
                            'default': {},
                            'additionalProperties': False,
                            'properties': union_dicts(
                                sub_props,
                                {
                                    'experiments': {
                                        'type': 'object',
                                        'default': {},
                                        'properties': {},
                                        'additionalProperties': {
                                            'type': 'object',
                                            'default': {},
                                            'additionalProperties': False,
                                            'properties': union_dicts(
                                                sub_props,
                                                {
                                                    'matrix': matrix_def,
                                                    'matrices': matrices_def,
                                                    'internals': internals_def,
                                                    'success_criteria': success_list_def,
                                                }
                                            )
                                        }
                                    }
                                }
                            )
                        }
                    }
                }
            )
        }
    }
}

#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Ramble application configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties
}
