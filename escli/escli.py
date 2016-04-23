#!/usr/bin/env python

import argparse
import json
import os

import elasticsearch
import prettytable


def parse_args():
    description = "Query log message data in elasticsearch"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--doc-type', default='logs',
                        help='Elasticsearch document type name. Default: '
                        '%(default)s.')
    parser.add_argument('-f', '--format', default='logs',
                        choices=['logs', 'json'],
                        help='Output format. Default: %(default)s. '
                        'Choices: %(choices)s.')
    parser.add_argument('-i', '--index', default='logstash',
                        help='Elasticsearch index name. Default: %(default)s.')
    parser.add_argument('-l', '--log-format',
                        default='@timestamp,severity,module,message',
                        help='Format for log output. Default: %(default)s.')
    parser.add_argument('--log-table', action='store_true',
                        help='Output logs in a pretty table. Default: '
                        '%(default)s.')
    parser.add_argument('-q', '--query',
                        help='Query string query. Uses Apache Lucene query '
                        'syntax.')
    parser.add_argument('--sort', default='_score',
                        help='Sort by this criteria. Comma separated list of '
                        'field:order pairs. Default: %(default)s.')
    parser.add_argument('-u', '--url', default=os.getenv('ELASTICSEARCH_URL'),
                        help='Elasticsearch URL. Default: %(default)s.')
    return parser.parse_args()


def build_body(args):
    body = {
        'query': {
            'query_string': {
                'query': args.query
            }
        }
    }
    return body


def search(es, args):
    body = build_body(args)
    results = es.search(index=args.index,
                        doc_type=args.doc_type,
                        body=body,
                        sort=args.sort)
    return results


def print_logs_ugly(fields, hits):
    for hit in hits:
        source = hit["_source"]
        log_fields = [source.get(field, '') for field in fields]
        print " ".join(log_fields)


def print_logs_pretty(fields, hits):
    t = prettytable.PrettyTable(fields)
    for hit in hits:
        source = hit["_source"]
        log_fields = [source.get(field, '') for field in fields]
        t.add_row(log_fields)
    print t


def print_logs(results, log_format, log_table):
    hits = results["hits"]
    if not hits["total"]:
        print "Got no hits"
        return

    print "Got %(total)s hits, max score %(max_score)s." % hits
    fields = log_format.split(',')
    fields = [field.strip() for field in fields]
    if log_table:
        print_logs_pretty(fields, hits["hits"])
    else:
        print_logs_ugly(fields, hits["hits"])


def print_json(results):
    print json.dumps(results, sort_keys=True, indent=4)


def print_results(results, args):
    if args.format == 'logs':
        print_logs(results, args.log_format, args.log_table)
    elif args.format == 'json':
        print_json(results)
    else:
        raise Exception("Unexpected format %s" % args.format)


def main():
    args = parse_args()
    es = elasticsearch.Elasticsearch([args.url])
    results = search(es, args)
    print_results(results, args)


if __name__ == '__main__':
    main()
