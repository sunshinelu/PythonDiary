import time
import os
import seleniumSpider

def print_ts(message):
    print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))


def run(interval, start_date, end_date, parentID, childID,Type):
    print_ts("-"*100)
    print_ts("Starting every %s seconds." % interval)
    print_ts("-"*100)
    errorFile = open("error.log", "w")
    errorFile.truncate()
    errorFile.close()
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval-time.time() % interval
            size = os.path.getsize('error.log')
            if size == 0:
                print_ts("Starting command.")
                # execute the command
                seleniumSpider.main(start_date, end_date, parentID, childID,Type)
                print_ts("-" * 100)
                print_ts("Command status = %s." % "打开浏览器")
            else:
                input = open('error.log', 'r')
                for line in input:
                    line = line.split()
                    if 'exceptions' in line or 'Error' in line:
                        print_ts("Starting command.")
                        # execute the command
                        seleniumSpider.main(start_date, end_date, parentID, childID, Type)
                        print_ts("-" * 100)
                        print_ts("Command status = %s." % "打开浏览器")
                        break
        except Exception as e:
            print(e)
        print_ts("Sleeping until %s (%s seconds)..." % ((time.ctime(time.time() + time_remaining)), time_remaining))
        time.sleep(time_remaining)


if __name__=="__main__":
    interval = 60
    run(interval, '2018-03-01', '2018-04-02', 'Achild', 'A004child', 'A')