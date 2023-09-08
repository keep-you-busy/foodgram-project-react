def check_is_flagged(model, relation_parameter, user, obj):
    """Метод проверяет выбранное отношение между пользователем и объектом."""
    parameters = {
        'user': user,
        relation_parameter: obj
    }
    return user.is_authenticated and model.objects.filter(
        **parameters).exists()
