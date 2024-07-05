from flask import Flask, request, render_template, redirect, session
from mailer import Mailer
import random
import hashlib
import sqlite3
from datetime import date, datetime
daych = datetime.now().date()
import html
date_  = date.today()

app = Flask(__name__) 
app.secret_key = '666666666666666666666666666'



def pp():
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()
    mydb.execute('SELECT * FROM clasesReservation')
    clasess = mydb.fetchall()
    for s in clasess:
        target_date = datetime.strptime(s[9], '%Y-%m-%d').date()
        
        if  daych > target_date and s[1] != 'Online' and s[11] == 'True':
            db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
            mydb = db.cursor()
            mydb.execute(f"UPDATE clases SET date1 = '{'Free'}' WHERE ClassId = '{s[1]}'")
            db.commit()
            db.close()
        elif daych < target_date and s[1] != 'Online' and s[11] == 'True':
            db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
            mydb = db.cursor()
            mydb.execute(f"UPDATE clases SET date1 = '{'Busy'}' WHERE ClassId = '{s[1]}'")
            db.commit()
            db.close()

 
def encrippt(prs):

    p1e = hashlib.md5(prs.encode()).hexdigest()
    p1d1 = p1e.translate({ord('b'): None})
    p1d2 = p1d1.translate({ord('8'): None})
    p1 = p1d2[0:9]


    p2e = hashlib.sha1(prs.encode()).hexdigest()
    p2d1 = p2e.translate({ord('e'): None})
    p2d2 = p2d1.translate({ord('6'): None})
    p2 = p2d2[0:6]


    p3e = hashlib.sha256(prs.encode()).hexdigest()
    p3d1 = p3e.translate({ord('1'): None})
    p3d2 = p3d1.translate({ord('l'): None})
    p3 = p3d2[0:10]


    return str(p1)+str(p2)+str(p3)


@app.route('/', methods =["GET", "POST"])
def loginn():

    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()

    if request.method == "POST":
        user = html.escape(request.form.get("usr").lower())
        pwd  = html.escape(request.form.get("pwd"))
        if user == '' and pwd == 'PASSWORDADMIN':
            session['name'] = 'Admin'
            return redirect('/admin')
        mydb.execute(f"SELECT * FROM acounts WHERE  user = '{user}' AND password = '{encrippt(pwd)}'")
        dddd = mydb.fetchone()
        if dddd == None:
            return render_template("logins.html", mm = 'error email or password')
        else:
            if dddd[5] == 'True':
                session['name'] = dddd[3]
                session['email'] = dddd[1]
                session['type'] = dddd[4]

                if dddd[6] == 'False':
                    session['type'] = 'Student'
                    session['email'] = dddd[1]
                    session['phone'] = dddd[7]
                elif dddd[6] == 'True':
                    session['email'] = dddd[1]
                    session['type'] = dddd[4]
                    

                return redirect('/home')
            else:
                session['email'] = user
                return redirect('/veres')
    
    return render_template("logins.html")


@app.route('/signup', methods =["GET", "POST"])
def signup():
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()
    if request.method == "POST":

        user = html.escape(request.form.get("nusr").lower())
        npwd  = html.escape(request.form.get("npwd"))
        Fullnamm = html.escape(request.form.get("hname"))
        Type = html.escape(request.form.get("type"))
        phone = html.escape(request.form.get("phone"))

        data11 = html.escape(request.form.get("data11"))
        data22 = html.escape(request.form.get("data22"))
        data33 = html.escape(request.form.get("data33"))
        exper = data11 +' '+data22+' '+data33
        if exper == 'None':
            exper = 'Student'

        
        
        # checker  
        mydb.execute("SELECT user FROM acounts")
        results = mydb.fetchall()
        if (user,) in results:
            return redirect('/')

        session['email'] = user
        session['vrcode'] = random.randint(100011,900019)
        vrcode_ = session.get('vrcode')



        mzil = Mailer(email="r2securtylogin@gmail.com", password="vbfbqxyavrmfrghy")
        mzil.send(receiver=user,
                subject="THIS IS EMAIL FOR VIRTCLY",
                message=" your vayrtcly code is ("+str(vrcode_ )+")" )


        
   
        db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
        mydb = db.cursor()
        mydb.execute(f"INSERT INTO acounts ( user, password, fullName, Type, PhoneNumber, data1, verificationAdmin, data3  )  VALUES ('{user}','{encrippt(npwd)}','{Fullnamm}','{Type}', '{phone}', '{date_}', '{'False'}','{exper}')")
        db.commit()
        db.close()

        return redirect('/veres')
        

    return render_template("signup.html")


