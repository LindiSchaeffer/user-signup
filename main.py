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
import cgi

form = """
<form method="post">
    <h1>Signup</h1>
    <table>
        <tr>
            <td>
                <label> Username </label>
            </td>
            <td>
                <input type="text" name="username" value="%(username)s">
                <span style="color:red">%(error1)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label> Password </label>
            </td>
            <td>
                <input type="password" name="password">
                <span style="color:red">%(error4)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label> Verify Password </label>
            </td>
            <td>
                <input type="password" name="verify_password">
                <span style="color:red">%(error2)s</span>
            </td>
        </tr>
            <td>
                <label> Email Address (optional) </label>
            </td>
            <td>
                <input type"text" name="email" value="%(email)s">
                <span style="color:red">%(error3)s</span>
        </tr>
    </table>
    <input type="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
    return USER_RE.match(user_name)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(user_password, user_verify_password):
    if user_password:
        if user_password == user_verify_password:
            return PASS_RE.match(user_password)
    else:
        return True

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(user_email):
    if user_email:
        return EMAIL_RE.match(user_email)
    else:
        return True

def valid_password_input(user_password):
    if user_password:
        return True

class MainHandler(webapp2.RequestHandler):

    def write_form(self, error1, error2, error3, error4, username, password, email):
        self.response.write(form % {"error1": error1,
                                    "error2": error2,
                                    "error3": error3,
                                    "error4": error4,
                                    "username": username,
                                    "password": password,
                                    "email": email})

    def get(self):
        self.write_form('', '', '', '', '', '', '')

    def post(self):
        user_name = self.request.get('username')
        user_password = self.request.get('password')
        user_verify_password = self.request.get('verify_password')
        user_email = self.request.get('email')

        username = valid_username(user_name)
        password = valid_password(user_password, user_verify_password)
        email = valid_email(user_email)
        password_input = valid_password_input(user_password)

        if not (username and password and email and password_input):

            error_1, error_2, error_3, error_4 = "That's not a valid username." if not username else '', \
                                        "Your passwords didn't match." if not password else '', \
                                        "That is not a valid email address." if not email else '', \
                                        "Please enter a valid password." if not password_input else '',

            self.write_form(error_1,
                            error_2,
                            error_3,
                            error_4,
                            user_name,
                            user_password,
                            user_email)

        else:
            self.redirect("/welcome?username=" + user_name)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("<h1>Welcome, %(username)s!</h1>" % {"username" : username})
        #self.response.write(username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
