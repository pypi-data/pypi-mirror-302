from time import sleep
from os import system

# INPUTRON I
# It's a Library that help in control and manage of Inputs and Outputs Terminals

# Starting Instancing
# inputron = Inputron()

class Inputron:

    # function that manage message in terminal
    def Message(self, msg:str, about:str = "", space:bool = False, iserror:bool = False):
        
        """Create better outputs messages, alerts with this function. 
        
        Arguments:
            msg {String} Set your message here
            about {String} The Message Title [Optional]
            space {Boolean} If has space or not [Optional] default=False
            iserror {Boolean} If the message is to sinalize a error or not [Optional] default=False
        """
        
        if space:
            print()

        if not about == "":
            print(f'{about} Warn - {msg}') if iserror is False else print(f'{about} Error - {msg}')
        else:
            print(f'Warn - {msg}') if iserror is False else print(f'Error - {msg}')

        if space:
            print()

    # function that show visual loading
    def Loading(self, msg: str = "LOADING", msgComplete: str = "COMPLETE", speed: float = 0.1, repeatTimes: int = 10, icon: list = ["|", "/", "-", "\\"]):
        
        """Create a loader in format of terminal, manage and the Icon
        
        Arguments:
            msg {String} Set here your text to show while is loading [Optional] default="LOADING"
            msgComplete {String} It is message that will be shown [Optional] default="COMPLETE"
            speed {Float} It is interval in each rotated [Optional] default=0.1
            repeatTime {Integer} It is amount of time that the icon spins [Optional] default=10
            icon {List} It is the icon strings, change to other if you want [Optional] default=["|", "/", "-", "\\"]
        """
        
        bars = icon
        
        for _ in range(repeatTimes):
            for i in range(len(bars)): 
                sleep(speed)   
                system('cls')    
                print(f'{bars[i]} > {msg}')
        
        sleep(speed)
        system('cls')
        print(msgComplete)
                
    # function that control asks in terminal
    def AskCustommer(self, ask:str, space:bool = True, isInt:bool = False, isFloat:bool = False):
        
        """Use this function to ask some information of user

        Arguments:
            ask {String} It is your ask 
            space {Boolean} If your asks will have spaces on top of below [Optional] default=True
            isInt {Boolean} If you want that be returned in Integer format [Optional] default=False
            isFloat {Boolean} if you want that be returned in Floating format [Optional] default=False

        """
        
        
        try:
        
            if space is True:
                print()

            askInp = input(f'    > {ask}: ')
            
            if not askInp == '':
                if isInt is True:
                    return int(askInp)
                
                if isFloat is True:
                    return float(askInp)
                
                if space is True:
                    print()
                    
                return askInp
            
            self.Message('It is empty, not accepted', 'Inputron', iserror=True)
            return None
            
        except Exception as err:
            inputron.Message(err, 'Nogra', True, True)
            
    # function to options Y|N
    def YN(self, ask:str, title:str = 'Question', space:bool = True, optionCorrect:str = "yes", optionIncorrect:str = "no"):
        
        """Use this function to obtain two answer, Yes or No, you can change the options.

        Arguments:
            ask {String} It is your question.
            title {String} It is the title of question [Optional] default="Question"
            space {Boolean} If your asks will have spaces on top or below [Optional] default=True
            optionCorrect {String} It is the text option correct [Optional] default="yes"
            optionIncorrect {String} It is the text option incorrect [Optional] default="no"

        Raises:
            ValueError: If the answer obtained not is Yes or No.

        Returns:
            Boolean: True to Yes and False to No 
        """
        
        
        if space:
            print()
            

        print(f'{title} - {ask}')
        question = input(f'[{optionCorrect[0].upper()}]{optionCorrect[1::]} or [{optionIncorrect[0].upper()}]{optionIncorrect[1::]} : ')

        if question.lower() == optionCorrect[0]:
            return True
        elif question.lower() == optionIncorrect[0]:
            return False 
        else:
            raise ValueError('Answernot Recognized')
        
        
        
        if space:
            print()
          
    # function to calc Average  
    def AVG(self, content:list, binsCalc:int = 4, isInt:bool = False, isFloat:bool = True, isStr:bool = False):
        
        """Use this function to calc Average of numbers to Grade

        Arguments:
            content {List} This is the list of numbers that will be used to calc
            binsCalc {Integer} It is the divider of calc [Optional] default=4
            isInt {Boolean} If the return is in integer format [Optional] default=False
            isFloat {Boolean} If the return is in floating format [Optional] default=True
            isStr {Boolean} If the return is in string format [Optional] default=False 
            
        """
        
        
        try:
            totalContents = sum(content)
            average = totalContents / binsCalc
            
            if isInt:
                return int(average)
            
            if isFloat:
                if isStr:
                    return f'{float(average):.1f}'
                return float(average)
            
            if isStr:
                return str(average) 
                 
        except Exception as err:
            self.Message(f'.~. {err}', 'Inputron', iserror=True)