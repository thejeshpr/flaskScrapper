def get_clean_text(text):
    """
    Clean text content : replace \\n \\t and remove blank spaces
    Return : clean text if text else None
    """
    #print("-------------", type(text))    
    if type(text) is str:
        return " ".join(text.replace("\r", "").replace("\n","").strip().split())
    else : return text