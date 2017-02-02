#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form = """
<form method="post">
    <h1>Signup</h1>
    <label>
        Username
        <input type="text" name="username">
    </label>
    <br>
    <label>
        Password
        <input type"password" name="password">
    </label>
    <br>
    <label>
        Verify Password
        <input type"password" name="verify_password">
    </label>
    <br>
    <label>
        Email Address (optional)
        <input type"text" name="email">
    </label>
    <br>
    <input type="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
    return USER_RE.match(user_name)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(user_password, user_verify_password):
    if user_password == user_verify_password:
        return PASS_RE.match(user_password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(user_email):
    return PASS_RE.match(user_email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)

    def post(self):
        user_name = self.request.get('username')
        user_password = self.request.get('password')
        user_verify_password = self.request.get('verify_password')
        user_email = self.request.get('email')

        username = valid_username(user_name)
        password = valid_password(user_password, user_verify_password)
        email = valid_email(user_email)

        if (username and password and user_email):
            self.response.write("It's Working!")

        else:
            self.response.write("Incorrect")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
