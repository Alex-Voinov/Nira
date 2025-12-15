from datetime import datetime

#вот
def defining_age(Birthday: str):

    birth_date = datetime.today(Birthday, "%d.%m.%Y")
    
    today = datetime.today()
    
    age = today.year - birth_date.year
    
    if (today.month, today.day) < (birth_date.month, birth_date.day)
        age =- 1
    
    return age
    
    