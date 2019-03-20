#encoding:utf-8
try:
    while True:
        print("try")
except KeyboardInterrupt:
    print("Interrupted!")
finally:
    print("finally.")