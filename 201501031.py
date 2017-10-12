import random
import MySQLdb
import datetime
p=input("Enter the password of your mysql")
def gen():
    m = random.randint(1000,9999)
    return(m)
def initialise():
    db = MySQLdb.connect("localhost","root",p,"mybank")
    c = db.cursor()
    return(db,c)
def set():
    try:
      admin = 'admin'
      password = 'password'
      db = MySQLdb.connect("localhost","root",p)
      c = db.cursor()
      sql = 'CREATE DATABASE MYBANK'
      c.execute(sql)
      db.commit()
      (db,c) = initialise()
      sql1 = 'CREATE TABLE ACHOLDERDETAILS(FIRSTNAME VARCHAR(15) NOT NULL,LASTNAME VARCHAR(15) NOT NULL,USERID VARCHAR(25) NOT NULL,PASSWORD VARCHAR(15) NOT NULL,ADLINE1 VARCHAR(40) NOT NULL,ADLINE2 VARCHAR(40) NOT NULL,CITY VARCHAR(25) NOT NULL,STATE VARCHAR(25) NOT NULL,PINCODE INT(6) NOT NULL,PRIMARY KEY(USERID))'  
      sql2 = 'CREATE TABLE ACDETAILS(ACCOUNTNO INT(15) NOT NULL AUTO_INCREMENT,DATECREATED DATE NOT NULL,ACTYPE VARCHAR(10) NOT NULL,USERID VARCHAR(25)NOT NULL,BALANCE INT(7),PRIMARY KEY(ACCOUNTNO),FOREIGN KEY (USERID) REFERENCES ACHOLDERDETAILS(USERID))'
      sql3 = 'CREATE TABLE ADMIN(ADMINID VARCHAR(20) NOT NULL,APASSWORD VARCHAR(12),PRIMARY KEY(ADMINID))'
      sql4 = 'CREATE TABLE DELETEDACCOUNT(ACCOUNTNO INT(15) NOT NULL,DATECREATED DATE NOT NULL,DATEDELETED DATE NOT NULL,PRIMARY KEY(ACCOUNTNO))'
      sql5 = 'CREATE TABLE TRANSACTION(ACCOUNTNO INT(15) NOT NULL,TYPE VARCHAR(18) NOT NULL,DATE DATE,AMOUNTREM INT(10),TMOUNT int(7))'
      sql6 = 'ALTER TABLE ACDETAILS AUTO_INCREMENT = 100000'
      sql7 = 'INSERT INTO ADMIN VALUES(%s,%s)'
      args = ( admin, password)
      c.execute(sql1)
      c.execute(sql2)
      c.execute(sql3)
      c.execute(sql4)
      c.execute(sql5)
      c.execute(sql6)
      c.execute(sql7,args)
      db.commit()
      print("Required Databases are created")
      postbank()
    except:
        print("Database is already created")
        postbank()
def postbank():
      print ("Welcome to Bank, We care for you\n")                                    
      pa=int(input("1. SignUp[New Customer]\n2. SignIn[Existing Customer]\n3. Admin SignIn\n4. Quit\n\n5.for use in new device\n\n "))    
      if pa == 1:                                                                       
          BankAccount()                              
      elif pa == 2:                                                                     
          ReturnCustomer()
      elif pa == 3:
          Admin()
      elif pa == 4:
          exit()
      elif pa == 5:
          set()
      else:
          print("You have pressed the wrong key, please try again\n")                       
          postbank()
class Admin():
  def __init__(self):
      self.AdminID = input("Enter your AdminID\n")
      self.Password = input("Enter the Password\n")
      (db,c) = initialise()
      c.execute("SELECT APASSWORD  FROM ADMIN WHERE AdminID = '%s'"%self.AdminID)
      passs = c.fetchall()
      passs = passs[0][0]
      if(passs == self.Password):
        self.adminfunctions()
      else:
        print ("Wrong Password\n")
        Admin()
  def adminfunctions(self):
      print ("Welcome %s"%self.AdminID)                                    
      pa=int(input("1. Print Closed Account's History\n2. Admin Logout\n"))
      if pa == 1:                                                                       
        self.printdeletedaccounts()
      elif pa == 2:                                                                     
        print ("Goodbye %s\n\n" %self.AdminID)
        postbank()
  def printdeletedaccounts(self):
      (db,c) = initialise()
      c.execute("SELECT * FROM DELETEDACCOUNT")
      passs = c.fetchall()
      print("______________________")
      print("ACCOUNTNO   |     DATE")
      print("______________________\n\n\n")
      for row in passs:
        no=row[0]
        date=row[1]
        print(no, date)
      db.commit()
      self.adminfunctions()

