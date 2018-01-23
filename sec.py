def check_password(s,k):
    if k==0: # email
        a = "!#$%^&*()'-,/\+=~"
    else: # password
        a = "!#$%^&*()'-.@,/\+=~"

    for i in a:
        for j in s:
            if i == j:
                return False
    return True

def check_null(s):
    if s == "":
        return False
    return True