@app.route('/veres', methods =["GET", "POST"])
def verecode():
    if session.get('email') == None:
        return redirect('/')
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()


    if request.method == "POST":
        vrcode__ = request.form.get('verc')

        if str(vrcode__) == str(session.get('vrcode')):
            user__ = str(session.get('email'))
            mydb.execute("UPDATE acounts SET verificationCode = ? WHERE user = ?", ('True', user__))
            db.commit()
            db.close()
            return redirect('/')
        else:
            massgeErorr_ = 'the code is not correct'
            return render_template('vere.html', massgeErorr = massgeErorr_, emailhis = str(session.get('email')) )


    return render_template('vere.html', emailhis = str(session.get('email')) )


@app.route('/addclass', methods =["GET", "POST"])
def addclass():
    if session.get('email') == None:
        return redirect('/')
    pp()
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()
    if request.method == "POST":
        cource = html.escape(request.form.get("cource")) 
        Room  = html.escape(request.form.get("Room"))
        teacher = html.escape(request.form.get("teacher", "")) or ''
        TimeStart = html.escape(request.form.get("TimeStart"))
        TimeEnd = html.escape(request.form.get("TimeEnd"))
        introduction = html.escape(request.form.get("introduction"))
        Date__ = html.escape(request.form.get("Date"))
        # ClassData


        # DrData
        if session.get('type') == 'Teacher':
            usser = session.get('name')
            mydb.execute('SELECT * FROM acounts WHERE fullName=?', (session.get('name'),))
            usss = mydb.fetchone()
            Dr_Name = usss[3]
        elif session.get('type') == 'Student':
            usser = session.get('name')
            mydb.execute('SELECT * FROM acounts WHERE fullName=?', (teacher,))
            usss = mydb.fetchone()
            Dr_Name = html.escape(usss[3])

        if Room == 'Online':
            ooo = 'Online'
            
            mydb.execute(f"INSERT INTO clasesReservation (ClassId, BildId, floorId, TImeReservationStert, TImeReservationEnd, UserName, data1, data2, confirmation, data3, data4, sname,TeacherAcsept) VALUES ('{ooo}', '{'None'}', '{'None'}', '{TimeStart}', '{TimeEnd}', '{str(Dr_Name)}', '{cource}', '{introduction}', '{'False'}','{Date__}', '{session.get('type')}', '{session.get('name')}', '{'False'}')")
            db.commit()
            db.close()
            return redirect('/home')
        else:
            mydb.execute(f'SELECT * FROM clases WHERE ClassId={Room}')                                                                                      
            ClassData = mydb.fetchone()
            Classid = ClassData[1]
            Classbild = ClassData[2]
            Classflour = ClassData[3]
            mydb.execute(f"INSERT INTO clasesReservation (ClassId, BildId, floorId, TImeReservationStert, TImeReservationEnd, UserName, data1, data2, confirmation, data3 , data4, sname,TeacherAcsept) VALUES ('{Classid}', '{Classbild}', '{Classflour}', '{TimeStart}', '{TimeEnd}', '{str(Dr_Name)}', '{cource}', '{introduction}', '{'False'}','{Date__}', '{session.get('type')}', '{session.get('name')}', '{'False'}')")        
            db.commit()
            db.close()
            return redirect('/home')
    return redirect('/home')


@app.route('/home', methods =["GET", "POST"])
def home():
    pp()
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()
    mydb.execute('SELECT * FROM clases')
    clasess = mydb.fetchall()
    clasesel = clasess
    mydb.execute('SELECT * FROM acounts WHERE verificationAdmin=?', ('True',))
    teacherr = mydb.fetchall()
    mydb.execute(f"SELECT * FROM record")
    reclass = mydb.fetchall()
    mydb.execute('SELECT * FROM clasesReservation WHERE confirmation=?', ('True',))
    clasesss = mydb.fetchall()
    mydb.execute('SELECT * FROM clasesReservation WHERE sname=?', (session.get('name'),))
    clasesReservation11 = mydb.fetchall()


    mydb.execute(f"SELECT * FROM clasesReservation WHERE   UserName='{session.get('name')}' AND data4='{'Student'}' AND TeacherAcsept='{'False'}' AND confirmation='{'False'}'")
    Studord = mydb.fetchall()
    
    if session.get('email') == None:
        return redirect('/')
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()

    return render_template('index.html', order=clasesReservation11, type = session.get('type'), clasesr = clasesss, clasesel =clasesel, Teacher= teacherr, reclass=reclass, name = session.get('name'), email=session.get('email'), phone=session.get('phone'),Studord=Studord )

