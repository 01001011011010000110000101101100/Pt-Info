from constants import MEDICAL_ABBREVIATIONS


def clear_shortcut_inputs(text: str) -> str: 
    try :
        words = text.strip().split()

        if len(words) > 1: # If the nurse enter more than one word that means he did not enter an abbreviation. Thus, return the text as will as it was entered 
            return " ".join([w.title() for w in words])  
        
        cleaned_word = []
        word = words[0]

        symbols =  [',', '.', '/', '(', ')', ';', '=', '!', '@', '#', '$', '%', '^', '&', '*', '_', '-', '\\']
        pure_word = "".join([char for char in word if char not in symbols])

        if pure_word.lower() in MEDICAL_ABBREVIATIONS :
            cleaned_word.append("".join([w.upper() for w in pure_word]))
            
        else :
            cleaned_word.append("".join(pure_word))

        return "".join(cleaned_word)
    except Exception as er :
        return