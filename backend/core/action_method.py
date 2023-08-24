from core.exceptions import ObjectExistsError, ObjectNotFoundError
from rest_framework import status
from rest_framework.response import Response

# need to add constants for errors messages here
ERROR = 'error'


def check_objects(method, objects):
    """Метод для проверки соответствия метода и действия с объектами."""
    if not objects.exists() and method == 'DELETE':
        raise ObjectExistsError(f'{ERROR}')
    elif objects.exists() and method == 'POST':
        raise ObjectNotFoundError(f'{ERROR}')


def save_objects(request, target, 
                 serializer_class, response_serializer_class, data):
    """Метод для сохранения отношений субъекта и объекта."""
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    serializer = response_serializer_class(
        target, context={'request': request}
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# need to fix thing with data, it's not important to have it here
def save_delete_action(request, objects, target,
                       serializer_class, response_serializer_class, data):
    """Главный метод в декораторе action."""
    method = request.method
    try:
        check_objects(method=method, objects=objects)
    except (ObjectExistsError, ObjectNotFoundError) as error:
        return Response(
            {
                'error': str(error)
            }, status=status.HTTP_400_BAD_REQUEST
        )
    if method == 'POST':
        return save_objects(
            request=request,
            target=target,
            serializer_class=serializer_class,
            response_serializer_class=response_serializer_class,
            data=data
        )
    objects.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
