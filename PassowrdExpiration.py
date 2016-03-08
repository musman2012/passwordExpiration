from org.jboss.seam.security import Identity
from org.xdi.model.custom.script.type.auth import PersonAuthenticationType
from org.xdi.oxauth.service import UserService
from org.xdi.util import StringHelper
from org.xdi.util import ArrayHelper
import java.util.Calendar

import java

class PersonAuthentication(PersonAuthenticationType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Basic (with password update). Initialization"
        print "Basic (with password update). Initialized successfully"
        return True   

    def destroy(self, configurationAttributes):
        print "Basic (with password update). Destroy"
        print "Basic (with password update). Destroyed successfully"
        return True

    def getApiVersion(self):
        return 1

    def isValidAuthenticationMethod(self, usageType, configurationAttributes):
        return True

    def getAlternativeAuthenticationMethod(self, usageType, configurationAttributes):
        return None

    def authenticate(self, configurationAttributes, requestParameters, step):
        credentials = Identity.instance().getCredentials()
        user_name = credentials.getUsername()

        if (step == 1):
            print "Basic (with password update). Authenticate for step 1"

            user_password = credentials.getPassword()

            logged_in = False
            if (StringHelper.isNotEmptyString(user_name) and StringHelper.isNotEmptyString(user_password)):
                userService = UserService.instance()
                logged_in = userService.authenticate(user_name, user_password)

            if (not logged_in):
                return False

            return True
        elif (step == 2):
            print "Basic (with password update). Authenticate for step 2"

            userService = UserService.instance()

            update_button = requestParameters.get("loginForm:updateButton")
            if ArrayHelper.isEmpty(update_button):
                return True

            new_password_array = requestParameters.get("new_password")
            if ArrayHelper.isEmpty(new_password_array) or StringHelper.isEmpty(new_password_array[0]):
                print "Basic (with password update). Authenticate for step 2. New password is empty"
                return False

            new_password = new_password_array[0]

            print "Basic (with password update). Authenticate for step 2. Attemprin to set new user '" + user_name + "' password"

            find_user_by_uid = userService.getUser(user_name)
           
            if (find_user_by_uid == None):
                print "Basic (with password update). Authenticate for step 2. Failed to find user"
                return False

            print "Get Attribute is going to be called!!!!123!"

            user_dispName = find_user_by_uid.getAttribute("displayName", False)

            if (user_dispName == None):
                print "Failed to get Mail"
                return False
 
            print "Mail is : '" + user_dispName + "' ."

            find_user_by_uid.setAttribute("oxPasswordExpirationDate", "20160213195000Z")

            user_expDate = find_user_by_uid.getAttribute("oxPasswordExpirationDate", False)

            if (user_expDate == None):
                    print "Failed to get Date"
                    return False

            print "Exp Date is : '" + user_expDate + "' ."

            myDate = GluuDate(user_expDate)

            expYear = myDate.getYear()

            print "Year of password expiration is" + expYear

            userService.updateUser(find_user_by_uid)
            print "Basic (with password update). Authenticate for step 2. Password updated successfully"

            return True
        else:
            return False

    def prepareForStep(self, configurationAttributes, requestParameters, step):
        if (step == 1):
            print "Basic (with password update). Prepare for Step 1"
            return True
        elif (step == 2):
            print "Basic (with password update). Prepare for Step 2"
            return True
        else:
            return False

    def getExtraParametersForStep(self, configurationAttributes, step):
        return None

    def getCountAuthenticationSteps(self, configurationAttributes):
        return 2

    def getPageForStep(self, configurationAttributes, step):
        if (step == 2):
            return "/auth/pwd/newpassword.xhtml"

        return ""

    def logout(self, configurationAttributes, requestParameters):
        return True

class GluuDate:
    def __init__(self, LDAPDate):
        self.LDAPDate = LDAPDate

    def getYear(self):
        year = self.LDAPDate[0:4]
        return year

    def getMonth(self):
        month = self.LDAPDate[4:6]
        return month

    def getDate(self):
        date = self.LDAPDate[6:8]
        return date



