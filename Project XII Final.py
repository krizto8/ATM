import sys
import mysql.connector
import time
import random
import json
import pickle
import matplotlib.pyplot as py

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print("\n              W E L C O M E   T O   T H E    A T M")
print("              ************************************")
print("\n    Before using the ATM, User Database has to be Created")
input("\n                  Click ENTER to continue")

cardlist=[]


mydb=mysql.connector.connect(host="localhost",user="root",passwd="123456",database="ATM")
mycursor=mydb.cursor()

#mycursor.execute("create database ATM")

input("\n     ATM database established! Click ENTER to continue")

mycursor.execute("create table User(Name varchar(20),Age int(2),AC_Number int(10) primary key,Card_Number int(16),PIN int(4),Balance_Amt int(10),Acc_Type varchar(10))")

print("\n|------------------------------------------------------------------------------|")

n=int(input("\nEnter the number of User Records You want to add:"))

for i in range(n):

    name=input("\nEnter the Name:")
    age=int(input("Enter the age:"))
    ac=int(input("Enter the Account number:"))
    cn=int(input("Enter the Card number:"))
    pn=int(input("Enter the PIN:"))
    bal=int(input("Enter your Account Balance(INR):"))
    typ=input("Enter the Account type(Current/Savings):")
    qry=("insert into User values(%s,%s,%s,%s,%s,%s,%s)")
    data=(name,age,ac,cn,pn,bal,typ)
    mycursor.execute(qry,data)
    mydb.commit()
    cardlist.append(cn)

ballist=[bal] #For storing all the balance values for plotting balance monitor
localtime1=time.asctime(time.localtime(time.time()))
datelist=[localtime1]

input("\nData Succesfully Stored in Database. Click ENTER to Proceed")

print("\n|------------------------------------------------------------------------------|")

while True:
    cn=int(input("\nEnter Your Card number to Initiate the ATM:"))
    if cn not in cardlist:
        sys.stderr.write("Card Not Found. Try Again\n")
        continue
    
        
    pin1=int(input("Enter the PIN number:"))
    print("\n|------------------------------------------------------------------------------|")


#VARIABLES----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    mycursor.execute("select Card_Number from User where Card_Number=%s"%(cn,))
    crd=mycursor.fetchone()
    card=crd[0]

    mycursor.execute("select PIN from User where Card_Number=%s"%(cn,))
    pn=mycursor.fetchone()
    pin=pn[0]

    mycursor.execute("select Name from User where Card_Number=%s"%(cn,))
    nm=mycursor.fetchone()
    name=nm[0]

    mycursor.execute("select AC_Number from User where Card_Number=%s"%(cn,))
    acn=mycursor.fetchone()
    acc=acn[0]

    mycursor.execute("select Balance_Amt from User where Card_Number=%s"%(cn,))
    blm=mycursor.fetchone()
    bal=blm[0]

    mycursor.execute("select Acc_Type from User where Card_Number=%s"%(cn,))
    act=mycursor.fetchone()
    typ=act[0]

    mycursor.execute("select Age from User where Card_Number=%s"%(cn,))
    ag=mycursor.fetchone()
    age=ag[0]

    piewithdrawal=0
    piedeposit=0
    piefund=0
    piepin=0




#ACCOUNT DETAILS---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

    if pin==pin1:
        
        print("\n           ACCOUNT DETAILS")
        print("           ---------------")
        print("     NAME              :",name)
        print("     AGE               :",age)
        print("     ACCOUNT NO.       :",acc)
        print("     CARD NUMBER       :",card)
        print("     BALANCE AMT       :",bal,"INR")
        print("     ACCOUNT TYPE      :",typ)

        


        
    else:
        sys.stderr.write("Incorrect PIN. Start Over!\n")
        continue

