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

    # utility methods
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

    def __str__(self):
        return f'{self.name} starts at {self.start} and ends at {self.end}'

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
        self.practices.append(practice)
        if practice.getDesignation() == 'afternoon':
            self.afternoon = True
        elif practice.getDesignation == 'morning':
            self.morning = True

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
    practice_starts = [datetime.time(7), datetime.time(8), datetime.time(2, 30), datetime.time(4), datetime.time(5, 30)]
    practice_ends = [datetime.time(8), datetime.time(9), datetime.time(4), datetime.time(5, 30), datetime.time(7)]
    practice_designations = ['morning', 'morning', 'afternoon', 'afternoon', 'afternoon']
    for n, s, e, d in zip(practice_names, practice_starts, practice_ends, practice_designations):
        practices.append(AthleticBlock(n, s, e, d))

    return practices

def get_datetimes(time_spread):
    time_spread = time_spread.replace(" ", "")        # delete all spaces
    print(time_spread)
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



def test_parser():
    swimmers = parse_swimmers()
    for s in swimmers:
        print(s)


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
    test_parser()