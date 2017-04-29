from django.test import TestCase

# Create your tests here.

from django.utils.deprecation import MiddlewareMixin


class M1(MiddlewareMixin):

    def process_request(self, request):
        print("m1")

    def process_response(self, request, response):
        print("m1, response")
        return response


class M2(MiddlewareMixin):

    def process_request(self, request):
        print("m2")


    def process_response(self, request, response):
        print("m2, response")
        return response