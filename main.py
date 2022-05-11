class PlugLead(): 
    def __init__(self,mapping):
        self.mapping=mapping
    
    def __str__(self):
        return str(self.mapping)
        
    def encode(self,character):
        if character in self.mapping:
            position=(self.mapping.find(character))
            if position==0:
                return(self.mapping[1])
            else:
                return(self.mapping[0])
        else: return((character))
    


class Plugboard():
    def __init__(self):
        self.board=[] #create empty list 
        
    def __str__(self):
        return self.board
        
  
    def add(self,lead):
        self.board.append(lead.__str__()) #ensure the lead is a string and add it to the board 
        return(self.board)


    def encode(self,letter): 
        for pair in self.board:
            if letter in pair:
                position=pair.find(letter) 
                if position==0:
                    return(pair[1])
                else: return(pair[0])
        else: return(letter)
        
    def newalphabet(self): #create a new alphabet with all of the plugleads
        newalphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for pair in self.board:

            index1=newalphabet.index(pair[0])
            index2=newalphabet.index(pair[1])
            newalphabet=newalphabet[:index1]+pair[1]+newalphabet[index1+1:]
            newalphabet=newalphabet[:index2]+pair[0]+newalphabet[index2+1:]
        return(newalphabet)
                
        
class rotor_from_name():
    def __init__(self,name):    
        self.rotors={"Alpha":"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                     "Beta":"LEYJVCNIXWPBQMDRTAKZGFUHOS",
                     "Gamma":"FSOKANUERHMBTIYCWLQPZXVGJD",
                     "I":"EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                     "II":"AJDKSIRUXBLHWTMCQGZNPYFVOE",
                     "III":"BDFHJLCPRTXVZNYEIWGAKMUSQO",
                     "IV":"ESOVPZJAYQUIRHXLNFTGKDCMWB",
                     "V":"VZBRGITYUPSDNHLXAWMJQOFECK",
                     "A":"EJMZALYXVBWFCRQUONTSPIKHGD",
                     "B":"YRUHQSLDPXNGOKMIEBFZCWVJAT",
                     "C":"FVPJIAOYEDRZXWGCTKUQSBNMHL"}
        self.rotor=self.rotors.get(name)
        self.Alpha=self.rotors.get("Alpha")


    def encode_right_to_left(self,c):
        return self.rotor[self.Alpha.index(c)] #find the index value of the character in the alphabet and then find that in the rotor 

    def encode_left_to_right(self,c):
        return self.Alpha[self.rotor.index(c)] #find the index value of the character in the rotor and then find that in the alphabet

    

