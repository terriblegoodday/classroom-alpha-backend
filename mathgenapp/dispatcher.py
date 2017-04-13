import importlib
try:
    from mathgenapp.settings import settings as s
except ImportError:
    s = {
    'quadequationgenerator': {
        'RANGE_OF_GENERATION': [-10, 10],
    },
    'linearinequalitiesgenerator': {
        
    }
}
import logging
logger = logging.getLogger(__file__)
# Task Generators
import_stack = ['quadequationgenerator', 'quadequationgeneratorhard', 'quadequationgeneratoreasy',
 'linearinequalitiesgenerator', 'logequationsgenerator',
 'logequationsgeneratoreasy', 'logequationsgeneratorhard']
generators = {} # DO NOT DELETE UNDER ANY CIRCUMSTANCES || НЕ УДАЛЯТЬ, ИНАЧЕ БУДЕТ ОЧЕ ПЛОХО

for i in import_stack:
    generators[i] = importlib.import_module('mathgenapp.generators.' + i)

class NoSuchGeneratorError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    print("Генератор квадратных уравнений. Консольный режим.")
    gen_id = input("Какой генератор вы хотите запустить? [gen_id]: ")
    if generators.get(gen_id):
        print(generators[gen_id].title)
        print(generators[gen_id].generate(s[gen_id]))
    else:
        raise NoSuchGeneratorError(gen_id)

else:
    def generate(gen_id):
        if generators.get(gen_id):
            task = generators[gen_id].generate(s.get(gen_id))
            logger.warn(str(task))
            return task
        else: raise NoSuchGeneratorError(gen_id)
    
    def getAvailableGenerators():
        availableGenerators = []
        for i, b in generators.items():
            availableGenerators.append(
                {
                    "title": b.title,
                    "description": b.description,
                    "gen_id": i
                }
            )
        return availableGenerators
