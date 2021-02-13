# Created by Caleb Bitting
# 02/12/2021

import datetime
import argparse

class TimeBlock:

	def __init__(self, name, start, end):
		'''init method
		
		Args:
			name (string): name
			start (datetime.time): the starting time as a datetime.time object
			end (datetime.time): the ending time as a datetime.time object
		'''
		self.name = name
		self.start = start
		self.end = end

	# accessor methods
	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def getName(self):
		return self.name

	def duration(self):
		'''gets the duration (as a timedelta) of the event
		
		Returns:
		    timedelta: the  duration
		'''
		# get datetime.time objects
		end = self.end
		start = self.start
		return TimeBlock.create_timedelta(start, end)

	def contains(self, time):
		'''check to see if passed time within start and end bounds
		
		Args:
			time (datetime.time): the target time
		
		Returns:
			bool: whether or not passed time is in this TimeBlock
		'''
		if time >= self.getStart() and time <= self.getEnd():
			return True
		else: 
			return False

	@staticmethod
	def create_timedelta(start, end):
		'''takes two time objects and returns a timedelta
		
		Args:
		    start (datetime.time): the start time
		    end (datetime.time): the end time
		
		Returns:
		    datetime.timedelta: the timedelta between the two
		'''
		return datetime.timedelta(
			hours=end.hour - start.hour,
			minutes=end.minute - start.minute)

	def __str__(self):
		return f'{self.name} starts at {self.start} and ends at {self.end}'

	def __floordiv__(self, other):
		'''compares a AcademicBlock with an AthleticBlock
		
		Args:
			other (TimeBlock): the other TimeBlock to compare to
		
		Returns:
			int: -1 if dogshit, 0 if horrible, 1 if manageable, 2 if ideal
		
		Raises:
			Exception: if the TimeBlock child class of both comparators are the same, this function raises an exception
		'''
		# make sure ALL comparisons are between and Academic and Atheltic block
		if isinstance(self, type(other)):
			raise Exception('Operation // not to be used on the same types of objects')

		# check start and end connections
		if other.end == self.start:
			return 0 if isinstance(self, AcademicBlock) else 1      # 0 when practice -> class && 1 when class -> practice
		if self.end == other.start:
			return 0 if isinstance(self, AthleticBlock) else 1      # 0 when practice -> class && 1 when class -> practice

		# check for overlap
		if self.duration() < other.duration():
			if other.contains(self.start) or other.contains(self.end):       # check if the longer block contains the start and end points of the shorter block
				return -1
		else:
			if self.contains(other.start) or self.contains(other.end):
				return -1
		# edge case of identical timeframes
		if self.start == other.start and self.end == other.end:
			return -1
		# remaining pairs are separated. is it enough?
		# find first block
		first_block = self if self.start < other.start else other
		# determine gap duration
		if first_block == self:
			gap = TimeBlock.create_timedelta(self.end, other.start)
		else:
			gap = TimeBlock.create_timedelta(other.end, self.start)
		gap_seconds = gap.total_seconds()
		# check for appropriate duration
		if isinstance(first_block, AcademicBlock):
			return 2 if gap_seconds >= 1200 else 1
		else:
			return 2 if gap_seconds >= 3600 else 0

class AcademicBlock(TimeBlock):

	def __init__(self, name, start, end):
		super().__init__(name, start, end)

class AthleticBlock(TimeBlock):

	def __init__(self, name, start,  end, designation):
		super().__init__(name, start,end)
		self.swimmers = []
		self.designation = designation

	# accessor methods
	def getDesignation(self):
		return self.designation

	# utility methods
	def add(self, swimmer):
		'''add a swimmer to this practice. also recordss in the Swimmer object that they will attend this practice
		
		Args:
			swimmer (Swimmer): Swimmer object to add
		'''
		self.swimmers.append(swimmer)
		swimmer.add(self)

