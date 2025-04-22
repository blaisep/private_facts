from decouple import config

port = config('PORT')

print(port)
