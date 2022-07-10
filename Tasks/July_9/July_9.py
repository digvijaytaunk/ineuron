# class
# object
# constructor
# inheritance
# private
# public
# protected
# abstraction
# encapsulations
# polymorphism
# method overriding
#
# For all the concepts that we have discussed in our class point by point you have to write
# at least 10 examples
#
# you have to make sure that use ineuron studnets , class , class type , number of courses
# , affiliates , blog, internship , jobs as a reference example

import logging
from datetime import time



class InvalidEmailException(Exception):
    """
    Class to handle invalid email ids
    """
    pass


class Person:
    """
    Base class for all people associated with iNeuron.
    """
    _name = ''  # protected variable
    _email_id = ''
    _contact_number = 0
    __age = 0

    def __init__(self, name, contact_number, email_id, age):
        self._name = name
        self._contact_number = contact_number
        try:
            self.__age = int(age)
            if '.com' not in email_id or '@' not in email_id:
                raise InvalidEmailException
            self._email_id = email_id
        except ValueError:
            logging.error("Value of age must be integer")
        except InvalidEmailException:
            logging.error('Invalid email found')
        except Exception as e:
            logging.error(e)

    def get_contact_details(self):
        """
        Returns Name, Contact Number and email id of any Person
        """
        return self._name, self._contact_number, self._email_id

    def update_email(self, new_email):  # Encapsulation - wrapping data and methods that work on data within one unit
        """
        Method to update existing email ID
        """
        try:
            if '.com' not in new_email or '@' not in new_email:
                raise InvalidEmailException

            self._email_id = new_email

        except InvalidEmailException:
            logging.error('Invalid email found')

    def relation_with_ineuron(self):   # polymorphism example - method overridden in subclass
        raise NotImplementedError

    def looking_for_job_change(self):
        raise NotImplementedError


class Student(Person):  # inheritance Example
    """
    Person who enrolled for any type of course or internship.
    Non-iNeuron employee
    """
    __enrolled_courses_and_progress = dict()  # Abstraction - user of this class need not know about this variable.
    completed_courses = []

    def __init__(self, name, contact_number, email_id, age, experienced):
        super().__init__(name, contact_number, email_id, age)
        self.__experienced = experienced

    __relation_with_ineuron = "Student"  # private variable

    def enroll_new_course(self, course_name):
        """
        List of courses this student has enrolled in
        """
        if course_name in self.__enrolled_courses_and_progress:
            logging.warning("Already enrolled for {} course".format(course_name))
        else:
            self.__enrolled_courses_and_progress.setdefault(course_name, 0)
            logging.info("{} course successfully added to enrollment list".format(course_name))

    def remove_course_enrollment(self, course_name):
        """
        Removes the given course from enrollment list if exists
        """
        if course_name in self.__enrolled_courses_and_progress:
            del self.__enrolled_courses_and_progress[course_name]
            logging.info("{} course removed from enrollment list".format(course_name))

    def update_course_progress(self, course, progress_percent):
        """
        Updates the progress of course in percentage
        """
        try:
            if course in self.__enrolled_courses_and_progress.keys():
                self.__enrolled_courses_and_progress[course] = float(progress_percent)
                logging.info("{} Progress for course {} is updated".format(progress_percent, course))
        except ValueError:
            logging.error("Percentage value must be numeric")
        except Exception as e:
            logging.error(e)

    def relation_with_ineuron(self):  # polymorphism example - overriding method on base class
        """
        Relationship with ineuron as a company
        """
        return self.__relation_with_ineuron

    def looking_for_job_change(self):
        """
        Returns whether searching for new job
        """
        return True

    def show_courses_enrolled(self):
        logging.info("show_courses_enrolled")
        return self.__enrolled_courses_and_progress.keys()

    def __isPlaceable(self):
        """
        Calculates based on number of course enrolled and corresponding progress less than criteria.
        """
        criteria = 50  # 50% progress required in each enrolled course

        for progress in self.__enrolled_courses_and_progress.values():
            if progress < criteria:
                return False

        return True

    def allowed_for_interview(self):
        """
        Determines based on the completeness of course progress and fulfill the minimum criteria.
        """
        logging.info("allowed_for_interview {}".format(self.__isPlaceable()))
        return self.__isPlaceable()  # Abstraction - logic hidden behind self.__isPlaceable()

    def show_all_courses_progress(self):
        return self.__enrolled_courses_and_progress


