from apscheduler.schedulers.blocking import BlockingScheduler
from mrdk import AutoDk
from priv import conf, loc

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    print('[+] Start scheduler on every 6:00 AM.')
    ad = AutoDk(config=conf, location=loc)
    ad.run()
    scheduler.add_job(ad.run, 'cron', hour=6)
    scheduler.start()
