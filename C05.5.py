import redis

red = redis.Redis(
    host='localhost',
    port=6379,
    password=''
)
red.set('var1', 'value1')
print(red.get('var1'))