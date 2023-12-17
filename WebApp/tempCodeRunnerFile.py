@app.route("/Login/<Username>/<password>")
# def Login(Username,password):
#     user = User.query.filter_by(username=Username).first()
#     if user:
#         #print(user[1],user[2],user[3])
#         print(user.id)
#         if check_password_hash(user.password,password):
#             login_user(user,False)
#             notify.send("LoginSuccessfully")
#             return jsonify({"message":True,"Username":user.username,"Userid":user.id})

#     return jsonify({"message":"False"})