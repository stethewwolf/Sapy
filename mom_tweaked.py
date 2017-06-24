import datetime
import uuid

class MoM():
    def __init__(self,Stamp=str(datetime.datetime.now().time())+" : "+str(datetime.datetime.now().date())):
        self.id=None
        self.Direction=0
        self.price=None
        self.cause=None
        self.Agent=None
        self.Payee=None
        self.Stamp=Stamp
        self.Parameter={}

    def data_movement(self):

        if 'id' in self.Parameter:
            self.Parameter.setdefault('id',[]).append(self.id)
        else:
            self.Parameter['id']=[self.id]

        if 'Cause' in self.Parameter:
            self.Parameter.setdefault('Cause',[]).append(self.cause)
        else:
            self.Parameter['Cause']=[self.cause]

        if 'Direction' in self.Parameter:
            self.Parameter.setdefault('Direction',[]).append(self.Direction)
        else:
            self.Parameter['Direction']=[self.Direction]

        if 'Agent' in self.Parameter:
            self.Parameter.setdefault('Agent',[]).append(self.Agent)
        else:
            self.Parameter['Agent']=[self.Agent]

        if 'Payee' in self.Parameter:
            self.Parameter.setdefault('Payee',[]).append(self.Payee)
        else:
            self.Parameter['Payee']=[self.Payee]

        if 'Stamp' in self.Parameter:
            self.Parameter.setdefault('Stamp',[]).append(self.Stamp)
        else:
            self.Parameter['Stamp']=[self.Stamp]
        if 'Price' in self.Parameter:
            self.Parameter.setdefault('Price',[]).append(self.price)
        else:
            self.Parameter['Price']=[self.price]

        print(self.Parameter)

    def transfer(self):
        print("Transfer screen")
        while(True):
            self.id=uuid.uuid4().hex
            mode = input("Do you want To Transfer(T) or Deposit(D) or Inquiry(I)")
            if mode == 'T':
                self.to()
                self.data_movement()
            elif mode=='D':
                self.from_()
                self.data_movement()
            elif mode=='I':
                self.inquiry_by_Agent()
            if input("Do you want to leave the screen Y/N") =='Y':
                exit(0)

    def to(self):
        print("Transferring initiated .. ")
        self.Direction=-1
        self.Agent=input("Enter the sender")
        self.Payee=input("Enter the receiver")
        self.price=input("Enter the money for the transfer")
        self.cause=input("Enter the motive of transfer")
        print("Committing and exiting..")

    def from_(self):
        print("Depositing .. ")
        self.Direction=1
        self.Agent=input("Enter the sender")
        self.Payee=input("Enter the receiver")
        self.price = input("Enter the money for the transfer")
        self.cause = input("Enter the motive of transfer")
        print("Committing and exiting..")

    def inquiry(self,i):


        print(self.Parameter['Stamp'][i])
        print("==========================================")
        print("Sender ==> Receiver:")
        print("\t"+self.Parameter['Agent'][i] + " ==> "+ self.Parameter['Payee'][i])
        print("==========================================")
        print("Cause Of Transfer: " +self.Parameter['Cause'][i])

        print("Price: "+str(self.Parameter['Price'][i]))
        print("==========================================")

    def inquiry_by_Agent(self):
        agent=input("Enter the Agent name to sort the data")
        for i in self.Parameter['Agent']:
            if i ==agent:
                ind=self.Parameter['Agent'].index(i)
                print("+++++++++++++++++  "+str(ind))
                self.inquiry(ind)
            else:
                print("Cannot Find the agent")
                exit(0)

def main():
    m=MoM()
    m.transfer()
if __name__ == '__main__':
    main()