class Swimmer:

	def __init__(self, name, classes):
		'''initialization method
		
		Args:
			name (string): name of swimmer
			classes (list): a list of datetime
		'''
		self.name = name
		self.classes = sorted(classes, key=lambda c: c.start)       # sorts by class start time
		self.practices = []
		self.practice_rankings  = {}
		self.afternoon = False
		self.morning = False

	# accessor methods
	def getName(self):
		return self.name

	def getClasses(self):
		return self.classes

	def getFirstStart(self):
		return self.classes[0].getStart()

	def getLastEnd(self):
		return self.classes[-1].getEnd()

	def hasAfternoon(self):
		return self.afternoon

	def hasMorning(self):
		return self.morning

	def hasAllPractices(self):
		if self.afternoon and self.morning:
			return True
		else:
			return False

	# utility methods
	def add(self, practice):
		'''adds a practice to the internal list
		
		Args:
		    practice (AthleticBlock): the practice to add
		'''
		self.practices.append(practice)
		if practice.getDesignation() == 'afternoon':
			self.afternoon = True
		elif practice.getDesignation == 'morning':
			self.morning = True

	def rankPractices(self, practice_list):
		'''ranks the practices (ideal -> 2, manageable -> 1, horrible -> 0, dogshit -> -1)
		
		Args:
		    practice_list (TYPE): DESCRIPTION
		'''
		for prac in practice_list:
			pairings = [c//prac for c in self.classes]
			self.practice_rankings[prac] = min(pairings)

	def  __str__(self):
		return f'{self.name} has {self.classes}'

def parse_args():
	'''This function parses the command line arguments
	
	Returns:
		argparse.namespace: an argparse namespace representing the command line arguments
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('csv_name', type=str, help='the name of the csv from which this program will read swimmers.')
	parser.add_argument('--testing', '-t', action='store_true', help='enter testing mode. All functions will be passed testing=True where possible.')
	args = parser.parse_args()

	return args

def create_practices():
	'''does exactly what it says on the tin
	
	Returns:
		list: a list of all AthleticBlock options
	'''
	practices = []
	practice_names = ['early lift', 'late lift', 'early swim', 'mid swim', 'late swim']
	practice_starts = [datetime.time(7), datetime.time(8), datetime.time(14, 30), datetime.time(16), datetime.time(17, 30)]
	practice_ends = [datetime.time(8), datetime.time(9), datetime.time(16), datetime.time(17, 30), datetime.time(19)]
	practice_designations = ['morning', 'morning', 'afternoon', 'afternoon', 'afternoon']
	for n, s, e, d in zip(practice_names, practice_starts, practice_ends, practice_designations):
		practices.append(AthleticBlock(n, s, e, d))

	return practices

def get_datetimes(time_spread):
	'''given a date in the form HH:MM - HH:MM returns tuple of datetime.time objects representing start and end times
	
	Args:
	    time_spread (string): input date
	
	Returns:
	    tuple of datetime.time objects: (start, end)
	'''
	time_spread = time_spread.replace(" ", "")        # delete all spaces
	start_end = time_spread.split('-')
	datetimes = []
	for item in start_end:
		hours_minutes = item.split(':')
		if len(hours_minutes) == 1:
			hours_minutes.append(0)
		foo = datetime.time(int(hours_minutes[0]), int(hours_minutes[1]))
		datetimes.append(foo)

	return tuple(datetimes)

def parse_swimmers(cmd_args):
	'''parses the passed CSV file
	
	Args:
	    cmd_args (argparse.namespace): the command-line arguments
	
	Returns:
	    list: list of Swimmer objects with AcademicBlocks
	'''
	# read csv
	with open(cmd_args.csv_name, 'r') as fp:
		csv_contents = fp.read()
	split_contents = csv_contents.split('\n')
	swimmers = []
	# for each swimmer
	for line in split_contents:
		if not line:            # filter out any empty lines
			continue
		# get each cell value
		line_items = line.split(',')
		name = line_items[0]                # first cell is the names
		# construct a list of classes they're taking
		swimmer_classes = []
		for item in line_items[1:]:
			start, end = get_datetimes(item)
			swimmer_classes.append(AcademicBlock('class', start, end))
		# create a swimmer object
		swimmers.append(Swimmer(name, swimmer_classes))

	return swimmers



######################################################################################################################################################
##############################										TEST CODE 											##############################
######################################################################################################################################################



def divmod_test():
	cmd_args = parse_args()
	practices = create_practices()
	swimmers = parse_swimmers(cmd_args)
	for index, s in enumerate(swimmers):
		s.rankPractices(practices)
		if index == 2 or index == 3:
			print(s.name)
			for key in s.practice_rankings:
				print(key, s.practice_rankings[key])
			print()
	''' EXPECTED OUTPUT:
	POS
	early lift starts at 07:00:00 and ends at 08:00:00 -1
	late lift starts at 08:00:00 and ends at 09:00:00 1
	early swim starts at 14:30:00 and ends at 16:00:00 -1
	mid swim starts at 16:00:00 and ends at 17:30:00 -1
	late swim starts at 17:30:00 and ends at 19:00:00 2

	POS2
	early lift starts at 07:00:00 and ends at 08:00:00 1
	late lift starts at 08:00:00 and ends at 09:00:00 0
	early swim starts at 14:30:00 and ends at 16:00:00 2
	mid swim starts at 16:00:00 and ends at 17:30:00 -1
	late swim starts at 17:30:00 and ends at 19:00:00 0
	'''

def object_tests():
	# initialize objects
	# AcademicBlocks
	class_one = AcademicBlock('GO281', datetime.time(9), datetime.time(9, 50))
	class_two = AcademicBlock('MA253', datetime.time(10), datetime.time(10, 50))
	class_three = AcademicBlock('CS333',  datetime.time(11), datetime.time(11, 50))
	class_four = AcademicBlock('HI342', datetime.time(19), datetime.time(21, 30))
	# Swimmer
	caleb = Swimmer('Bitting', [class_two, class_one, class_three, class_four])
	# AthleticBlocks
	early = AthleticBlock('early_swim', datetime.time(14, 30), datetime.time(16), 'afternoon')
	lift_one = AthleticBlock('early_lift', datetime.time(6), datetime.time(7), 'morning')
	# make sure correct construction
	print(class_one)
	print(caleb)
	print(early)

	# check for functionality
	print(caleb.classes[0] == class_one)
	print(f'{class_one.contains(datetime.time(9, 12))} should be True')
	print(f'{class_one.contains(datetime.time(10))} should be False')
	early.add(caleb)
	print(f'{caleb in early.swimmers} should be true')
	print(f'{early in caleb.practices} should be true')
	print(f'{caleb.hasAfternoon()} should be true')
	print(f'{caleb.hasMorning()} {caleb.hasAllPractices()} should both be false')

if __name__ == '__main__':
	divmod_test()