class enigma():
    def __init__(self,rotor,reflector,position,notch,ringsetting,letter):
        self.rotor=rotor
        self.reflector=reflector
        self.position=position
        self.notch=notch
        self.ringsetting=ringsetting
        self.letter=letter
    
    def offsetright(position,letter,ringsetting): #find the offset: add the position, minus the ringsetting 
        positionoffset=(ord(position)-65) 
        newposition=ord(letter)+positionoffset
        newletter=newposition-ringsetting+1 #add 1 as ring setting of 2 is the same as position of A
        if newletter<=64:
            newletter=newletter+26
        if newletter>=91:
            newletter=newletter-26
        output=chr(newletter)
        return(output)

    def offsetleft(position,output,ringsetting): #find the offset: add the ring setting, minus the position
        positionoffset=(ord(position)-65)
        output=ord(output)+ringsetting-1 #minus 1 as ring setting of 2 is the same as position of A
        output=output-positionoffset
        if output<=64:
            output=output+26
        if output>=91:
            output=output-26
        output=chr(output)
        return(output)

      
    def rotateright(self): #rotation: right most will also rotate, others only rotate if on the notch.
        if position[0]!=notch[0] and position[1]==notch[1] and position[2]==notch[2]:
            position[1]=chr(ord(position[1])+1)
            position[2]=chr(ord(position[2])+1)
        
        if len(self.position)==4:
            if self.position[2]==self.notch[2]:
                if self.position[3]=="Z":
                    self.position[3]="A"
                else:
                    self.position[3]=chr(ord(self.position[3])+1)
        
        if self.position[1]==self.notch[1]:
            if self.position[2]=="Z":
                self.position[2]="A"
            else:
                self.position[2]=chr(ord(self.position[2])+1)
    
        if self.position[0]==self.notch[0]:
            if self.position[1]=="Z":
                self.position[1]="A"
            else:
                self.position[1]=chr(ord(self.position[1])+1)
                
        if self.position[0]=="Z":
            self.position[0]="A"
        else:
            self.position[0]=chr(ord(self.position[0])+1)
        return(position)
    
    def rotateleft(position,notch): #opposite of rotate right. needed for code breaking.
        if len(position)==4:
            if position[2]==notch[2]:
                if position[3]=="A":
                    position[3]="Z"
                else:
                    position[3]=chr(ord(position[3])-1)
        
        if position[1]==notch[1]:
            if position[2]=="A":
                position[2]="Z"
            else:
                position[2]=chr(ord(position[2])-1)
    
        if position[0]==notch[0]:
            if position[1]=="A":
                position[1]="Z"
            else:
                position[1]=chr(ord(position[1])-1)
  
        if position[0]=="A":
            position[0]="Z"
        else:
            position[0]=chr(ord(position[0])-1)
        return(position)
              
    
    def machine(self):
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        plugboardalpha=plugboard.newalphabet() #using the plugboard alphabet
        letter1=plugboardalpha[alphabet.index(letter)] #finding the new letter taking into account the plugboard
        newposition=enigma.rotateright(self) #rotate right 
        output=enigma.offsetright(newposition[0],letter1,ringsetting[0]) #using the offset function for the right most rotor
        rotor1=rotor_from_name(rotor[0]) #find the first rotor 
        encode=rotor1.encode_right_to_left(output) #encode letter using first rotor 
        output=enigma.offsetleft(newposition[0],encode,ringsetting[0]) #using reverse offset function to get the output from the first rotor 
        
        #output from second rotor
        output=enigma.offsetright(newposition[1],output,ringsetting[1])
        rotor2=rotor_from_name(rotor[1])
        encode=rotor2.encode_right_to_left(output)
        output=enigma.offsetleft(newposition[1],encode,ringsetting[1])
        
        #output from third rotor
        output=enigma.offsetright(newposition[2],output,ringsetting[2])
        rotor3=rotor_from_name(rotor[2])
        encode=rotor3.encode_right_to_left(output)
        output=enigma.offsetleft(newposition[2],encode,ringsetting[2])
        
        #output from fourth rotor if there are four rotors
        if len(rotor)==4:
            output=enigma.offsetright(newposition[3],output,ringsetting[3])
            rotor4=rotor_from_name(rotor[3])
            encode=rotor4.encode_right_to_left(output)
            output=enigma.offsetleft(newposition[3],encode,ringsetting[3])
         
        #output from reflector
        reflector1=rotor_from_name(reflector)
        output=reflector1.encode_left_to_right(output)
        
        #reverse output from fourth rotor
        if len(rotor)==4:
            output=enigma.offsetright(newposition[3],output,ringsetting[3])
            encode=rotor4.encode_left_to_right(output)
            output=enigma.offsetleft(newposition[3],encode,ringsetting[3])
        
        #reverse output from thurd rotor
        output=enigma.offsetright(newposition[2],output,ringsetting[2])
        encode=rotor3.encode_left_to_right(output)
        output=enigma.offsetleft(newposition[2],encode,ringsetting[2])
        
        #reverse output from second rotor
        output=enigma.offsetright(newposition[1],output,ringsetting[1])
        encode=rotor2.encode_left_to_right(output)
        output=enigma.offsetleft(newposition[1],encode,ringsetting[1])
        
        #reverse output from first rotor
        output=enigma.offsetright(newposition[0],output,ringsetting[0])
        encode=rotor1.encode_left_to_right(output)
        output=enigma.offsetleft(newposition[0],encode,ringsetting[0])
        
        #find the letter taking into account the plugboard
        output=alphabet[plugboardalpha.index(output)]
        return(output)
