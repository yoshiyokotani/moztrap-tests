#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.manage_user_page import MozTrapManageUserPage

class TestManageUsers():
    
    @pytest.mark.moztrap(5000)
    @pytest.mark.destructive
    def test_that_new_user_can_be_added(self,mozwebqa):
        from pages.login_page import MozTrapLoginPage
        login_pg = MozTrapLoginPage(mozwebqa)
        login_pg.go_to_login_page()
        login_pg.login()
                
        user_pg = MozTrapManageUserPage(mozwebqa)
        user_pg.create_user('user2','newuser2@test.com','Tester')
        user_pg.delete_user('user2')
        user_pg.create_user('user2','newuser2@test.com','Tester')
        user_pg.activate_user('user2','newuser2@test.com','Tester')
        user_pg.deactivate_user('user2','newuser2@test.com','Tester')
        
        
        
        
