def is_valid_user(request):
    """Authentication logic for every request of the django-sh app.
    Don't change the name of the function!!

    Parameters:
    request (Request): Django request object

    Returns:
    bool: Continue or not the execution
    """
    return None if request.user.is_superuser else "Unauthorized"
