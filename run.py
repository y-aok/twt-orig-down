#!/usr/bin/env python

import sys
import yaml
import os
from twimg.get_tw_json import GetTwJson
from twimg.get_tw_img import GetImg
from twimg import simple_down


def main():
    try:
        with open('apikey.yml', 'r') as yml:
            _auth = yaml.load(yml)
            auth = [_auth['consumer_key'],
                    _auth['consumer_secret'],
                    _auth['access_token'],
                    _auth['access_token_secret']]
    except IOError:
        print('apikey.yml not found')
        sys.exit()

    try:
        query = sys.argv[1]
    except IndexError:
        query = input("input search query >")

    get_json = GetTwJson(query, auth)
    try:
        get_json.from_query()
    except Exception as e:
        print("failed during getting tweet jsons : {}".format(e))
        sys.exit()

    get_img = GetImg()
    succeed_tweets = []
    failed_tweets = []

    for q in get_json.json_for.keys():
        print("---- QUERY '{}'".format(q))
        for jsn in get_json.json_for[q]:
            links = []
            try:
                print("[ tweet id {}, by '{}' ]".format(jsn['id'], jsn['user']['name']))
                try:
                    links += get_img.from_json(jsn)
                except:
                    print("\t failed...")
                if links:
                    failed = 0
                    for link in links:
                        print("\t {}".format(link), end=' - ')
                        filename = link.split('/')[-1].split(':orig')[0]
                        target = os.path.join('./down', filename)
                        try:
                            simple_down.down(link, target)
                            print("success!")
                        except:
                            print("failed.")
                            failed = 1
                    if not failed:
                        succeed_tweets.append(jsn)
                    else:
                        failed_tweets.append(jsn)
                else:
                    print("\t no media found for this tweet.")
                    failed_tweets.append(jsn)
            except Exception as e:
                print("failed session : {}".format(e))

    print('----------------------')
    print('all sessions finished.')
    print('----------------------')
    print('[ Result summary ]')

    tweets_checked = len(succeed_tweets) + len(failed_tweets)
    print('number of tweets checked : {}'.format(tweets_checked))
    print('success : {}/{}'.format(len(succeed_tweets), tweets_checked))
    print('failed  : {}/{}'.format(len(failed_tweets), tweets_checked))
    if failed_tweets:
        print("failed for following tweets:")
        for jsn in failed_tweets:
            try:
                print(jsn['entities']['urls']['expanded_url'])
            except:
                print("id {}".format(jsn['id']))


if __name__ == "__main__":
    main()