class SupportPerson(Person):
    """
    Class to handle details regarding the support person working in iNeuron
    """
    __relation = 'Support'
    __available_start_time = time(10, 00, 00)   # private variable
    __available_end_time = time(20, 00, 00)
    __available_for_chat = False

    def relation_with_ineuron(self):
        """
        Relationship with ineuron as a company
        """
        return self.__relation

    def looking_for_job_change(self):   # polymorphism example
        """
        Returns whether searching for new job
        """
        return False

    def available_between(self):
        """
        Returns the tie this support person is available for support
        """
        return 'Available between {} to {}'.format(self.__available_start_time, self.__available_end_time)

    def isAvailable_for_chat_support(self):
        """
        Checks curent availability
        """
        return self.__available_for_chat

    def mark_as_available(self, flag):
        """
        Sets the availability
        """
        if flag is bool:
            self.__available_for_chat = flag


class Instructor(Person):  # inheritance Example
    """
    iNeuron employee teaching or non-teaching staff.
    """

    __relation_with_ineuron = "Instructor"   # private variable
    __can_teach_courses = []

    def relation_with_ineuron(self):  # polymorphism example
        """
        Relationship with ineuron as a company
        """
        return self.__relation_with_ineuron

    def looking_for_job_change(self):  # polymorphism example
        """
        Returns whether searching for new job
        """
        return False

    def can_teach_courses(self):
        """
        List ot courses that an instructor can teach
        """
        return self.__can_teach_courses

    def add_new_course_to_teach(self, course):
        """
        Adds a new course to instructor's competency so that he/she can teach
        """
        if course not in self.__can_teach_courses:
            self.__can_teach_courses.append(course)
            logging.info('{} course added to {} can teach list'.format(course, self._name))
        else:
            logging.warning('{} already can teach {}'.format(self._name, course))


if __name__ == '__main__':

    logging.basicConfig(filename="task_9_july_logs.log", level=logging.DEBUG,
                        format='[%(levelname)s] : %(asctime)s : %(name)s : %(message)s')

    logging.info("THIS IS THE BEGINING OF THE APP")
    s = Student("Digvijay", 89798546, 'd@d.com', '25', True)
    s1 = Student("Sid", 89798546, 'dd.com', '25', True)
    s2 = Student("Sid", 89798546, 'd@d.com', '25a', True)
    s.relation_with_ineuron()
    print(s.get_contact_details())
    s.enroll_new_course("ML")
    s.enroll_new_course("FSDS")
    s.enroll_new_course("FSDS")
    s.enroll_new_course("C++")
    s.remove_course_enrollment("C++")
    s.update_email('dt@gmail.com')
    print(s.get_contact_details())
    s.update_course_progress("ML", 10)
    s.update_course_progress("FSDS", 70)
    s.update_course_progress("Javascript", 40)
    print(s.show_all_courses_progress())
    s.enroll_new_course("Javascript")
    s.update_course_progress("Javascript", '40a')
    print(s.relation_with_ineuron())
    print(s.allowed_for_interview())
    print(s.show_all_courses_progress())

    i = Instructor('Hitesh', 2354353, 'hitesh@lco.com', 25)
    print(i.relation_with_ineuron())
    i.add_new_course_to_teach('javascript')
    i.add_new_course_to_teach('javascript')
    i.add_new_course_to_teach('Python')
    print(i.can_teach_courses())
    print(i.get_contact_details())
    print(i.can_teach_courses())
    print(i.get_contact_details())

    s = SupportPerson("Sunny", 54654635, 'sunny@ineuron.com', 25)
    print(s.available_between())
