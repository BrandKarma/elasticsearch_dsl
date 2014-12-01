# -*- coding: utf-8 -*-

from __future__ import (absolute_import, print_function, unicode_literals, division)


class BaseNode:
    def accept(self, visitor):
        visitor.visit(self)


class TopLevelQuery(BaseNode):
    def __init__(self, query, q_size=None, q_from=None, aggs=None, sort=None):
        self.query = query
        self.q_size = q_size
        self.q_from = q_from
        self.aggs = aggs
        self.sort = sort


class FilteredQuery(BaseNode):
    def __init__(self, query, filter):
        self.query = query
        self.filter = filter


class MatchQuery(BaseNode):
    def __init__(self, field_name, text_query, query_type, analyzer):
        self.field_name = field_name
        self.text_query = text_query
        self.query_type = query_type
        self.analyzer = analyzer


class MatchAllQuery(BaseNode):
    def __init__(self):
        pass


class Range(BaseNode):
    #FIXME: hard-code to half-close range at this moment
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound


class HasChildFilter(BaseNode):
    def __init__(self, clause, doc_type):
        self.clause = clause
        self.doc_type = doc_type


class MatchAllFilter(BaseNode):
    def __init__(self):
        pass


class RangeFilter(BaseNode):
    def __init__(self, field_name, range):
        self.field_name = field_name
        self.range = range


class BoolFilter(BaseNode):
    def __init__(self, must=None, must_not=None, should=None):
        self.must = must
        self.must_not = must_not
        self.should = should


class AndFilter(BaseNode):
    def __init__(self, clauses):
        self.clauses = clauses


class OrFilter(BaseNode):
    def __init__(self, clauses):
        self.clauses = clauses


class NotFilter(BaseNode):
    def __init__(self, clause):
        self.clause = clause


class TermFilter(BaseNode):
    def __init__(self, field_name, value):
        self.field_name = field_name
        self.value = value


class TermsFilter(BaseNode):
    def __init__(self, field_name, values, execution):
        self.field_name = field_name
        self.values = values
        self.execution = execution


class NestedFilter(BaseNode):
    def __init__(self, path, filters):
        self.path = path
        self.filters = filters


class MissingFilter(BaseNode):
    def __init__(self, field_name, existence=True, null_value=True):
        self.field_name = field_name
        self.existence = existence
        self.null_value = null_value


class GeoDistanceFilter(BaseNode):
    def __init__(self, field_name, center_lat, center_lng, distance_in_km=1):
        self.field_name = field_name
        self.center_lat = center_lat
        self.center_lng = center_lng
        self.distance_in_km = distance_in_km


class TopLevelAggregation(BaseNode):
    def __init__(self, field_name, agg):
        self.field_name = field_name
        self.agg = agg


class TermsAggregation(BaseNode):
    def __init__(self, field_name, size=0):
        self.field_name = field_name
        self.size = size


class SumAggregation(BaseNode):
    def __init__(self, field_name):
        self.field_name = field_name


class AvgAggregation(BaseNode):
    def __init__(self, field_name):
        self.field_name = field_name


class StatsAggregation(BaseNode):
    def __init__(self, field_name):
        self.field_name = field_name


class MinAggregation(BaseNode):
    def __init__(self, field_name):
        self.field_name = field_name


class MaxAggregation(BaseNode):
    def __init__(self, field_name):
        self.field_name = field_name


class ValueAccountAggregation(BaseNode):
    def __init__(self, field_name):
        self.field_name = field_name

