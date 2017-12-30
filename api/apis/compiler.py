from flask import request
from flask_restplus import Namespace, Resource, fields

from compiler.manager import GccManager
from . import data


# Defining the name space for Catt cafile
api = Namespace('compiler',description='Check if the given c source code can be compiled successfully.')


# Defining raw code model
CCode = api.model('CCode',{
    'raw_c_code': fields.String(
        required=True,
        description='The C source code to be compiled.',
        default=data.RAW_C_CODE
    )

})


@api.route('')
class Gcc(Resource):
    """Deals with the parallelization of C99 Source code with OpenMP directives."""

    def head(self):
        """Used for clients to check if the resource is available."""
        data = {}
        return data

    @api.expect(CCode)
    def post(self):
        """Check if a C program compile correctly."""

        data = request.json
        raw_c_code = data['raw_c_code']

        manager = GccManager()
        stdout, stderror = manager.compile_raw_code(raw_c_code)

        if stderror:
            response = (stderror, 400)
        else:
            response = ({'message':'Compilation successfull !!'}, 200)

        return response