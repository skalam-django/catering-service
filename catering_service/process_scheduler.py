import threading
import time, datetime
import schedule
from django.conf import settings
import traceback


class SchedulerThread(object):
	def __init__(self, *args, **kwargs):
		self.cease 		= 	threading.Event()
		self.scheduler 	= 	schedule.Scheduler()
		self.daemon  	= 	kwargs.get('daemon', True)

	def run(self, *args, **kwargs):
		job = args[0]
		interval = kwargs.get('interval', 1)
		interval = interval if interval>1 else 1
		until = kwargs.get('until')
		self.start_delay = kwargs.get('start_delay')
		if until is not None:
			self.job = self.scheduler.every(interval).seconds.until(datetime.timedelta(seconds=until)).do(job)
		else:
			self.job = self.scheduler.every(interval).seconds.do(job)	

		class ScheduleThread(threading.Thread):
			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)
				self.daemon = kwargs.get('daemon', True)

			@classmethod
			def run(cls):
				if self.start_delay is not None:
					try:
						time.sleep(int(self.start_delay))
					except:
						pass	
				try:									
					while not self.cease.is_set():
						self.scheduler.run_pending()
						try:
							time.sleep(interval/2)	
						except:
							time.sleep(1)
				except Exception as e:
					print(f"ScheduleThread.run Error: {e}", traceback.format_exc())			
		try:
			continuous_thread = ScheduleThread(daemon=self.daemon)
			continuous_thread.start()
		except Exception as e:
			print(f"ScheduleThread.run Error: {e}", traceback.format_exc())			


	def stop(self, *args, **kwargs):
		self.scheduler.cancel_job(self.job)
		self.cease.set()
		