class UserFunctions():
  def User(self):
      print("\n\nTo access any function below, enter the corresponding key")
      ans=input("\n1.Address Change\n2.Money Deposit\n3.Money Withdrawal\n4.Print Statement\n5.Transfer Money\n6.Account Closure\n7.Customer Logout\n8.Check Balance\n")
      if ans == '1':
        self.passcheck()
        self.addresschange()
      if ans == '5':
        self.passcheck()
        self.transfer()
      if ans == '4':
        self.printstatement()
      if ans == '8':
        self.passcheck()
        self.checkbalance()
      elif ans=='2':
        self.passcheck()
        self.depositcash()
      elif ans=='3':
        self.passcheck()
        self.withdrawcash()
      elif ans=='6':
        self.passcheck()
        self.delete()
      elif ans=='7':
        print("goodbye %s"%self.FirstName)
        postbank()
      else:
        print ("No function assigned to this key, please try again")
        self.User()
  def addresschange(self):
      print ("Hi %s, We are here to Help you to Update your Address"%self.FirstName)
      self.NewAdLine1=input("Enter the New Address line1\n")
      self.NewAdLine2=input("Enter the New Address line\n")
      self.NewCity=input("Enter the New City\n")
      self.NewState=input("Enter the New State\n")
      self.NewPincode=input("Enter the New Pincode\n")
      b=10
      while b>0:
        if(len(str(self.Pincode)) != 6 and type(self.Pincode) != int):
          print("Pincode should have 6 numbers without space and characters")
          self.Pincode=input("Enter the 6-digit Pincode\n")
          b = b-1
        else:
          break
      (db,c) = initialise()
      c.execute("UPDATE ACHOLDERDETAILS SET ADLINE1 = '%s' where userid='%s'"%(self.NewAdLine1,self.UserID))
      c.execute("UPDATE ACHOLDERDETAILS SET ADLINE2 = '%s' where userid='%s'"%(self.NewAdLine2,self.UserID))
      c.execute("UPDATE ACHOLDERDETAILS SET CITY = '%s' where userid='%s'"%(self.NewCity,self.UserID))
      c.execute("UPDATE ACHOLDERDETAILS SET STATE = '%s' where userid='%s'"%(self.NewState,self.UserID))
      c.execute("UPDATE ACHOLDERDETAILS SET PINCODE = %s where userid='%s'"%(self.NewPincode,self.UserID))
      db.commit()
      print ("Your Address is Changed successfully to\n%s\n%s\n%s\n%s\n%s\nGoodBye"%(self.NewAdLine1,self.NewAdLine2,self.NewCity,self.NewState,self.NewPincode))
      self.transact_again()
  def printstatement(self):
      NO=input("Enter your Account Number\n")
      fromdate=input("Enter the Date[yyyy-mm-dd] from which the Transactionhas to be displayed\n")
      todate=input("Enter the Date[yyyy-mm-dd] upto which the Transactionhas to be displayed\n")
      print("Hi %s Your Account Details is here\n "%self.FirstName)
      (db,c) = initialise()
      c.execute("select * from Transaction where AccountNo=%s and date>'%s' and date<'%s'"%(NO,fromdate,todate))
      passs = c.fetchall()
      print("________________________________________________________")
      print("ACCOUNTNO|  TYPE  |   DATE   |BALANCE|TRANSACTION AMOUNT")
      print("________________________________________________________\n\n")
      for row in passs:
          no=row[0]
          typ = row[1]
          date = row[2]
          amt = row[3]
          bal = row[4]
          print(no    ,"|",typ,"|", date ,"|",  amt  ,"|",    bal)
      db.commit()
      self.transact_again()
  def transfer(self):
    try:
      x = 'Transfer'
      amount=int(input("Please enter amount to transfer:\n"))
      NO2=input("Please enter the AccountNO of the Account Holder you want to transfer the money\n\n")
      (db,c) = initialise()
      c.execute("SELECT BALANCE FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
      passs = c.fetchall()
      bal = passs[0][0]
      c.execute("SELECT BALANCE FROM ACDETAILS WHERE ACCOUNTNO=%s"%NO2)
      passs = c.fetchall()
      bal1 = passs[0][0]
      if(self.Actype == 'Current'):
          c = 5000
      if(self.Actype == 'Savings'):
          c = 500
      if(bal-c < amount):
          print("Sorry %s, You Have only Rupees %s in your account\n"%(self.FirstName,bal))
          self.transact_again()
      if(bal-c > amount):
          bal = bal - amount
          bal1 = bal1 + amount
          date = datetime.datetime.now().date()
          (db,c) = initialise()
          c.execute("UPDATE ACDETAILS SET BALANCE = %s where userid='%s'"%(bal,self.UserID))
          c.execute("UPDATE ACDETAILS SET BALANCE = %s where ACCOUNTNO=%s"%(bal1,NO2))
          db.commit()
          (db,c) = initialise()
          c.execute("SELECT BALANCE FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
          bal = c.fetchall()
          bal = bal[0][0] 
          print ("Your new account balance is %s" %bal)
          (db,c) = initialise()
          c.execute("INSERT INTO  TRANSACTION VALUES(%s,'%s','%s',%s,%s)"%(self.AccountNO,x,date,bal,amount))
          db.commit()
          self.transact_again()
    except IndexError:
        print("Account Number of the Second user Doesn't Exixts")
        self.transact_again()
  def delete(self):
    try:
      print ("%s, your account is being deleted"%self.UserID)
      print ("Minions at work")
      delet=datetime.datetime.now().date()
      (db,c) = initialise()
      c.execute("SELECT DATECREATED FROM ACDETAILS WHERE USERID = '%s'"%(self.UserID))
      passs = c.fetchall()
      date=passs[0][0]
      c.execute("INSERT INTO  DELETEDACCOUNT VALUES(%s,'%s','%s')"%(self.AccountNO,date,delet))
      db.commit()
      (db,c) = initialise()
      c.execute("SET FOREIGN_KEY_CHECKS = 0")
      c.execute("DELETE FROM ACHOLDERDETAILS WHERE USERID = '%s'"%(self.UserID))
      c.execute("DELETE FROM ACDETAILS WHERE USERID = '%s'"%(self.UserID))
      c.execute("SET FOREIGN_KEY_CHECKS = 1")
      db.commit()
      print ("Your account has been successfully deleted, goodbye")
      postbank()
    except IndexError:
        print("Your Account is alreasy deleted")
  def deleteauto(self):
      delet=datetime.datetime.now().date()
      (db,c) = initialise()
      c.execute("SELECT DATECREATED FROM ACDETAILS WHERE USERID = '%s'"%(self.UserID))
      passs = c.fetchall()
      date=passs[0][0]
      c.execute("INSERT INTO  DELETEDACCOUNT VALUES(%s,'%s','%s')"%(self.AccountNO,date,delet))
      db.commit()
      (db,c) = initialise()
      c.execute("SET FOREIGN_KEY_CHECKS = 0")
      c.execute("DELETE FROM ACHOLDERDETAILS WHERE USERID = '%s'"%(self.UserID))
      c.execute("DELETE FROM ACDETAILS WHERE USERID = '%s'"%(self.UserID))
      c.execute("SET FOREIGN_KEY_CHECKS = 1")
      db.commit()
      postbank()
  def checkbalance(self):
      (db,c) = initialise()
      c.execute("SELECT BALANCE FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
      bal = c.fetchone()
      print ("Your account balance is %s" %bal)
      self.transact_again()
  def withdrawcash(self):   
        x = 'Withdrawal'
        amount=int(input("Please enter amount to withdraw:\n"))
        (db,c) = initialise()
        c.execute("SELECT BALANCE FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
        bal = c.fetchall()
        bal = bal[0][0]
        if(self.Actype == 'Current'):
          c = 5000
        if(self.Actype == 'Savings'):
          c = 500
        if(bal-c < amount):
          print("Sorry %s, You Have only Rupees %s in your account please try again\n\n"%(self.FirstName,bal))
          self.transact_again()
        if(bal-c > amount):
          bal = bal - amount;
          date = datetime.datetime.now().date()
          (db,c) = initialise()
          c.execute("UPDATE ACDETAILS SET BALANCE = %s where userid='%s'"%(bal,self.UserID))
          db.commit()
          (db,c) = initialise()
          c.execute("SELECT BALANCE FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
          bal = c.fetchall()
          bal = bal[0][0] 
          print ("Your new account balance is %s" %bal)
          (db,c) = initialise()
          c.execute("INSERT INTO  TRANSACTION VALUES(%s,'%s','%s',%s,%s)"%(self.AccountNO,x,date,bal,amount))
          db.commit()
          self.transact_again()
    
  def depositcash(self):
      x = 'Deposit'
      amount=int(input("Please enter amount to be deposited:\n"))
      (db,c) = initialise()
      c.execute("SELECT BALANCE FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
      bal = c.fetchall()
      bal = bal[0][0]
      bal = bal + amount
      date = datetime.datetime.now().date()
      (db,c) = initialise()
      c.execute("UPDATE ACDETAILS SET BALANCE = %s where userid='%s'"%(bal,self.UserID))
      db.commit()
      (db,c) = initialise()
      c.execute("SELECT BALANCE FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
      bal = c.fetchall()
      bal = bal[0][0]
      print ("Your new account balance is %s" %bal)
      (db,c) = initialise()
      c.execute("INSERT INTO  TRANSACTION VALUES(%s,'%s','%s',%s,%s)"%(self.AccountNO,x,date,bal,amount))
      db.commit()
      self.transact_again()
  def passcheck(self):
      print("""Please enter the Password to Complete Your Transaction\n""")
      b=3
      while b>0:
        self.Password = input("Enter the Password\n")
        (db,c) = initialise()
        c.execute("SELECT PASSWORD FROM ACHOLDERDETAILS WHERE USERID='%s'"%self.UserID)
        passs = c.fetchall()
        passs = passs[0][0]
        if(self.Password == passs):
          return True
        else:
          print ("Wrong Password")
          b-=1
          print ("%d more attempt(s) remaining" %b)
      print ("Account has been freezed due to three wrong password attempts,\n contact your bank for help, bye bye")
      print ("...")
      print("...")
      exit()
  def transact_again(self):
      ans=input("Do you want to do any other transaction? (y/n)\n").lower()
      if ans=='y':
        self.User()
      elif ans=='n':
        print ("Thank you for using PostBank we value you. Have a good day")
        print ("Goodbye %s" %self.UserID)
        exit()
      elif ans!='y' and ans!='n':
        print ("Unknown key pressed, please choose either 'N' or 'Y'")
        self.transact_again()

class BankAccount(UserFunctions):
  def __init__(self):
    self.FirstName=input("Enter the First Name\n")
    self.LastName=input("Enter the Last Name\n")
    self.AdLine1=input("Enter the Address line1\n")
    self.AdLine2=input("Enter the Address line\n")
    self.City=input("Enter the City\n")
    self.State=input("Enter the State\n")
    self.Pincode=input("Enter the 6-digit Pincode\n")
    b=10
    while b>0:
      if(len(str(self.Pincode)) != 6 and type(self.Pincode) != int):
        print("Pincode should have 6 numbers without space")
        self.Pincode=input("Enter the 6-digit Pincode\n")
        b = b-1
      else:
          break
    self.Actype=input("Enter the type of account(Savings/Current)\n")
    self.Password=input("Enter the password\n")
    self.UserID = self.FirstName +'_'+ str(gen())
    print("Your User Id is %s"%self.UserID)
    (db,c) = initialise()
    sql='INSERT INTO AcHolderDetails VALUES(%s , %s , %s , %s , %s , %s , %s , %s , %s)'
    args = [self.FirstName , self.LastName , self.UserID , self.Password , self.AdLine1 , self.AdLine2 , self.City , self.State , self.Pincode]
    c.execute(sql,args)
    db.commit()
    if(self.Actype == 'Savings'):
      self.Balance=int(input("Enter the amount Of Initial Deposit\n"))
      b = 3
      while b>0:
        if(self.Balance < 500):
          print("Current Account should have atleast 5000 initial amount\n")
          self.Balance = int(input("Enter the amount Of Initial Deposit greater than 500\n"))
          b = b-1
        else:
            break
      self.datecreated=datetime.datetime.now().date()
      (db,c) = initialise()
      sql2="insert into acdetails(DATECREATED,ACTYPE,USERID,BALANCE) values(%s,%s,%s,%s)"
      record = [self.datecreated, self.Actype, self.UserID, self.Balance]
      c.execute(sql2, record)
      db.commit()
      (db,c) = initialise()
      c.execute("SELECT ACCOUNTNO,DATECREATED FROM ACDETAILS WHERE USERID = '%s'"%(self.UserID))
      passs = c.fetchall()
      self.AccountNO=passs[0][0]
      print("Your Account Number is %s\n"%(self.AccountNO))
      print("Thank you %s, your account is set up and ready to use,\n a %s Rupees has been credited to your %s account\n" %(self.FirstName,self.Balance,self.Actype))
      self.User()
    elif(self.Actype == 'Current'):
      self.Balance = int(input("Enter the amount Of Initial Deposit\n"))
      b = 3
      while b>0:
        if(self.Balance < 5000):
          print("Current Account should have atleast 5000 initial amount\n")
          self.Balance = int(input("Enter the amount Of Initial Deposit greater than 5000\n"))
          b = b-1
        else:
            break
      self.datecreated=datetime.datetime.now().date()
      (db,c) = initialise()
      sql1="insert into acdetails(DATECREATED,ACTYPE,USERID,BALANCE) values(%s,%s,%s,%s)"
      record = [self.datecreated, self.Actype, self.UserID, self.Balance]
      c.execute(sql1, record)
      db.commit()
      (db,c) = initialise()
      c.execute("SELECT ACCOUNTNO FROM ACDETAILS WHERE USERID = '%s'"%(self.UserID))
      passs = c.fetchall()
      self.AccountNO=passs[0][0]
      print("Your Account Number is %s\n"%(self.AccountNO))
      print("Thank you %s, your account is set up and ready to use,\n a %s Rupees has been credited to your %s account\n" %(self.FirstName,self.Balance,self.Actype))
      self.User()
    else:
      print("Your account type is wrong please Register again with correct Account Type\n ")
      BankAccount()
class ReturnCustomer(UserFunctions):
  def __init__(self):
    try:
      b = 3
      while b>0:
        self.UserID = input("Enter the UserID\n")
        self.Password = input("Enter the Password\n")
        (db,c) = initialise()
        c.execute("SELECT FIRSTNAME,PASSWORD FROM ACHOLDERDETAILS WHERE USERID='%s'"%self.UserID)
        passs = c.fetchall()
        self.FirstName = passs[0][0]
        p = passs[0][1]
        c.execute("SELECT ACTYPE,ACCOUNTNO FROM ACDETAILS WHERE USERID='%s'"%self.UserID)
        passs = c.fetchall()
        self.Actype = passs[0][0]
        self.AccountNO=passs[0][1]
        if(p == self.Password):
          self.User()
        else:
          print ("Wrong Password")
          b-=1
          print ("%d more attempt(s) remaining" %b)
      print ("Account has been freezed due to three wrong password attempts,\n contact your bank for help, bye bye\n")
      self.deleteauto()
    except IndexError:
        print("UserID doesn't Exists")
        postbank()

postbank()

