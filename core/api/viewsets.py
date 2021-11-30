import requests
from rest_framework import permissions
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from core.common.helpers import api_view

headers = {
    "Cookie": "_relevant_session=QTRGU1Aram9kNmRZcU5zdGpFOHl0UFlhY3ZhbngvWGE1QVdDN0VKS0o4N2NyN2N1eENYYm5GMEJBWEVSTzFndUpNbVRmWm9WMW1UZWtyYXZ5bnRTSnR0NjN3ckppK3RoOFNQL2pybGRjTUMwajQ3RFBJNzEvcEZqelo0dkUvK3JIVzV3MHpJY1o5c0djaFd5am5XelRXNXI0d3hoTHNJZUFEZ0pSYlg2WlVZPS0tMmdBWGlIRU8rSW5wOEk4WHFNR1hodz09--99f84dc8a5f639c47232d40c1189ad29f2b59d99"
}


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes([])
def api_report_aging_report(request):
    report_age = requests.get(
        'https://alliancech.relevant.healthcare/api/ar?summary_field=balance&groups%5B%5D=age',
        headers=headers
    )
    # report_location = requests.get(
    #     'https://alliancech.relevant.healthcare/api/ar?summary_field=balance&groups%5B%5D=location',
    #     headers=headers
    # )
    #
    # report_aging_payer_group = requests.get(
    #     'https://alliancech.relevant.healthcare/api/ar?summary_field=balance&groups%5B%5D=aging_payer_group',
    #     headers=headers
    # )
    #
    # report_balance = requests.get(
    #     'https://alliancech.relevant.healthcare/api/ar?summary_field=balance',
    #     headers=headers
    # )
    #
    # report_profiles = requests.get(
    #     'https://fast.trychameleon.com/observe/v2/profiles/61718997cd7d2a0013f465fd',
    #     headers=headers
    # )

    return Response({
        "results": report_age.text,
        # "report_location": report_location.text,
        # "report_aging_payer_group": report_aging_payer_group.text,
        # "report_balance": report_balance.text,
        # "report_profiles": report_profiles.text,
    })


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes([])
def api_report_by_location(request):
    report_location = requests.get(
        'https://alliancech.relevant.healthcare/api/ar?summary_field=balance&groups%5B%5D=location',
        headers=headers
    )

    return Response({"results": report_location.text})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes([])
def api_report_aging_payer_group(request):
    report_aging_payer_group = requests.get(
        'https://alliancech.relevant.healthcare/api/ar?summary_field=balance&groups%5B%5D=aging_payer_group',
        headers=headers
    )

    return Response({"results": report_aging_payer_group.text})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes([])
def api_report_balance(request):
    report_balance = requests.get(
        'https://alliancech.relevant.healthcare/api/ar?summary_field=balance',
        headers=headers
    )
    return Response({"results": report_balance.text})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes([])
def api_report_count(request):
    report_count = requests.get(
        'https://alliancech.relevant.healthcare/api/ar?summary_field=count',
        headers=headers
    )
    return Response({"results": report_count.text})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes([])
def api_report_profiles(request):
    report_profiles = requests.get(
        'https://fast.trychameleon.com/observe/v2/profiles/61718997cd7d2a0013f465fd',
        headers=headers
    )
    return Response({"results": report_profiles.text})
