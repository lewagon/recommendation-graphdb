from neo4j import GraphDatabase

class AddRecipes:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def complete_recipes(self):
        with self.driver.session() as session:
            session.execute_write(self._import_authors)
            session.execute_write(self._import_ingredients)
            session.execute_write(self._import_keywords)
            session.execute_write(self._import_diet_types)
            session.execute_write(self._import_collections)

    @staticmethod
    def _import_authors(tx):
        query = """
        CALL apoc.load.json('https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/stream_clean.json') YIELD value
        WITH value.page.article.id AS id,
            value.page.article.author AS author
        MERGE (a:Author {name: author})
        WITH a,id
        MATCH (r:Recipe {id:id})
        MERGE (a)-[:WROTE]->(r);
        """
        tx.run(query)

    @staticmethod
    def _import_ingredients(tx):
        query = """
        CALL apoc.load.json('https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/stream_clean.json') YIELD value
        WITH value.page.article.id AS id,
               value.page.recipe.ingredients AS ingredients
        MATCH (r:Recipe {id:id})
        FOREACH (ingredient IN ingredients |
          MERGE (i:Ingredient {name: ingredient})
          MERGE (r)-[:CONTAINS_INGREDIENT]->(i)
        );
        """
        tx.run(query)

    @staticmethod
    def _import_keywords(tx):
        query = """
        CALL apoc.load.json('https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/stream_clean.json') YIELD value
        WITH value.page.article.id AS id,
               value.page.recipe.keywords AS keywords
        MATCH (r:Recipe {id:id})
        FOREACH (keyword IN keywords |
          MERGE (k:Keyword {name: keyword})
          MERGE (r)-[:KEYWORD]->(k)
        );
        """
        tx.run(query)

    @staticmethod
    def _import_diet_types(tx):
        query = """
        CALL apoc.load.json('https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/stream_clean.json') YIELD value
        WITH value.page.article.id AS id,
               value.page.recipe.diet_types AS dietTypes
        MATCH (r:Recipe {id:id})
        FOREACH (dietType IN dietTypes |
          MERGE (d:DietType {name: dietType})
          MERGE (r)-[:DIET_TYPE]->(d)
        );
        """
        tx.run(query)

    @staticmethod
    def _import_collections(tx):
        query = """
        CALL apoc.load.json('https://raw.githubusercontent.com/neo4j-examples/graphgists/master/browser-guides/data/stream_clean.json') YIELD value
        WITH value.page.article.id AS id,
               value.page.recipe.collections AS collections
        MATCH (r:Recipe {id:id})
        FOREACH (collection IN collections |
          MERGE (c:Collection {name: collection})
          MERGE (r)-[:COLLECTION]->(c)
        );
        """
        tx.run(query)

if __name__ == "__main__":
    recipes = AddRecipes("bolt://database:7687", "neo4j", "abcd1234")
    recipes.complete_recipes()
    recipes.close()