@app.route('/deletec', methods =["GET", "POST"])
def delec():
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()
    if request.method == "POST":
        id_del = request.form.get('val')
        mydb.execute(f"DELETE FROM clasesReservation WHERE ii = {id_del}")
        db.commit()
        db.close()

    return redirect('/home')





@app.route('/admin', methods =["GET", "POST"])
def adminjob():
    if session.get('name') != 'Admin':
        session.clear()
        return redirect('/')
    pp()
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()
    mydb.execute('SELECT * FROM clases')
    clasess = mydb.fetchall()
    clasesel = clasess
    mydb.execute('SELECT * FROM acounts WHERE verificationAdmin=?', ('True',))
    teacherr = mydb.fetchall()
    mydb.execute(f"SELECT * FROM record")
    reclass = mydb.fetchall()
    mydb.execute('SELECT * FROM clasesReservation WHERE confirmation=?', ('True',))
    clasesss = mydb.fetchall()

    #teachers
    mydb.execute(f"SELECT * FROM acounts WHERE verificationCode='{'True'}' AND Type='{'Teacher'}' AND verificationAdmin='{'False'}' ")
    teachers = mydb.fetchall()
    

    #clases order by teachers
    mydb.execute(f"SELECT * FROM clasesReservation WHERE data4='{'Teacher'}' AND confirmation='{'False'}' ")
    clases_NotConf_T = mydb.fetchall()
    

    #clases order by Students
    mydb.execute(f"SELECT * FROM clasesReservation WHERE data4='{'Student'}' AND confirmation='{'False'}' AND TeacherAcsept='{'True'}'")
    clases_NotConf_S = mydb.fetchall()


    
    if request.method == "POST":
        what = html.escape(request.form.get("what") or '')
        nameb = html.escape(request.form.get('acs') or '')
        emailt = html.escape(request.form.get("email") or '')
        classa = html.escape(request.form.get("class") or '')
        corsea = html.escape(request.form.get("corse") or '')
        namet = html.escape(request.form.get("name") or '')
        phonet = html.escape(request.form.get("phone") or '')
        

        corseName = html.escape(request.form.get("corseName") or '')
        Urlname = html.escape(request.form.get("Urlname") or '')
        Intrud = html.escape(request.form.get("Intrud") or '')
        Teacher = html.escape(request.form.get("Teacher") or '')
        


        ClassId = html.escape(request.form.get("ClassId") or '')
        building = html.escape(request.form.get("building") or '')
        Flour = html.escape(request.form.get("Flour") or '')
        if what == 'Teaching requests':

            if nameb == 'Accept':
                mydb.execute(f"UPDATE acounts SET verificationAdmin = '{'True'}' WHERE user = '{emailt}' AND fullName='{namet}' AND PhoneNumber='{phonet}'")
                db.commit()
                db.close()
                mzil = Mailer(email="", password="")
                mzil.send(receiver=emailt,
                        subject="Teaching-requests",
                        message="Accepted by the admin!" )
                return redirect('/admin')
            if nameb == 'reject':
                mydb.execute(f"DELETE FROM acounts WHERE user = '{emailt}' AND fullName='{namet}' AND PhoneNumber='{phonet}'")
                db.commit()
                db.close()
                mzil = Mailer(email="", password="")
                mzil.send(receiver=emailt,
                        subject="Teaching-requests",
                        message="Rejected by the admin!" )
                return redirect('/admin')

        elif what == 'request for a totring lesson (by the Teachers)':
            mydb.execute(f"SELECT * FROM clasesReservation WHERE UserName = '{namet}' AND ClassId='{classa}' AND data1='{corsea}' AND data4='{'Teacher'}'")
            a1 = mydb.fetchone()
            accff = a1[12]
            mydb.execute(f"SELECT * FROM acounts WHERE fullName='{accff}'")
            ddff = mydb.fetchone()
            emailttte = ddff[1]
            if nameb == 'Accept':
                mydb.execute(f"UPDATE clasesReservation SET confirmation = '{'True'}' WHERE UserName = '{namet}' AND ClassId='{classa}' AND data1='{corsea}' AND data4='{'Teacher'}'")
                db.commit()
                db.close()
                mzil = Mailer(email="", password="")
                mzil.send(receiver=emailttte,
                        subject="your Tutor Class",
                        message="Accepted by the admin!" )
                return redirect('/admin')
            if nameb == 'reject':
                mydb.execute(f"DELETE FROM clasesReservation WHERE UserName = '{namet}' AND ClassId='{classa}' AND data1='{corsea}' AND data4='{'Teacher'}'") 
                db.commit()
                db.close()
                mzil = Mailer(email="", password="")
                mzil.send(receiver=emailttte,
                        subject="your Tutor Class",
                        message="Rejected by the admin!" )
                return redirect('/admin')
            
        elif what == 'request for a totring lesson (by the student)':
            mydb.execute(f"SELECT * FROM clasesReservation WHERE UserName = '{namet}' AND ClassId='{classa}' AND data2='{corsea}' AND data4='{'Student'}'")
            a1 = mydb.fetchone()
            accff = a1[12]
            mydb.execute(f"SELECT * FROM acounts WHERE fullName='{accff}'")
            ddff = mydb.fetchone()
            emailttt = ddff[1]
            if nameb == 'Accept':
                mydb.execute(f"UPDATE clasesReservation SET confirmation = '{'True'}' WHERE UserName = '{namet}' AND ClassId='{classa}' AND data2='{corsea}' AND data4='{'Student'}'")
                db.commit()
                db.close()
                mzil = Mailer(email="", password="")
                mzil.send(receiver=emailttt,
                        subject="your Tutor Class",
                        message=" your Tutor Class Accepted by the admin!" )
                return redirect('/admin')
            if nameb == 'reject':
                mydb.execute(f"DELETE FROM clasesReservation WHERE UserName = '{namet}' AND ClassId='{classa}' AND data2='{corsea}' AND data4='{'Student'}'")
                db.commit()
                db.close()
                mzil = Mailer(email="", password="")
                mzil.send(receiver=emailttt,
                        subject="your Tutor Class",
                        message=" your Tutor Class Rejected by the admin!" )
                return redirect('/admin')

        elif what == 'OnlineCorseAdd':
            mydb.execute(f"INSERT INTO record (course, url, data1, teach) VALUES ('{corseName}', '{Urlname}', '{Intrud}', '{Teacher}')")
            db.commit()
            db.close()
            return redirect('/admin')
        elif what == 'Add a class':
            mydb.execute(f"INSERT INTO clases (ClassId, BildId, floorId, date1) VALUES ('{ClassId}', '{building}', '{Flour}', '{'Free'}')")
            db.commit()
            db.close()
            return redirect('/admin')
            
    return render_template('admin.html', teachers=teachers,clasesr = clasesss, clasesel =clasesel, Teacher= teacherr, clases_NotConf_T=clases_NotConf_T, clases_NotConf_S=clases_NotConf_S, reclass=reclass )


