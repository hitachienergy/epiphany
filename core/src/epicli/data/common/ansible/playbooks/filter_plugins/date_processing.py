#!/usr/bin/python

from datetime import datetime


class FilterModule(object):
    def filters(self):
        return {
            'openssl_date2days': self.openssl_date2days
        }

    def openssl_date2days(self, openssl_date):
        """
        This function is used to find difference between openssl's
        '-enddate' or '-startdate' output and today
        :param openssl_date: '-enddate' or '-startdate' output of openssl, example: notAfter=Apr 20 07:06:21 2022 GMT
        :return: result in days
        """
        date1 = datetime.strptime(openssl_date.split('=')[1], '%b %d %H:%M:%S %Y %Z').date()
        date2 = datetime.now().date()
        return (date1 - date2).days
