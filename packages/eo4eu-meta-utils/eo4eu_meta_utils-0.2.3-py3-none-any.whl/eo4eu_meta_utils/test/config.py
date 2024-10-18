import copy
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .recipe import Recipe


class TestConfig:
    def __init__(self, recipes: list[Recipe], **kwargs):
        self._recipes = recipes
        self._attrs = kwargs

    def recipes(self) -> list[Recipe]:
        return self._recipes

    def to_dict(self) -> dict:
        result = copy.deepcopy(self._attrs)
        recipe_services = {
            recipe.name(): recipe.to_dict()
            for recipe in self._recipes
        }
        if "services" in result:
            result["services"] |= recipe_services
        else:
            result["services"] = recipe_services

        return result

    def to_yaml(self) -> str:
        return dump(self.to_dict(), Dumper = Dumper)

    def cleanup(self):
        shutil.rmtree(Recipe.LOCAL_CFG_DIR)

    def inputs(self) -> list[KafkaMessage]:
        result = []
        for recipe in self._recipes:
            result.extend(recipe.inputs())
        return result

    def outputs(self) -> list[KafkaMessage]:
        result = []
        for recipe in self._recipes:
            result.extend(recipe.outputs())
        return result
