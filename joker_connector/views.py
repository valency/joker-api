import os
import xmlrpclib

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class SmartCubeAdminClient(xmlrpclib.ServerProxy):
    def __init__(self, host, port, rpc_path='/RPC2'):
        xmlrpclib.ServerProxy.__init__(
            self, 'http://{}:{}{}'.format(host, port, rpc_path), allow_none=True
        )


SC_ADMIN = SmartCubeAdminClient(
    host=os.environ.get('SMARTCUBE_ADMIN_CORE_HOST', 'scworker00'),
    port=int(os.environ.get('SMARTCUBE_ADMIN_CORE_PORT', '19800'))
)


@api_view(['GET'])
def list_modules(request):
    return Response(SC_ADMIN.job_list_modules())


@api_view(['GET'])
def list_profiles(request):
    if "module" in request.GET:
        return Response({
            "module": request.GET["module"],
            "profiles": SC_ADMIN.job_list_profiles(request.GET["module"])
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_profile(request):
    if "module" in request.GET and "profile" in request.GET:
        module = request.GET["module"]
        profile = request.GET["profile"]
        return Response({
            "module": module,
            "profile": profile,
            "content": SC_ADMIN.job_profile(module, profile)
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
