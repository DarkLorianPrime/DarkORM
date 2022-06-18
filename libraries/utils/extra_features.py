class Singleton(object):
    _instance = None

    def __new__(cls):
        """
        Создает новый объект класса если такового не существует, или же просто возвращает существующий
        """
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance
