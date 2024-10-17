# Mortal Quest Devlopment Kit version 0.0.4
#
# Feel free to modify as you wish, but please credit me (AlexDM) if you publish it anywhere.
#
# Happy modding! 😀

import os
from datetime import datetime

def clear_logs():
    with open("build-logs.log", "w") as f:
        f.write("")

def log(msg, level="INFO"):
    with open("build-logs.log", "a") as f:
        now = datetime.now()
        f.write(f"{now.hour}-{now.minute}-{now.second} {level}: {msg}\n")

class Feature:
    def __init__(self, name, durablity=10) -> None:
        log(f"Loading Feature: {name}...")
        self.name = name

        if isinstance(durablity, (int, float)):
            self.durablity = durablity
        else:
            self.durablity = f"{durablity[0]}?{durablity[1]}"

class MQdk:
    def __init__(self):
        self.modify = self.modify()
        self.new = self.new()

        self.custom_recipes = []
        self.features = []

        self.name = "UNKNOWN"
        self.version = "UNKNOWN"

    def init(self):
        clear_logs()
        log("Thank you for using the Mortal Quest Devlopment Kit! Happy modding!")
        log("Loading MQ Features...")

        self.features.append(Feature("Chest", 1))
        self.features.append(Feature("Trees", 10))
        self.features.append(Feature("Knoxwood", 15))
        self.features.append(Feature("Grass", 0))
        self.features.append(Feature("Beehive", [3, 5]))
        self.features.append(Feature("Pebble", 3))
        self.features.append(Feature("Seashell", 1))
        self.features.append(Feature("Stone", 10))
        self.features.append(Feature("Iron", 15))
        self.features.append(Feature("Gold", 20))
        self.features.append(Feature("Emerald", 50))
        self.features.append(Feature("Diamond", 80))
        self.features.append(Feature("Titanium", 120))

        log("Features loaded!")

    def config(self, name="mod", version="0.0.1"):
        self.name = name
        self.version = version

    class Texture:
        def __init__(self, name, url) -> None:
            self.name = name
            self.url = url

    class new:
        def __init__(self) -> None:
            pass

        class Recipe:
            def __init__(self, output, input, slot_texture=None, output_amount=1, crafting_level=1) -> None:
                self.output = output
                self.input = input
                self.output_amount = output_amount
                self.crafting_level = crafting_level

                self.slot_texture = slot_texture

                mqdk.custom_recipes.append(self)

    class modify:
        def __init__(self) -> None:
            pass
            
        def Feature(self, feature, durablity=None):

            if durablity is not None:
                for f in mqdk.features:
                    if f.name == feature:
                        f.durablity = durablity
                        break

    def package(self, path="builds/"):
        warns = 0
        errors = 0

        print(f"Starting build of {self.name}-{self.version}")
        log(f"Packaging {self.name}-{self.version}...")

        if not os.path.exists(path):
            os.makedirs(path)
            log("Created builds folder")

        log(f"Writing {self.name}-{self.version}.mqm...")
        with open(f'{path}{self.name}-{self.version}.mqm', 'w') as f:

            if self.name == "UNKNOWN":
                log("Mod name is unknown, consider seting one using mqdk.config()!", "WARN")
                warns += 1

            f.write(f'mod>')
            f.write(f'{self.name};')
            f.write(f'{self.version};')
            f.write(f'<')

            log("Writing features...")
            f.write(f'features>')
            for feature in self.features:
                f.write(f'{feature.name}/')
                f.write(f'{feature.durablity};')
                f.write(f'\\')

                log(f"Wrote feature: {feature.name}")
            f.write(f'<')

            log("Writing recipes...")
            f.write(f'recipes.custom>')
            for recipe in self.custom_recipes:
                f.write(f'{recipe.output}/')
                f.write(f'{recipe.crafting_level};')

                f.write(f'{len(recipe.input)};[')
                for entry in recipe.input:
                    for key, value in entry.items():
                        f.write(f'{value}-')
                        f.write(f'{key};')
                f.write(f']')

                f.write(f'{recipe.output_amount};')
                f.write(f'[{recipe.slot_texture.name}-{recipe.slot_texture.url};]')
                f.write(f'\\')

                log(f"Wrote recipe: {recipe.output}")
            f.write(f'<')

        print(f"Finished build with {warns} warning(s) and {errors} error(s){". Please check build-logs.txt!" if warns or errors else ""}")

mqdk = MQdk()