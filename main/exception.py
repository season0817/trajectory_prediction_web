from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response
from rest_framework import status


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    # 为空，drf 中没有对应的处理，自定义二次处理
    if response is None:
        # print(exc)
        #print('%s - %s - %s' % (context['view'], context['request'].method, exc))
        return Response({
            'detail': '服务器错误'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    return response