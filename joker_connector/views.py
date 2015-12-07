import os
import xmlrpclib

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from joker_common.views import DATA_PATH


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
    return Response(SC_ADMIN.job_modules())


@api_view(['GET'])
def list_profiles(request):
    if "module" in request.GET:
        module = request.GET["module"]
        return Response(SC_ADMIN.job_profiles(module))
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
            "content": SC_ADMIN.job_profile_pull(module, profile)
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_status(request):
    if "id" in request.GET:
        return Response(SC_ADMIN.job_status(request.GET["id"]))
    else:
        return Response(SC_ADMIN.job_status())


@api_view(['GET'])
def job_kill(request):
    if "id" in request.GET:
        job_id = request.GET["id"]
        try:
            SC_ADMIN.job_kill(job_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exp:
            return Response(str(exp), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_clear(request):
    return Response(SC_ADMIN.job_clear())


@api_view(['GET'])
def job_set_num_slots(request):
    if "slots" in request.GET:
        slots = request.GET["slots"]
        return Response({
            "slots": SC_ADMIN.job_set_num_slots(slots)
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def job_profile_push(request):
    if "module" in request.POST and "profile" in request.POST and "content" in request.POST:
        module = request.POST["module"]
        profile = request.POST["profile"]
        content = request.POST["content"]
        if "overwrite" in request.POST:
            overwrite = request.POST["overwrite"] == "true"
        else:
            overwrite = False
        return Response({
            "id": SC_ADMIN.job_profile_push(module, profile, content, overwrite)
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_top(request):
    if "id" in request.GET:
        job_id = request.GET["id"]
        try:
            SC_ADMIN.job_top(job_id)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as exp:
            return Response(str(exp), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_remove(request):
    if "id" in request.GET:
        job_id = request.GET["id"]
        try:
            SC_ADMIN.job_remove(job_id)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as exp:
            return Response(str(exp), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_submit(request):
    if "module" in request.GET and "profile" in request.GET:
        module = request.GET["module"]
        profile = request.GET["profile"]
        return Response({
            "id": SC_ADMIN.job_submit(module, profile)
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_reset(request):
    return Response(SC_ADMIN.job_reset())


@api_view(['GET'])
def job_profile_remove(request):
    if "module" in request.GET and "profile" in request.GET:
        module = request.GET["module"]
        profile = request.GET["profile"]
        try:
            SC_ADMIN.job_profile_remove(module, profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exp:
            return Response(str(exp), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_module_uninstall(request):
    if "module" in request.GET:
        module = request.GET["module"]
        try:
            SC_ADMIN.job_module_uninstall(module)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exp:
            return Response(str(exp), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_module_install(request):
    if "src" in request.GET:
        package_file = DATA_PATH + "module/" + request.GET["src"]
        try:
            return Response(SC_ADMIN.job_module_install(package_file))
        except Exception as exp:
            return Response(str(exp), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
