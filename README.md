# DSL for elasticsearch

## Motivation
An emerging trend in recent year for software, including mongodb, elasticsearch and Chef, is to expose an JSON interface to accept complex requests. They give up the traditional SQL query and adopt JSON as the text encoding of abstract syntax tree. Therefore, whenever you are making up a request to these services, you are actually hand coding an abstract syntax tree in JSON. Although it is flexible and easy to extend, it is also error prone and hard to maintain. A common solution for this is to write a Domain Specific Language. And with python’s language design, a naive and natural solution is to use Class to denote AST node and Visitor pattern to code-generate the underlying JSON.


## Installation

``
pip install .
``


## Examples

### Nested Aggregation

``query_py_obj`` in the following code snippet contains the generated AST. Just ``json.dumps(query_py_obj)`` and you would get the JSON request to elasticsearch

```
    nested_agg = ast.NestedAggregation("name", "tags", ast.TermsAggregation("tags.name", size=20, order_type="_count", order="desc", min_doc_count=100))
    aggregation = ast.TopLevelAggregation("tag", nested_agg)
    ast_root = ast.TopLevelQuery(MatchAllQuery(), aggs=[aggregation])

    codegen = CodeGeneratorVisitor()
    codegen.visit(ast_root)
    query_py_obj = codegen.query
```

### Nested Query

```
    and_clauses = []
    and_clauses.append(ast.GeoDistanceFilter("geocode", user.geocode["latitude"], user.geocode["longitude"], 10))

    tag_names = []
    should_clauses= []
    for t, ind in tags:
        should_clauses.append(ast.TermQuery("tags.name", t.name.lower()))

    nested_queries= ast.BoolQuery(should=should_clauses)
    f = ast.NestedQuery("tags", nested_queries)

    query = ast.FilteredQuery(f, ast.AndFilter(and_clauses))
    query_size = 20
    query_from = 0
    ast_root = ast.TopLevelQuery(query, query_size, query_from, sort={"_score": {"order": "desc"}})

    codegen = CodeGeneratorVisitor()
    codegen.visit(ast_root)
    query_py_obj = codegen.query
```
