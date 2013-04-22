#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from unittestzero import Assert

from pages.base_page import MozTrapBasePage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions as Exceptions

from pages.elUtilities import Utilities

class MozTrapManageUserPage(MozTrapBasePage):

    _page_title = 'Manage User'
    
    #locators
    _LocatorManageTab = (By.CSS_SELECTOR, "li.manage-nav > a") 
    _LocatorUsersTab = (By.CSS_SELECTOR, "li.nav-users > a")
    _LocatorCreateUser = (By.CSS_SELECTOR, "#manageusers .create.single ")

    #constants
    _TimeOut = 10

    #add a new user into the user list
    def create_user(self, name=None, emailAddr=None, role=None):     
        
        #click the "Manage" tab       
        try:
            element = WebDriverWait(self.selenium,self._TimeOut). \
                      until(lambda s: self.find_element(*self._LocatorManageTab))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        element.click()
        
        #click the "Users" tab
        try:         
            element = WebDriverWait(self.selenium,self._TimeOut). \
                      until(lambda s: self.find_element(*self._LocatorUsersTab))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)     
        element.click()

        #create a new user
        #click "create a user" tab
        try:
            element = WebDriverWait(self.selenium,self._TimeOut). \
                      until(lambda s: self.find_element(*self._LocatorCreateUser))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        element.click()
            
        #fill out the info of a new user
        try:
            elmntName = self.find_element(By.CSS_SELECTOR, "#id_username.value")
            elmntEmail = self.find_element(By.CSS_SELECTOR, "#id_email.value")
            elmntRole = self.find_element(By.CSS_SELECTOR, "#id_groups.value") 
            elmntActions = self.find_element(By.CSS_SELECTOR, "div.form-actions > button")   
        except WebDriverException:
            Assert.fail(Exceptions.WebDriverException)
        elmntName.send_keys(name)
        elmntEmail.send_keys(emailAddr)
        try:
            Select(elmntRole).select_by_visible_text(role)
        except Exceptions.NoSuchElementException:
            Assert.fail(Exceptions.NoSuchElementException)
        elmntActions.submit()   #submit the info
        
        #check if the submission is complete without an error
        try:
            elmntErrList = self.find_element(By.CSS_SELECTOR, "ul.errorlist > li") 
            Assert.false(elmntErrList.is_displayed())   #either the name or the email is already in use      
        except Exceptions.NoSuchElementException:
            print "submission is complete"

        #acquire the list of users
        try:
            elmntUserList = self.find_elements(By.CSS_SELECTOR, "#manage-users-form .listitem")
        except Exceptions.WebDriverException:
            Assert.fail(Exceptions.WebDriverException)  #failed to obtain a list of users
        
        #review the contents of the submission
        isGivenUserFound = False
        for element in elmntUserList:
            userName = element.find_element(By.CSS_SELECTOR, "div.name").text
            userEmail = element.find_element(By.CSS_SELECTOR, "div.email").text
            userRoles = element.find_element(By.CSS_SELECTOR, "div.roles").text            
            if userName == name and userEmail == emailAddr and userRoles == role:
                isGivenUserFound = True
                break
        Assert.true(isGivenUserFound)   #the given user is not listed in

    #delete the user in the user list
    #def delete_user(self, name=None):
    #
        #click the "Manage" tab
    #    try:
    #        element = WebDriverWait(self.selenium, self._TimeOut). \
    #                  until(lambda s: self.find_element(*self._LocatorManageTab))
    #    except Exceptions.TimeoutExceptions:
            #Assert.fail

    #    
    #def find_user(self, name=None):
        
    #test
    def test(self):
        
        FilterTermName = "Test Run"
        
        #click the "Manage" tab       
        try:
            element = WebDriverWait(self.selenium,self._TimeOut). \
                      until(lambda s: self.find_element(*self._LocatorManageTab))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        element.click()
        
        #type in a filter term in the input field
        try:
            element = WebDriverWait(self.selenium, self._TimeOut) . \
                      until(lambda s: self.find_element(By.CSS_SELECTOR,"#text-filter"))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        element.send_keys(FilterTermName)
        
        try:
            elements = WebDriverWait(self.selenium, self._TimeOut) . \
                      until(lambda s: self.find_elements(By.CSS_SELECTOR,'a.suggestion.new'))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        for element in elements:
            TermName = element.find_element(By.CSS_SELECTOR, "b").text
            TermType = element.find_element(By.CSS_SELECTOR, "i").text
            if TermName == FilterTermName and TermType == "[description]":
                element.click()
                
    def test2(self,category=None,name=None):
             
        utils = Utilities(self.selenium,self._TimeOut)
             
        #click "Manage" tab
        tab = utils.find_element(By.CSS_SELECTOR, "li.manage-nav > a")
        tab.click()
        
        #click "Advanced Filtering" tab
        tab = utils.find_element(By.CSS_SELECTOR, "h4.toggle>a")
        tab.click()
        
        #get the filter form
        form = utils.find_element(By.CSS_SELECTOR, "#filterform")
        elements = form.find_elements(By.CSS_SELECTOR, "section.filter-group")
        category = category.lower()
        for element in elements:
            #access the name of a category
            name_element = element.find_element(By.CSS_SELECTOR, "h5.category-title")
            name_category = name_element.text
            #check the name if the category name matches
            name_category = name_category.lower()
            if name_category == category and len(name_category) == len(category):
                #find all the associated items
#               ul = element.find_element(By.CSS_SELECTOR, "ul.filter-items long")
#               items = ul.find_elements(By.CSS_SELECTOR, "li.filter-item")
                item_no = 1
                while 1:
                    try:
                        item = element.find_element(By.CSS_SELECTOR, "#id-filter-"+category+"-"+str(item_no))
                        content = item.find_element(By.CSS_SELECTOR, "onoffswitch")
                        content = content.text
                        if content == name and len(content) == len(name):
                            break
                        item_no = item_no + 1                      
                    except Exceptions.NoSuchElementException:
                        break
                if item != 0:
                    item.click()
                            
                    
                    
                
                for item in items:
                    content = item.find_element(By.CSS_SELECTOR, "onoff.content")
                    content = content.text
                    print content
             