@app.route('/Tacsept', methods =["GET", "POST"])
def teacsept():
    if session.get('email') == None:
        return redirect('/')
    db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
    mydb = db.cursor()
    if request.method == "POST":
        usn = html.escape(request.form.get('usn'))
        ent = html.escape(request.form.get('ent'))
        abu = html.escape(request.form.get('abu'))
        btn = html.escape(request.form.get('btn'))
        db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
        mydb = db.cursor()
        mydb.execute(f"SELECT * FROM clasesReservation WHERE sname='{usn}' AND TImeReservationEnd='{ent}' AND data2='{abu}' AND data4='{'Student'}'")
        emails = mydb.fetchone()
        acc = emails[12]
        mydb.execute(f"SELECT * FROM acounts WHERE fullName='{acc}'")
        emailsh = mydb.fetchone()
        if btn == 'acs':
            mydb.execute(f"UPDATE clasesReservation SET TeacherAcsept = '{'True'}' WHERE sname='{usn}' AND TImeReservationEnd='{ent}' AND data2='{abu}' AND data4='{'Student'}'")    
            db.commit()
            db.close()
            mzil = Mailer(email="", password="")
            mzil.send(receiver=emailsh[1],
                    subject="your Tutor Class",
                    message=" your Tutor Class Acsepted! By Teacher" )
            return redirect('/home')
        elif btn == 'rej':
            db = sqlite3.connect("/home/Uhbtutoring/mysite/Totringdb.db")
            mydb = db.cursor()
            mydb.execute(f"DELETE FROM clasesReservation WHERE TeacherAcsept = '{'False'}' AND sname='{usn}' AND TImeReservationEnd='{ent}' AND data2='{abu}' AND data4='{'Student'}'") 
            db.commit()
            db.close()
            mzil = Mailer(email="", password="")
            mzil.send(receiver=emailsh[1],
                    subject="your Tutor Class",
                    message=" your Tutor Class rejected! By Teacher" )
            return redirect('/home')
    return redirect('/home')


@app.route('/Logout', methods =["GET", "POST"])
def sss():
    session.clear()
    return redirect('/')

if __name__=='__main__':    
   app.run(debug=True)