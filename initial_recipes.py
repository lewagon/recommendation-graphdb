from neo4j import GraphDatabase

class AddRecipes:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_recipes(self):
        with self.driver.session() as session:
            greeting = session.execute_write(self._load_and_update_recipes)
            print(greeting)

    @staticmethod
    def _load_and_update_recipes(tx):
        query = """
        CALL apoc.load.json('https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/stream_clean.json') YIELD value
        WITH value.page.article.id AS id,
            value.page.title AS title,
            value.page.article.description AS description,
            value.page.recipe.cooking_time AS cookingTime,
            value.page.recipe.prep_time AS preparationTime,
            value.page.recipe.skill_level AS skillLevel
        MERGE (r:Recipe {id: id})
        SET r.cookingTime = cookingTime,
            r.preparationTime = preparationTime,
            r.name = title,
            r.description = description,
            r.skillLevel = skillLevel;
        """
        tx.run(query)



if __name__ == "__main__":
    recipes = AddRecipes("bolt://database:7687", "neo4j", "abc123")
    recipes.add_recipes()
    recipes.close()
