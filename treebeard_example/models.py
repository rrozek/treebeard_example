from django.db import models

from treebeard.mp_tree import MP_Node


class Category(MP_Node):
    name = models.CharField(max_length=30)
    category_code = models.CharField(max_length=3)
    node_order_by = ['name']

    def __str__(self):
        return f'Category: {self.category_string_from_root} ({self.category_names_from_root})'

    @property
    def category_string_from_root(self):
        return self._category_from_root('category_code')

    @property
    def category_names_from_root(self):
        return self._category_from_root('name')

    def _category_from_root(self, property_name):
        path = []
        current_item = self
        parent = self.get_parent()
        while not current_item.is_root() and parent:
            path.append(getattr(current_item, property_name))
            current_item = parent
            parent = parent.get_parent()
        path.append(getattr(current_item, property_name))
        path.reverse()
        return '.'.join(path)


class Thing(models.Model):
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Kategoria', related_name='categories+')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'Thing {self.name} categorized as: {self.category_string}'

    @property
    def category_string(self):
        return ';'.join([cat.category_string_from_root for cat in self.categories.all()])

