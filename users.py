import redis
r = redis.from_url('redis://:p6276f73643cd377844153100d0c88f2a3b5d6b23c8b20ae56c48c8cbe6638c3b@ec2-3-217-237-190.compute-1.amazonaws.com:16889')

db_keys = r.keys(pattern="*")
for single in db_keys:
    chat_id = r.get(single).decode("UTF-8")
    print(single.decode("UTF-8"), ": ", chat_id)