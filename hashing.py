for i in range(1000000):

def md5test():
  x = hashlib.md5(b"florida")

  for i in range(1000000):
    x = md5test()


from passlib.hash import bcrypt


# put this in on registration before sending to the data base.
encrpass = bcrypt.hash("variable for a password goes here")

if bcrypt.verify("attemp at log in", encrpass):
    print("yay"):
else :
    print ("aw man")

# go to DB find user that matches email
# check if pass word is same as stored passlib
#

# Authenticate
# input email, password
1. find user in DB by email
    if found:
        2. compare given pw to hashed pw
            if matches:
                :) remember state
                if
            else:
                error message (401)

    else
        error message(401)




# \replicate create for a MyRequestHandler
create new div
