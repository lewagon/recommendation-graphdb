# recommendation-graphdb

## Getting setup

Lets use docker to help us set up an environment to run the graph database in!

## Add the recipes

Add the recipe nodes into neo4j

```bash
python intial_recipes.py
```

Add all the other info into neo4j

```bash
python complete_recipes.py
```

Now we can build our recommendation system!

## Recommend!

Lets begin with a simple filter we have a few friends coming over one vegan and one is allergic to nuts. We also don't want to spend more than 20-25 mins cooking!

```sql
MATCH (r:Recipe)-[rel:DIET_TYPE]->(d:DietType)
WHERE r.skillLevel = 'Easy'
AND r.preparationTime > 1200
AND r.preparationTime < 1800
AND d.name = 'Vegan' OR d.name = 'Nut-free'
RETURN r, d, rel
```

Lets use what we have in our fridge!

```sql
MATCH (r:Recipe)-[rel:CONTAINS_INGREDIENT]->(i:Ingredient)
WHERE i.name IN ['double cream', 'caramel']
WITH r, COLLECT(i) AS ingredients, COLLECT(rel) AS relationships
WHERE SIZE(ingredients) = 2
RETURN r, ingredients, relationships
```

We really like 'Pull-apart chicken with green curry & lime leaf dressing' how can we find similar recipes?

```sql
WITH "Pull-apart chicken with green curry & lime leaf dressing" AS favoriteRecipeName

MATCH (fav:Recipe {name: favoriteRecipeName})
OPTIONAL MATCH (fav)-[:KEYWORD]->(k:Keyword)
OPTIONAL MATCH (fav)-[:CONTAINS_INGREDIENT]->(i:Ingredient)
OPTIONAL MATCH (fav)-[:COLLECTION]->(favCollection:Collection)
OPTIONAL MATCH (fav)-[:DIET_TYPE]->(d:DietType)

MATCH (rec:Recipe)-[:KEYWORD]->(k)
WHERE rec <> fav
WITH fav, i, favCollection, d, rec, COUNT(k) AS sharedKeywords
MATCH (rec)-[:CONTAINS_INGREDIENT]->(i)
WHERE rec <> fav
WITH fav, favCollection, d, rec, sharedKeywords, COUNT(i) AS sharedIngredients
WHERE NOT (rec)-[:COLLECTION]->(favCollection)

RETURN rec.name AS RecommendedRecipe, sharedKeywords, sharedIngredients
ORDER BY sharedKeywords DESC, sharedIngredients DESC
LIMIT 10
```

```sql
WITH "Pull-apart chicken with green curry & lime leaf dressing" AS favoriteRecipeName

MATCH (fav:Recipe {name: favoriteRecipeName})
OPTIONAL MATCH (fav)-[:CONTAINS_INGREDIENT]->(i:Ingredient)
OPTIONAL MATCH (fav)-[:KEYWORD]->(k:Keyword)
OPTIONAL MATCH (fav)<-[:WROTE]-(a:Author)

WITH fav, i, k, a, COUNT(a) AS authorInfluence
ORDER BY authorInfluence DESC
LIMIT 10

MATCH (rec:Recipe)-[:CONTAINS_INGREDIENT]->(i), (rec)-[:KEYWORD]->(k), (rec)<-[:WROTE]-(a)
WHERE rec <> fav
WITH rec, COUNT(i) + COUNT(k) AS relevanceScore
ORDER BY relevanceScore DESC
LIMIT 10

RETURN rec.name AS RecommendedRecipe, relevanceScore
```

These look similar which is great but what about if we want to leverage the graph to find things related that are not too similar!

```sql
WITH "Pull-apart chicken with green curry & lime leaf dressing" AS favoriteRecipeName

MATCH (fav:Recipe {name: favoriteRecipeName})

MATCH (fav)-[:CONTAINS_INGREDIENT|KEYWORD|WROTE*4]-(rec:Recipe)-[:DIET_TYPE]->(d:DietType {name: "Vegan"})
WHERE fav <> rec
WITH rec, COUNT(*) AS pathsOfLength4
ORDER BY pathsOfLength4 DESC
LIMIT 5

RETURN rec.name AS RecommendedRecipe, pathsOfLength4
```

Super intresting results if you want to dig deeper you can being here (https://neo4j.com/docs/getting-started/appendix/tutorials/guide-build-a-recommendation-engine/) and keep digging!
