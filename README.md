# recommendation-graphdb

## Getting setup

Lets use docker to help us set up an enviroment to

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
