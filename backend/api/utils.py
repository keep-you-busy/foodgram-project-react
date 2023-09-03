from functools import wraps


def check_is_flagged(model, relation_parameter):
    def decorator(func):
        @wraps(func)
        def wrapper(self, obj):
            user = self.context.get('request').user
            parameters = {
                'user': user,
                relation_parameter: obj
            }
            return user.is_authenticated and model.objects.filter(
                **parameters).exists()
        return wrapper
    return decorator
