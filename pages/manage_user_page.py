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
    
    #common locators
    _locManageTab = (By.XPATH, "//ul//li/child::a[text()='Manage']")    
    _locUsersTab = (By.XPATH, "//div/ul//child::a[text()='Users']") 
    _locUserList = (By.XPATH, "//child::article[attribute::class='listitem']")

    #constants
    _TimeOut = 30

    #add a new user into the user list
    def create_user(self, name=None, emailAddr=None, role=None):     
        
        #local locators          
        _locCreateUser = (By.XPATH, "//child::section/a[text()='create a user']")        
        _locNewUserName = (By.XPATH, "//child::input[attribute::id='id_username']")
        _locNewUserEmail = (By.XPATH, "//child::input[attribute::id='id_email']")
        _locNewUserRole = (By.XPATH, "//child::select[attribute::id='id_groups']")
        _locAddUser = (By.XPATH, "//div[attribute::class='form-actions']/child::button")
        _locErrList = (By.XPATH, "//child::ul[attribute::class='errorlist']")        
        
        _locUserName = (By.CSS_SELECTOR, "h3.title")
        _locUserEmail = (By.CSS_SELECTOR, "div.email")
        _locUserRole = (By.CSS_SELECTOR, "ul.roles")         
        
        #[H] click the "Manage" tab       
        try:
            element = WebDriverWait(self.selenium,self._TimeOut). \
                                    until(lambda s: self.find_element(*self._locManageTab))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        element.click()
        
        #[H] click the "Users" tab
        try:         
            element = WebDriverWait(self.selenium,self._TimeOut). \
                                    until(lambda s: self.find_element(*self._locUsersTab))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)     
        element.click()

        #create a new user
        #[H] click "create a user" tab
        try:
            element = WebDriverWait(self.selenium,self._TimeOut). \
                                    until(lambda s: self.find_element(*_locCreateUser))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        element.click()
            
        #[H] fill out the info of a new user
        try:
            elmntName = WebDriverWait(self.selenium,self._TimeOut). \
                                      until(lambda s: self.find_element(*_locNewUserName))
            elmntEmail = WebDriverWait(self.selenium,self._TimeOut). \
                                       until(lambda s: self.find_element(*_locNewUserEmail))
            elmntRole = WebDriverWait(self.selenium,self._TimeOut). \
                                      until(lambda s: self.find_element(*_locNewUserRole))                                            
            elmntActions = WebDriverWait(self.selenium,self._TimeOut). \
                                         until(lambda s: self.find_element(*_locAddUser))             
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        elmntName.send_keys(name)
        elmntEmail.send_keys(emailAddr)
        try:
            Select(elmntRole).select_by_visible_text(role)
        except Exceptions.NoSuchElementException:
            Assert.fail(Exceptions.NoSuchElementException)
        elmntActions.click()   #submit the info
        
        #[M] check if the submission is complete without an error
        isErrListDisplayed = False
        try:
            elmntErrList = WebDriverWait(self.selenium,self._TimeOut). \
                                         until(lambda s: self.find_element(*_locErrList))
            isErrListDisplayed = elmntErrList.is_displayed()
        except Exceptions.TimeoutException:
            print "submission is complete without an error"
        if isErrListDisplayed == True:      
            print "the given set of the new user setting is already in use.\n"
            return False

        #[M] acquire the list of users
        try:
            elmntUserList = WebDriverWait(self.selenium,self._TimeOut). \
                                          until(lambda s: self.find_elements(*self._locUserList))                                                            
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)  #failed to obtain a list of users
        
        #[M] review the contents of the submission
        isGivenUserFound = False
        for i in range(len(elmntUserList)):
            try: 
                element = elmntUserList[i]
                #elements
                userName = WebDriverWait(self.selenium,self._TimeOut). \
                                         until(lambda s: element.find_element(*_locUserName))
                userEmail = WebDriverWait(self.selenium,self._TimeOut). \
                                          until(lambda s: element.find_element(*_locUserEmail))
                userRole = WebDriverWait(self.selenium,self._TimeOut). \
                                         until(lambda s: element.find_element(*_locUserRole))
                #texts
                userName_text = userName.text
                userEmail_text = userEmail.text
                userRole_text = userRole.text                                                     
                if userName_text == name and userEmail_text == emailAddr and userRole_text == role:
                    isGivenUserFound = True
                    break      
            except Exceptions.TimeoutException:
                print "let us move on..\n"
        #end
        return isGivenUserFound
        
    #delete the user in the user list
    def delete_user(self, name=None):
    
        #local locators
        _locUser = (By.XPATH, "//h3[attribute::title='"+name+"']/preceding-sibling::div[attribute::class='controls']")
        _locDelButton = (By.CSS_SELECTOR, "button")
    
        #[H] click the "Manage" tab       
        try:
            element = WebDriverWait(self.selenium,self._TimeOut). \
                      until(lambda s: self.find_element(*self._locManageTab))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
        element.click()
        
        #[H] click the "Users" tab
        try:         
            element = WebDriverWait(self.selenium,self._TimeOut). \
                      until(lambda s: self.find_element(*self._locUsersTab))
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)     
        element.click()
          
        #[M] find the user to leave out of the user list
        isGivenUserFound = False
        try: 
            user = WebDriverWait(self.selenium,self._TimeOut). \
                                     until(lambda s: self.find_element(*_locUser))
            #take a delete action on the element       
            delButton = WebDriverWait(self.selenium,self._TimeOut). \
                                          until(lambda s: user.find_element(*_locDelButton))
            isGivenUserFound = True           
        except Exceptions.TimeoutException:
            print "let us move on..\n"

        if isGivenUserFound == True:
            #click the button
            delButton.click()            
        
        #return the outcome in boolean
        return isGivenUserFound


    #    
    #def find_user(self, name=None):
        
    #test
    def test(self):
        
        FilterTermName = "Test Run"
        
        #click the "Manage" tab       
        try:
            element = WebDriverWait(self.selenium,self._TimeOut). \
                      until(lambda s: self.find_element(*self._locManageTab))
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
                #look for the category with the given name
                item_no = 1
                content = 0
                while 1:
                    try:
                        item = element.find_element(By.CSS_SELECTOR, "#id-filter-"+category+"-"+str(item_no))
                        content = item.find_element(By.XPATH, "//label[text()='" + name + "']")
                        if content != 0:
                            break
                        item_no = item_no + 1                      
                    except Exceptions.NoSuchElementException:
                        break
                if content != 0:
                    content.click()
             