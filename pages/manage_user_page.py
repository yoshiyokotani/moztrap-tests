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
from sqlalchemy.sql.operators import isnot

class MozTrapManageUserPage(MozTrapBasePage):

    _page_title = 'Manage User'
    
    #common locators
    _locManageTab = (By.XPATH, "//ul//li/child::a[text()='Manage']")    
    _locUsersTab = (By.XPATH, "//div/ul//child::a[text()='Users']") 
    _locUserList = (By.XPATH, "//child::article[attribute::class='listitem']")
    _locAddUser = (By.XPATH, "//div[attribute::class='form-actions']/child::button")

    _locStatusSelectButton = (By.CSS_SELECTOR, "div.status-title")

    #constants
    _TimeOut = 30

    #move to the user page
    def __move_to_user_page(self):

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
        
    #add a new user into the user list
    def create_user(self, name=None, emailAddr=None, role=None, isActive=None):     
        
        #local locators          
        _locCreateUser = (By.XPATH, "//child::section/a[text()='create a user']")        
        _locNewUserName = (By.XPATH, "//child::input[attribute::id='id_username']")
        _locNewUserEmail = (By.XPATH, "//child::input[attribute::id='id_email']")
        _locNewUserRole = (By.XPATH, "//child::select[attribute::id='id_groups']")
        _locNewUserStatus = (By.XPATH, "//child::input[@id='id_is_active']")  
        _locErrList = (By.XPATH, "//child::ul[attribute::class='errorlist']")               
        
        #[H] move to the user page
        self.__move_to_user_page()

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
            elmntStatus = WebDriverWait(self.selenium,self._TimeOut). \
                                        until(lambda s: self.find_element(*_locNewUserStatus))                                                                                  
            elmntActions = WebDriverWait(self.selenium,self._TimeOut). \
                                         until(lambda s: self.find_element(*self._locAddUser))
            
            elmntName.send_keys(name)
            elmntEmail.send_keys(emailAddr)
            if isActive != None and isActive == 0:
                elmntStatus.click()     #set as an inactive user
                                                         
        except Exceptions.TimeoutException:
            Assert.fail(Exceptions.TimeoutException)
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

        #[M] just check if the added user can be found in the DB
        element = self.__find_user(name, emailAddr, role)
        if element is None:
            return False
        else:
            return True
        
    #delete the user in the user list
    def delete_user(self, name=None):
    
        #local locators
        _locUser = (By.XPATH, "//h3[attribute::title='"+name+"']/preceding-sibling::div[attribute::class='controls']")
        _locDelButton = (By.CSS_SELECTOR, "button")
    
        #[H] move to the user page
        self.__move_to_user_page()
          
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
    #find the given user in the DB.
    #
    # return value:
    #    None    : not found
    #    element : found user element
    #
    def __find_user(self, name=None, emailAddr=None, role=None):
    
        #local locators
        _locUserName = (By.CSS_SELECTOR, "h3.title")
        _locUserEmail = (By.CSS_SELECTOR, "div.email")
        _locUserRole = (By.CSS_SELECTOR, "ul.roles") 
        
        #move to the user page
        self.__move_to_user_page()
        
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
                
                #check the attributes
                isNameMatched = False
                if name != None and name == userName_text:
                    isNameMatched = True
                isEmailMatched = False
                if emailAddr != None and emailAddr == userEmail_text:
                    isEmailMatched = True
                isRoleMatched = False
                if role != None and role == userRole_text:
                    isRoleMatched = True
                isGivenUserFound = isNameMatched
                if isGivenUserFound == True:
                    break      
            except Exceptions.TimeoutException:
                print "let us move on..\n"
        
        #post-processing
        if isGivenUserFound == False:
            element = None
        return element
                
    #change the role of the given user
    def change_user_role(self, name=None, emailAddr=None, role=None, newRole=None):

        #local locators
        _locEditButton = (By.CSS_SELECTOR, "a.edit-link")        
        _locRoleOption = (By.XPATH, "//option[attribute::value][text()='"+newRole+"']" )    
            
        #move to the user page
        self.__move_to_user_page()
                
        #find the given user 
        user = self.__find_user(name, emailAddr, role)
        if user is None:
            print "the given user is not found in the DB.\n"
            return False
        else:
            #click the edit button
            try:
                button = WebDriverWait(self.selenium,self._TimeOut). \
                                       until(lambda s: user.find_element(*_locEditButton))
                button.click()
            except Exceptions.TimeoutException:
                print "the edit button was not found.\n"
                return False
            
            #search for the new role in the roles box and select it
            try:
                roleOption = WebDriverWait(self.selenium,self._TimeOut). \
                                           until(lambda s: self.find_element(*_locRoleOption))
                roleOption.click()
            except Exceptions.TimeoutException:          
                print "the given new role was not found.\n"
                return False
            
            #click the submit button
            try:
                submitButton = WebDriverWait(self.selenium,self._TimeOut). \
                                             until(lambda s: self.find_element(*self._locAddUser))
                submitButton.click()
            except Exceptions.TimeoutException:          
                print "the submit button was not found.\n"
                return False            
            
            #make sure that the user with the new role can be found in the list
            if self.__find_user(name, emailAddr, newRole) is None:
                return False
            else:
                return True
            
    #activate via switch of the user editing page                 
    def activate_user(self, userName=None):
    
        #local locator
        _locActiveStatusAction = (By.XPATH, "//button[@class='active status-action' and @name='action-activate']")

        #find the element associated with the given user
        user = self.__find_user(userName)
        if user is None:
            print "the given user is not found.\n"
            return False
        else:
            try:
                statusSelectButton = WebDriverWait(self.selenium,self._TimeOut). \
                                                   until(lambda s: user.find_element(*self._locStatusSelectButton))
            except Exceptions.TimeoutException:          
                print "the submit button was not found.\n"
            #check the current status of the button
            status = statusSelectButton.text
            if status == 'active':
                #the current status is active, so no further action is needed
                print "the user is already active.\n"
            else:
                #the current status is inactive, so click the button for the activation
                statusSelectButton.click()
                try:
                    activateButton = WebDriverWait(self.selenium,self._TimeOut). \
                                                       until(lambda s: self.find_element(*_locActiveStatusAction))
                    activateButton.submit()                                                       
                except Exceptions.TimeoutException:          
                    print "the activate button was not found.\n"               
            return True
    
    #deactivate via switch of the user editing page  
    def deactivate_user(self, userName=None):
 
        #local locator        
        _locDisabledStatusAction = (By.XPATH, "//button[@class='disabled status-action' and @name='action-deactivate']")
        
        #find the element associated with the given user
        user = self.__find_user(userName)
        if user is None:
            print "the given user is not found.\n"
            return False
        else:
            try:
                statusSelectButton = WebDriverWait(self.selenium,self._TimeOut). \
                                                   until(lambda s: user.find_element(*self._locStatusSelectButton))
            except Exceptions.TimeoutException:          
                print "the submit button was not found.\n"
            #check the current status of the button
            status = statusSelectButton.text
            if status == 'active':
                #the current status is active, so click the button for the deactivation
                statusSelectButton.click()
                try:
                    deactivateButton = WebDriverWait(self.selenium,self._TimeOut). \
                                                     until(lambda s: user.find_element(*_locDisabledStatusAction))
                    #deactivateButton.click() 
                    deactivateButton.submit()    
                except Exceptions.TimeoutException:          
                    print "the submit button was not found.\n"
                                                                  
            else:
                #the current status is inactive, so no further action is needed
                print "the user is already inactive.\n"
            return True
               
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
                content is None
                while 1:
                    try:
                        item = element.find_element(By.CSS_SELECTOR, "#id-filter-"+category+"-"+str(item_no))
                        content = item.find_element(By.XPATH, "//label[text()='" + name + "']")
                        if content is not None:
                            break
                        item_no = item_no + 1                      
                    except Exceptions.NoSuchElementException:
                        break
                if content is not None:
                    content.click()
             