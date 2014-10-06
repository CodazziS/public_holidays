# -*- coding: utf-8 -*-


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def get_instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class calendars_factory(object):

    def __init__(self):

        self._registered_calendars = []  
        self._calendars_pool = {}

    def register(self, cal_class, string, country_code=None):
        
        if country_code is None:
            country_code = len(self._registered_calendars)

        self._registered_calendars.append({'class': cal_class,
                                           'string': string,
                                           'id': country_code})

    def _get_class_by_id(self, country_code):
        
        for cl in self._registered_calendars:
            if cl['id'] == country_code:
                return cl['class']
        return None        

    def get_calendar_by_id(self, country_code):

        try: 
            return self._calendars_pool[country_code]
        except KeyError:    
            self._calendars_pool[country_code] =\
                self._get_class_by_id(country_code)()
          
        return self._calendars_pool[country_code]

    def __getitem__(self, item):

        return self.get_calendar_by_id(item)

