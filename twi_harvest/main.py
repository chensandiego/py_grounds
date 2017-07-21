from twython import Twython
import time
import math
import json
import pymongo





rate_limit_window=15*60

def twitter_oauth_login():
    API_key=' '
    API_Secret=' '

    ACCESS_Token=' '
    ACCESS_Token_secret=' '

    twitter = Twython(API_key,API_Secret,ACCESS_Token,ACCESS_Token_secret)

    return (twitter)

def pull_users_profiles(ids):
    users=[]
    for i in range(0,len(ids),100):
        batch = ids[i:1 +100]
        users += twitter.lookup_user(user_id=batch)
        print(twitter.get_lastfunction_header('x-rate-limit-remaining'))
        return (users)


def pull_users_profiles_limit_aware(ids):
    users=[]
    start_time=time.time()

    #must look up usrs in
    for i in range(0,len(ids),10):
        batch=ids[i:i+10]
        users +=twitter.lookup_user(user_id=batch)
        calls_left= float(twitter.get_lastfunction_header('x-rate-limit-remaining'))
        time_remaining_in_window = rate_limit_window - (time.time()-start_time)

        sleep_duration = math.ceil(time_remaining_in_window/calls_left)
        print('sleeping for' + str(sleep_duration) + ' seconds;' + str(calls_left)+ ' API calls remaining')
        time.sleep(sleep_duration)
        return (users)



def save_json(filename,data):
    with open(filename,"w", encoding="utf8") as outfile:
        json.dump(data,outfile)

def load_json(filename):
    with open(filename) as infile:
        data = json.load(infile)
        return data



#configure mongodb connections

def save_json_data_to_mongo(data,mongo_db,mongo_db_collection,host_string="localhost",port=27017):
    mongo_client=pymongo.MongoClient(host_string,port)
    mongo_db=mongo_client[mongo_db]
    collection=mongo_db[mongo_db_collection]
    inserted_object_ids = collection.insert(data)
    return(inserted_object_ids)



twitter=twitter_oauth_login()
friends_ids=twitter.get_friends_ids(count=5000)
friends_ids=friends_ids['ids']



followers_ids=twitter.get_followers_ids(count=5000)
followers_ids=followers_ids['ids']

print(len(friends_ids),len(followers_ids))


friends_profiles = pull_users_profiles(friends_ids)
followers_profiles = pull_users_profiles(followers_ids)


#use list comprehension
friends_screen_names=[p['screen_name'] for p in friends_profiles]

print (friends_screen_names)


fname='test_friends_profile.json'
save_json(fname,friends_profiles)



test_reload=load_json(fname)
#print(test_reload[0])

#store data to mongodb
save_json_data_to_mongo(friends_profiles,mongo_db='test',mongo_db_collection='user_profiles')
save_json_data_to_mongo(followers_profiles,mongo_db='test',mongo_db_collection='user_profiles')

geo_enabled=[p['geo_enabled'] for p in friends_profiles]
print(geo_enabled.count(1))

#print how many unique locations
location=[p['location'] for p in friends_profiles]
print(set(location))

#print time zone
time_zone=[p['time_zone'] for p in friends_profiles]
print(set(time_zone))



#print user latest status
status_geo=[p['status']['geo'] for p in friends_profiles if ('status' in p and p['status']['geo'] is not None)]
if status_geo: print(status_geo[0])
print(len(status_geo))
