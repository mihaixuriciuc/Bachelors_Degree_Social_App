def get_client_ip(request):

    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')  #IP LISTS  from the first one to the last one, are un antet daca trece prin proxy
    if forwarded:
        return forwarded.split(',')[0].strip()  #returns the first ip in the list
    return request.META.get('REMOTE_ADDR')