#!/usr/bin/env python

import argparse
import json
import os

import elasticsearch


def parse_args():
    description = "Query log message data in elasticsearch"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--doc-type', default='post')
    parser.add_argument('--index', default='blog')
    return parser.parse_args()


def main():
    args = parse_args()
    url = os.getenv('ELASTICSEARCH_URL')
    es = elasticsearch.Elasticsearch([url])
    body = {
        'query': {
            'match_all': {}
        }
    }
    res = es.search(index=args.index,
                    doc_type=args.doc_type,
                    body=body)
    print json.dumps(res, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