#FUNCTIONS---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def Cash_Withdrawal():
        global bal
        global piewithdrawal
        
        num=int(input("Enter your 4 Digit PIN:"))
        if num==pin:
            print("\nYour Account Balance is:",bal,"INR")
            print("\nAccount Type:",typ)

            while True:

                amt=int(input("\nEnter the Amount You want to Withdraw:"))
                input("Click ENTER to continue")
                if amt>bal:
                    sys.stderr.write("Insufficient Balance!\n")
                    continue
                else:

                    bal=bal-amt
                    ballist.append(bal)
                    upd=("update User set Balance_Amt=%s where Card_Number=%s")
                    one=(bal,cn)
                    

                    mycursor.execute(upd,one)
                    mydb.commit()
                    time.sleep(2)
                    print("\nTransaction Succesful. Updated Balance Amount:",bal,"INR")

                    accdict={"NAME":name,"AGE":age,"ACCOUNT NO.":acc,"CARD NUMBER":card,"BALANCE AMT":bal,"ACCOUNT TYPE":typ}
                    accdict["Amount Withdrawn"]=amt

                    localtime=time.asctime(time.localtime(time.time()))
                    datelist.append(localtime)
                    accdict["Date_And_Time"]=localtime
                    
                    myfile=open(r"C:\Users\dell\Desktop\RECEIPT.txt","w")
                    myfile.writelines(json.dumps(accdict))
                    print("\nTransaction Receipt in RECEIPT file")


                    trans=open(r"C:\Users\dell\Desktop\Transaction_History.dat","ab")
                    dict={"Amount Withdrawn":amt,"Balance":bal,"Date_And_Time":localtime}
                    pickle.dump(dict,trans)
                    trans.close()
                    print("\n|------------------------------------------------------------------------------|")
                    piewithdrawal+=1
                    break
        else:
            sys.stderr.write("Incorrect PIN\n")
        

    def Cash_Deposit():
        global bal
        global piedeposit
        

        num=int(input("Enter your 4 Digit PIN:"))
        if num==pin:
            print("\nYour Account Balance is:",bal,"INR")
            print("\nAccount Type:",typ)
            amt=int(input("\nEnter the Amount You Want to Deposit:"))
            input("\nClick ENTER to continue")
            input("\nInsert Your Money on the Slot and Press ENTER key")
            bal=bal+amt
            ballist.append(bal)
            upd=("update User set Balance_Amt=%s where Card_Number=%s")
            one=(bal,cn)
            mycursor.execute(upd,one)
            mydb.commit()
            
            time.sleep(2)
            print("\nTransaction Succesfull. Your Current Account Balance is:",bal,"INR")

            accdict={"NAME":name,"AGE":age,"ACCOUNT NO.":acc,"CARD NUMBER":card,"BALANCE AMT":bal,"ACCOUNT TYPE":typ}
            accdict["Amount Deposited"]=amt

            localtime=time.asctime(time.localtime(time.time()))
            datelist.append(localtime)
            accdict["Date_And_Time"]=localtime
            
            myfile=open(r"C:\Users\dell\Desktop\RECEIPT.txt","w")
            myfile.writelines(json.dumps(accdict))
            print("\nTransaction Receipt in RECEIPT file")


            trans=open(r"C:\Users\dell\Desktop\Transaction_History.dat","ab")
            dict={"Amount Deposited":amt,"Balance":bal,"Date_And_Time":localtime}
            pickle.dump(dict,trans)
            trans.close()
            print("\n|------------------------------------------------------------------------------|")
            piedeposit+=1

        else:
           sys.stderr.write("Incorrect PIN\n")

    def Fund_Transfer():
        global bal
        global piefund
        

        num=int(input("Enter your 4 Digit PIN:"))
        if num==pin:
            print("\nYour Account Balance is:",bal,"INR")
            print("\nAccount Type:",typ)
            ben=int(input("\nEnter the Bank Account Number of the Benificiary:"))
            print("\nYour Daily Transaction Limit is 50,000 INR")

            while True:

                amt=int(input("\nEnter the Amount You want to Transfer:"))
                if amt<bal and amt<50000:
                    input("\nClick ENTER to Confirm")
                    print("\nProcessing")
                    time.sleep(2)
                    bal=bal-amt
                    ballist.append(bal)
                    upd=("update User set Balance_Amt=%s where Card_Number=%s")
                    one=(bal,cn)

                    mycursor.execute(upd,one)
                    mydb.commit()
                    print("\nTransaction Succesfull. Your Current Account Balance is:",bal,"INR")

                    accdict={"NAME":name,"AGE":age,"ACCOUNT NO.":acc,"CARD NUMBER":card,"BALANCE AMT":bal,"ACCOUNT TYPE":typ}
                    accdict["Amount Transferred"]=amt
                    accdict["Beneficiary AC Number"]=ben

                    localtime=time.asctime(time.localtime(time.time()))
                    datelist.append(localtime)
                    accdict["Date_And_Time"]=localtime
                    
                    myfile=open(r"C:\Users\dell\Desktop\RECEIPT.txt","w")
                    myfile.writelines(json.dumps(accdict))
                    print("\nTransaction Receipt in RECEIPT file")


                    trans=open(r"C:\Users\dell\Desktop\Transaction_History.dat","ab")
                    dict={"Amount Transferred":amt,"Balance":bal,"Beneficiary AC Number":ben,"Date_And_Time":localtime}
                    pickle.dump(dict,trans)
                    trans.close()
                    print("\n|------------------------------------------------------------------------------|")
                    piefund+=1
                    break

                elif amt>bal:
                   sys.stderr.write("Insufficient Balance\n")
                   continue
                elif amt>50000:
                   sys.stderr.write("Amount Exceeded Transaction limit\n")
                   continue
        else:
           sys.stderr.write("Incorrect PIN\n") 
                
            
    def Pin_Change():
        global piepin
        
        
        num=int(input("\nEnter your 4 Digit PIN:"))
        if num==pin:
            input("Click ENTER to proceed to change PIN")
            pin2=int(input("\nEnter the Current PIN:"))
            if pin2==num:
                pin3=int(input("\nEnter the New PIN:"))
                while True:
                    pin4=int(input("\nPlease Enter the New PIN to Confirm:"))
                    if pin3==pin4:
                        upd=("update User set PIN=%s where Card_Number=%s")
                        one=(pin3,cn)

                        mycursor.execute(upd,one)
                        mydb.commit()
                        print("PIN Changed Succesfully!")
                        localtime=time.asctime(time.localtime(time.time()))

                        act=open(r"C:\Users\dell\Desktop\Activity.dat","ab")
                        dict1={"Activity":"PIN Changed","Date_And_Time":localtime}
                        pickle.dump(dict1,act)
                        act.close()
                        print("\n|------------------------------------------------------------------------------|")
                        piepin+=1

                        break
                    else:
                        sys.stderr.write("Password Mismatch! Try Again.\n")
                        continue
            else:
               sys.stderr.write("Incorrect PIN Entered\n") 
        else:
            sys.stderr.write("Incorrect PIN\n")
            
    def Acc_Info():
        print("\nSelect Your Desired Service")
        print("---------------------------")
        print("\n >> 1.Transaction History       2. Account Visualisation         3.Account Activity")
        choose=int(input("\nEnter Your Choice:"))
        if choose==1:
            hist=open(r"C:\Users\dell\Desktop\Transaction_History.dat","rb")
            while True:
                try:
                    hist1=pickle.load(hist)
                    print(hist1)
                except EOFError:
                    break
                
        if choose==2:
            print(">> 1. Activity Chart     2. Balance Monitor")
            get=int(input("Enter the Choice:"))
            if get==1:
                info=[piewithdrawal,piedeposit,piefund,piepin]
                data=["Withdrawals","Deposits","Fund Transfers","PIN Change"]
                py.pie(info,labels=data,autopct="%2.2f%%")
                py.title("No. of Transactions")
                py.show()
            elif get==2:
                py.plot(ballist,datelist,"g",linestyle="dotted",marker="d")
                py.ylabel("Date and Time")
                py.xlabel("Balance(INR)")
                py.title("Balance Monitor")
                py.show()
                
                


        if choose==3:
            try:
                hist=open(r"C:\Users\dell\Desktop\Activity.dat","rb")
                while True:
                    try:
                        hist1=pickle.load(hist)
                        print(hist1)
                    except EOFError:
                        break
            except FileNotFoundError:
                print("PIN not changed yet!")

        



#MAIN----------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("\n|------------------------------------------------------------------------------|")


    print("\n                     S E R V I C E S")
    print("                     ===============")
    print("\n    1.Cash Withdrawal                    2.Cash Deposit")
    print("\n    3.Fund Transfer                      4.Change PIN")
    print("\n    5.Account Information Inquiry        6.EXIT")
    while True:

        choice=int(input("\n<> Select the Serial Number of the Service you want or Hit 6 to EXIT:"))

        if choice==1:
            Cash_Withdrawal()
            

        elif choice==2:
            Cash_Deposit()
            
        elif choice==3:
            Fund_Transfer()

        elif choice==4:
            Pin_Change()

        elif choice==5:
            Acc_Info()
    
        elif choice==6:
            print("\n >>> Thank You For Using The ATM <<<")
            break
        else:
            print("\n Invalid Input!")

    break










