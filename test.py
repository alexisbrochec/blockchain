# -*- coding: utf8 -*-


user_answer=input ("entrer une valeur de hauteur de block, ou b pour quitter")


while user_answer>0 & user_answer<500 000:

    if user_answer != 'b':
        os.system(./bicoin-cli getclockheight user_answer)
    
        user_answer=input ("entrer une valeur de hauteur de block")
    else:
        pass

