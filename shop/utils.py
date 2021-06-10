def django_sub_dict(obj):
    #allowed_fields = obj._meta.fields # pick the list containing the requested fields
    sub_dict = {}
    for field in obj._meta.fields: # go through all the fields of the model (obj)
        if field.is_relation: # will result in true if it's a foreign key
            if getattr(obj, field.name):
                # call this function, with a new object, the model which is being referred to by the foreign key.
                sub_dict[field.name] = django_sub_dict(getattr(obj, field.name)) 
        else: # not a foreign key? Just include the value (e.g., float, integer, string)
            sub_dict[field.name] = getattr(obj, field.name)
            
    return sub_dict
