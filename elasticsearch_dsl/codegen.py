# -*- coding: utf-8 -*-

from __future__ import (absolute_import, print_function, unicode_literals, division)

from elasticsearch_dsl.ast import *
import elasticsearch_dsl.visitor as v
import datetime


class CodeGeneratorVisitor():
    def __init__(self):
        self.query = dict()
        self.cursor = self.query

    @v.on('node')
    def visit(self, node):
        """This is the generic method"""
        pass

    @v.when(TopLevelQuery)
    def visit(self, node):
        self.cursor["query"] = dict()

        if node.q_size:
            self.cursor["size"] = node.q_size

        if node.q_from:
            self.cursor["from"] = node.q_from

        if node.sort:
            self.cursor["sort"] = node.sort

        current_cursor = self.cursor
        self.cursor = self.cursor["query"]

        node.query.accept(self)

        self.cursor = current_cursor

        if node.aggs:
            self.cursor["aggs"] = dict()

            current_cursor = self.cursor
            for idx, agg in enumerate(node.aggs):
                self.cursor = self.cursor["aggs"]
                node.aggs[idx].accept(self)
                self.cursor = current_cursor


    @v.when(FilteredQuery)
    def visit(self, node):
        self.cursor["filtered"] = {
            "query": dict(),
            "filter": dict()
        }

        current_cursor = self.cursor

        self.cursor = self.cursor["filtered"]["query"]
        node.query.accept(self)
        self.cursor = current_cursor

        self.cursor = self.cursor["filtered"]["filter"]
        node.filter.accept(self)
        self.cursor = current_cursor


    @v.when(MatchQuery)
    def visit(self, node):
        self.cursor["match"] = dict()
        self.cursor["match"][node.field_name] = {
            "query": node.text_query,
            "type": node.query_type,
            "analyzer": node.analyzer
        }


    @v.when(MatchAllQuery)
    def visit(self, node):
        self.cursor["match_all"] = dict()


    @v.when(TermQuery)
    def visit(self, node):
        self.cursor["term"] = dict()
        self.cursor["term"][node.field_name] = node.value
        self.cursor["term"]["boost"] = node.boost


    @v.when(NestedQuery)
    def visit(self, node):
        if isinstance(node.queries, list):
            self.cursor["nested"] = {
                "path": node.path,
                "query": [dict() for i in range(0, len(node.queries))]
            }

            current_cursor = self.cursor
            for idx, clause in enumerate(node.queries):
                self.cursor = self.cursor["nested"]["query"][idx]
                node.queries[idx].accept(self)
                self.cursor = current_cursor
        else:
            self.cursor["nested"] = {
                "path": node.path,
                "query": dict()
            }

            current_cursor = self.cursor
            self.cursor = self.cursor["nested"]["query"]
            node.queries.accept(self)
            self.cursor = current_cursor


    @v.when(BoolQuery)
    def visit(self, node):
        self.cursor["bool"] = dict()

        current_cursor = self.cursor

        if node.must:
            if isinstance(node.must, list):
                self.cursor["bool"]["must"] = [dict() for i in range(0, len(node.must))]

                current_cursor = self.cursor
                for idx, clause in enumerate(node.must):
                    self.cursor = self.cursor["bool"]["must"][idx]
                    node.must[idx].accept(self)
                    self.cursor = current_cursor
            else:
                self.cursor["bool"]["must"] = dict()

                current_cursor = self.cursor
                self.cursor = self.cursor["bool"]["must"]
                node.must.accept(self)
                self.cursor = current_cursor


        if node.must_not:
            if isinstance(node.must_not, list):
                self.cursor["bool"]["must_not"] = [dict() for i in range(0, len(node.must_not))]

                current_cursor = self.cursor
                for idx, clause in enumerate(node.must_not):
                    self.cursor = self.cursor["bool"]["must_not"][idx]
                    node.must_not[idx].accept(self)
                    self.cursor = current_cursor
            else:
                self.cursor["bool"]["must_not"] = dict()

                current_cursor = self.cursor
                self.cursor = self.cursor["bool"]["must_not"]
                node.must_not.accept(self)
                self.cursor = current_cursor


        if node.should:
            if isinstance(node.should, list):
                self.cursor["bool"]["should"] = [dict() for i in range(0, len(node.should))]

                current_cursor = self.cursor
                for idx, clause in enumerate(node.should):
                    self.cursor = self.cursor["bool"]["should"][idx]
                    node.should[idx].accept(self)
                    self.cursor = current_cursor
            else:
                self.cursor["bool"]["should"] = dict()

                current_cursor = self.cursor
                self.cursor = self.cursor["bool"]["should"]
                node.should.accept(self)
                self.cursor = current_cursor


    @v.when(Range)
    def visit(self, node):
        if node.lower_bound:
            if type(node.lower_bound) is datetime.datetime:
                self.cursor["gte"] = datetime.datetime.strftime(node.lower_bound, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                self.cursor["gte"] = node.lower_bound

        if node.upper_bound:
            if type(node.upper_bound) is datetime.datetime:
                self.cursor["le"] = datetime.datetime.strftime(node.upper_bound, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                self.cursor["le"] = node.upper_bound


    @v.when(HasChildFilter)
    def visit(self, node):
        self.cursor["has_child"] = dict()
        self.cursor["has_child"]["type"] = node.doc_type
        self.cursor["has_child"]["filter"] = dict()

        current_cursor = self.cursor
        self.cursor = self.cursor["has_child"]["filter"]

        node.clause.accept(self)

        self.cursor = current_cursor


    @v.when(MatchAllFilter)
    def visit(self, node):
        self.cursor["match_all"] = dict()


    @v.when(RangeFilter)
    def visit(self, node):
        self.cursor["range"] = dict()
        self.cursor["range"][node.field_name] = dict()

        current_cursor = self.cursor
        self.cursor = self.cursor["range"][node.field_name]

        node.range.accept(self)

        self.cursor = current_cursor


    @v.when(BoolFilter)
    def visit(self, node):
        self.cursor["bool"] = dict()

        current_cursor = self.cursor

        if node.must:
            if isinstance(node.must, list):
                self.cursor["bool"]["must"] = [dict() for i in range(0, len(node.must))]

                current_cursor = self.cursor
                for idx, clause in enumerate(node.must):
                    self.cursor = self.cursor["bool"]["must"][idx]
                    node.must[idx].accept(self)
                    self.cursor = current_cursor
            else:
                self.cursor["bool"]["must"] = dict()

                current_cursor = self.cursor
                self.cursor = self.cursor["bool"]["must"]
                node.must.accept(self)
                self.cursor = current_cursor


        if node.must_not:
            if isinstance(node.must_not, list):
                self.cursor["bool"]["must_not"] = [dict() for i in range(0, len(node.must_not))]

                current_cursor = self.cursor
                for idx, clause in enumerate(node.must_not):
                    self.cursor = self.cursor["bool"]["must_not"][idx]
                    node.must_not[idx].accept(self)
                    self.cursor = current_cursor
            else:
                self.cursor["bool"]["must_not"] = dict()

                current_cursor = self.cursor
                self.cursor = self.cursor["bool"]["must_not"]
                node.must_not.accept(self)
                self.cursor = current_cursor


        if node.should:
            if isinstance(node.should, list):
                self.cursor["bool"]["should"] = [dict() for i in range(0, len(node.should))]

                current_cursor = self.cursor
                for idx, clause in enumerate(node.should):
                    self.cursor = self.cursor["bool"]["should"][idx]
                    node.should[idx].accept(self)
                    self.cursor = current_cursor
            else:
                self.cursor["bool"]["should"] = dict()

                current_cursor = self.cursor
                self.cursor = self.cursor["bool"]["should"]
                node.should.accept(self)
                self.cursor = current_cursor



    @v.when(AndFilter)
    def visit(self, node):
        self.cursor["and"] = [dict() for i in range(0, len(node.clauses))]

        current_cursor = self.cursor
        for idx, clause in enumerate(node.clauses):
            self.cursor = self.cursor["and"][idx]
            node.clauses[idx].accept(self)
            self.cursor = current_cursor


    @v.when(OrFilter)
    def visit(self, node):
        self.cursor["or"] = [dict() for i in range(0, len(node.clauses))]

        current_cursor = self.cursor
        for idx, clause in enumerate(node.clauses):
            self.cursor = self.cursor["or"][idx]
            node.clauses[idx].accept(self)
            self.cursor = current_cursor


    @v.when(NotFilter)
    def visit(self, node):
        self.cursor["not"] = dict()

        current_cursor = self.cursor
        self.cursor = self.cursor["not"]
        node.clause.accept(self)
        self.cursor = current_cursor


    @v.when(TermFilter)
    def visit(self, node):
        self.cursor["term"] = dict()
        self.cursor["term"][node.field_name] = node.value


    @v.when(TermsFilter)
    def visit(self, node):
        self.cursor["terms"] = dict()
        self.cursor["terms"][node.field_name] = node.values
        self.cursor["terms"]["execution"] = "bool"


    @v.when(NestedFilter)
    def visit(self, node):
        if isinstance(node.filters, list):
            self.cursor["nested"] = {
                "path": node.path,
                "filter": [dict() for i in range(0, len(node.filters))]
            }

            current_cursor = self.cursor
            for idx, clause in enumerate(node.filters):
                self.cursor = self.cursor["nested"]["filter"][idx]
                node.filters[idx].accept(self)
                self.cursor = current_cursor
        else:
            self.cursor["nested"] = {
                "path": node.path,
                "filter": dict()
            }

            current_cursor = self.cursor
            self.cursor = self.cursor["nested"]["filter"]
            node.filters.accept(self)
            self.cursor = current_cursor



    @v.when(MissingFilter)
    def visit(self, node):
        self.cursor["missing"] = {
            "field": node.field_name
        }

        if node.existence:
            self.cursor["missing"]["existence"] = True
        else:
            self.cursor["missing"]["existence"] = False


        if node.null_value:
            self.cursor["missing"]["null_value"] = True
        else:
            self.cursor["missing"]["null_value"] = False


    @v.when(GeoDistanceFilter)
    def visit(self, node):
        self.cursor["geo_distance"] = {
            "distance": "%skm" %node.distance_in_km
        }

        self.cursor["geo_distance"][node.field_name] = {
            "lat": node.center_lat,
            "lon": node.center_lng
        }


    @v.when(TopLevelAggregation)
    def visit(self, node):
        self.cursor[node.field_name] = dict()

        current_cursor = self.cursor
        self.cursor = self.cursor[node.field_name]
        node.agg.accept(self)
        self.cursor= current_cursor


    @v.when(TermsAggregation)
    def visit(self, node):
        self.cursor["terms"] = dict()
        self.cursor["terms"]["field"] = node.field_name
        self.cursor["terms"]["size"] = node.size


    @v.when(SumAggregation)
    def visit(self, node):
        self.cursor["sum"] = dict()
        self.cursor["sum"]["field"] = node.field_name


    @v.when(AvgAggregation)
    def visit(self, node):
        self.cursor["avg"] = dict()
        self.cursor["avg"]["field"] = node.field_name


    @v.when(StatsAggregation)
    def visit(self, node):
        self.cursor["stats"] = dict()
        self.cursor["stats"]["field"] = node.field_name


    @v.when(MinAggregation)
    def visit(self, node):
        self.cursor["min"] = dict()
        self.cursor["min"]["field"] = node.field_name


    @v.when(MaxAggregation)
    def visit(self, node):
        self.cursor["max"] = dict()
        self.cursor["max"]["field"] = node.field_name


    @v.when(ValueAccountAggregation)
    def visit(self, node):
        self.cursor["value_count"] = dict()
        self.cursor["value_count"]["field"] = node.field_name
