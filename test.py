class SetOnceMappingMixinSuper:

    def __setitem__(self, key, value):
        print('xa')

class SetOnceMappingMixin(SetOnceMappingMixinSuper):
    """自定义混入类"""
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        else:
            print('xsada')
        return super().__setitem__(key, value) # type: ignore


class SetOnceDict(SetOnceMappingMixin, dict):
    """自定义字典"""
    def __setitem__(self, key, value):
        print(f'Setting {key} to {value}')
        return super().__setitem__(key, value)
    pass


my_dict= SetOnceDict() 
try:
    my_dict['username'] = 'jackfrued'
    my_dict['username'] = 'hellokitty'
except KeyError:
    pass
print(my_dict)