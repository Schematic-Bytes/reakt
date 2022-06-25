import pymysql
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

# Create your views here.
db = pymysql.connect(
    host="localhost",
    user="root",
    port=3309,
    password="",
    database="sandbox",
)
c = db.cursor()


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        email = request.POST["name"]
        password = request.POST["password"]
        s = f"select count(*) from login where uname='{email}'"
        c.execute(s)
        i = c.fetchone()
        if i[0] > 0:
            s = f"select * from login where uname='{email}'"
            c.execute(s)
            i = c.fetchone()
            if i[3] == password:
                request.session["email"] = email
                if i[5] == "Active":
                    if i[4] == "admin":
                        return redirect("/adminHome")
                    elif i[4] == "investor":
                        s = f"select * from investors where inemail='{email}'"
                        c.execute(s)
                        d = c.fetchone()
                        request.session["id"] = d[0]
                        return redirect("/inHome")
                    elif i[4] == "startup":
                        s = f"select * from startpfounder where sfemail='{email}'"
                        c.execute(s)
                        d = c.fetchone()
                        request.session["id"] = d[0]
                        return redirect("/sfHome")
                else:
                    msg = "Account is not Active..."
                    return render(request, "login.html", {"msg": msg})
            else:
                msg = "Password Dosent Match..."
                return render(request, "login.html", {"msg": msg})
        else:
            msg = "User Dosent Exists..."
            return render(request, "login.html", {"msg": msg})
    else:
        return render(request, "login.html")


def inReg(request):
    flag = 0
    msg = ""
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        pin = request.POST["pin"]
        img = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        check = f"SELECT COUNT(*) FROM `login` WHERE `uname`='{email}'"
        c.execute(check)
        check = c.fetchone()
        check = check[0]
        if check == 0:
            qry = f"INSERT INTO `investors` (`inname`,`inaddress`,`inphone`,`inemail`,`indocument`,`pin`) VALUES ('{name}','{address}','{phone}','{email}','{uploaded_file_url}','{pin}')"
            c.execute(qry)
            db.commit()
            qryLog = f"INSERT INTO `login`(`uid`,`uname`,`password`,`utype`,`status`) VALUES ((SELECT MAX(`invid`) FROM `investors`),'{email}','{password}','investor','Inactive')"
            c.execute(qryLog)
            db.commit()
            msg = "Registration Successful..."
            flag = 1
        else:
            msg = "Email already exists..."

    return render(request, "inReg.html", {"msg": msg, "flag": flag})


def sfReg(request):
    flag = 0
    msg = ""
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        pin = request.POST["pin"]
        img = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        check = f"SELECT COUNT(*) FROM `login` WHERE `uname`='{email}'"
        c.execute(check)
        check = c.fetchone()
        check = check[0]
        if check == 0:
            qry = f"INSERT INTO `startpfounder` (`sfname`,`sfaddress`,`sfphone`,`sfemail`,`sfdocument`,`pin`) VALUES ('{name}','{address}','{phone}','{email}','{uploaded_file_url}','{pin}')"
            c.execute(qry)
            db.commit()
            qryLog = f"INSERT INTO `login`(`uid`,`uname`,`password`,`utype`,`status`) VALUES ((SELECT MAX(`sfid`) FROM `startpfounder`),'{email}','{password}','startup','Active')"
            c.execute(qryLog)
            db.commit()
            msg = "Registration Successful..."
            flag = 1
        else:
            msg = "Email already exists..."

    return render(request, "sfReg.html", {"msg": msg, "flag": flag})


def adminHome(request):
    return render(request, "adminHome.html")


def adminInvestor(request):
    qry = "SELECT * FROM `investors` i, `login` l WHERE i.`inemail`=l.`uname` AND l.`status`='Inactive'"
    c.execute(qry)
    data = c.fetchall()
    qry = "SELECT * FROM `investors` i, `login` l WHERE i.`inemail`=l.`uname` AND l.`status`='Active'"
    c.execute(qry)
    dataActive = c.fetchall()
    qry = "SELECT * FROM `investors` i, `login` l WHERE i.`inemail`=l.`uname` AND l.`status`='Rejected'"
    c.execute(qry)
    dataInactive = c.fetchall()
    return render(
        request,
        "adminInvestor.html",
        {"data": data, "dataActive": dataActive, "dataInactive": dataInactive},
    )


def approveInvestors(request):
    id = request.GET["id"]
    status = request.GET["status"]
    qry = f"UPDATE `login` SET `status`='{status}' WHERE `logid`='{id}'"
    c.execute(qry)
    db.commit()
    return redirect("/adminInvestor")


def adminStartUp(request):
    qry = "SELECT * FROM `startpfounder` s, `login` l WHERE s.`sfemail`=l.`uname` AND l.`status`='Inactive'"
    c.execute(qry)
    data = c.fetchall()
    qry = "SELECT * FROM `startpfounder` s, `login` l WHERE s.`sfemail`=l.`uname` AND l.`status`='Active'"
    c.execute(qry)
    dataActive = c.fetchall()
    qry = "SELECT * FROM `startpfounder` s, `login` l WHERE s.`sfemail`=l.`uname` AND l.`status`='Rejected'"
    c.execute(qry)
    dataInactive = c.fetchall()
    return render(
        request,
        "adminStartup.html",
        {"data": data, "dataActive": dataActive, "dataInactive": dataInactive},
    )


def approveStartUp(request):
    id = request.GET["id"]
    status = request.GET["status"]
    qry = f"UPDATE `login` SET `status`='{status}' WHERE `logid`='{id}'"
    c.execute(qry)
    db.commit()
    return redirect("/adminStartUp")


def adminViewFeedback(request):
    qry = "SELECT * FROM `feedback` f, `startpfounder` s WHERE f.`sfid`=s.`sfid`"
    c.execute(qry)
    data = c.fetchall()
    return render(request, "adminViewFeedback.html", {"data": data})


def inHome(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `investors` WHERE `invid`='{id}'"
    c.execute(qry)
    data = c.fetchone()
    pin = data[6]
    qryPost = f"SELECT * FROM `idea` i, `startpfounder` sf WHERE i.`sfid`=sf.`sfid` AND sf.`pin`='{pin}' ORDER BY i.`ideaid` DESC"
    c.execute(qryPost)
    post = c.fetchall()
    if request.method == "POST":
        search = request.POST["search"]
        qrySer = f"SELECT * FROM `idea` i, `startpfounder` sf WHERE i.`sfid`=sf.`sfid` AND sf.`pin`='{pin}' AND (i.`idea` LIKE '%{search}%' OR i.`desc` LIKE '%{search}%') ORDER BY i.`ideaid` DESC"
        c.execute(qrySer)
        post = c.fetchall()
    return render(request, "inHome.html", {"data": data, "post": post})


def inProfile(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `investors` i, `login` l WHERE i.`invid`='{id}' AND i.`invid`=l.`uid` AND l.`utype`='investor'"
    c.execute(qry)
    data = c.fetchone()
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        qryProUp = f"UPDATE `investors` SET `inname`='{name}', `inaddress`='{address}', `inphone`='{phone}', `inemail`='{email}' WHERE `invid`='{id}'"
        c.execute(qryProUp)
        db.commit()
        qryLogUp = f"UPDATE `login` SET `password`='{password}' WHERE `uid`='{id}' AND `utype`='investor'"
        c.execute(qryLogUp)
        db.commit()
        return redirect("/inHome")
    return render(request, "inProfile.html", {"data": data})


def inViewIdea(request):
    id = request.GET["post"]
    qry = f"SELECT * FROM `idea` i, `startpfounder` sf WHERE `ideaid`='{id}' AND i.`sfid`=sf.`sfid`"
    c.execute(qry)
    data = c.fetchone()
    qryViewCom = f"SELECT * FROM `comments`c, `startpfounder` s WHERE c.`ideaid`='{id}' AND c.`sfid`=s.`sfid` ORDER BY c.`comid` DESC"
    c.execute(qryViewCom)
    comments = c.fetchall()
    interest = c.fetchone()
    return render(
        request,
        "inViewIdea.html",
        {"data": data, "comments": comments, "interest": interest},
    )


def inViewSf(request):
    id = request.GET["sfid"]
    qry = f"SELECT * FROM `startpfounder`WHERE `sfid`='{id}'"
    c.execute(qry)
    user = c.fetchone()
    qryPost = f"SELECT * FROM `idea` WHERE `sfid`={id}"
    c.execute(qryPost)
    post = c.fetchall()
    return render(request, "inViewSf.html", {"user": user, "post": post})


def inChangeImage(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `investors` WHERE `invid`='{id}'"
    c.execute(qry)
    data = c.fetchone()
    if request.method == "POST":
        img = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        qryUp = f"UPDATE `investors` SET `indocument`='{uploaded_file_url}' WHERE `invid`='{id}'"
        c.execute(qryUp)
        db.commit()
        return redirect("/inHome")
    return render(request, "inChangeImage.html", {"data": data})


def inViewInvestmentOffers(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `investmentinterest` ii, `idea` i, `startpfounder`s WHERE ii.`invid`='{id}' AND ii.`ideaid`=i.`ideaid` AND i.`sfid`=s.`sfid`"
    c.execute(qry)
    data = c.fetchall()
    return render(request, "inViewInvestmentOffers.html", {"data": data})


def inChat(request):
    sender = request.session["email"]
    receiver = request.GET["email"]
    if request.method == "POST":
        msg = request.POST["msg"]
        qry = f"INSERT INTO `chat` (`sender`,`receiver`,`message`,`date`) VALUES('{sender}','{receiver}','{msg}',(select sysdate()))"
        c.execute(qry)
        db.commit()
    qryChat = f"SELECT * FROM chat WHERE sender='{sender}' AND receiver='{receiver}' UNION SELECT * FROM chat WHERE receiver='{sender}' AND sender='{receiver}' ORDER BY `chatid`"
    c.execute(qryChat)
    messages = c.fetchall()
    return render(request, "inChat.html", {"messages": messages, "user": sender})


def inMakePayment(request):
    id = request.session["id"]
    sfid = request.GET["sfid"]
    if request.method == "POST":
        amt = request.POST["amt"]
        qry = f"INSERT INTO `payment` (`sfid`,`invid`,`amount`,`date`) VALUES ('{sfid}','{id}','{amt}',(SELECT SYSDATE()))"
        c.execute(qry)
        db.commit()
        return redirect("/inViewPayments")
    return render(request, "payment.html")


def inViewPayments(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `payment` p, `startpfounder` s WHERE p.`invid`='{id}' AND p.`sfid`=s.`sfid`"
    c.execute(qry)
    data = c.fetchall()
    return render(request, "inViewPayments.html", {"data": data})


def sfHome(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `startpfounder` WHERE `sfid`='{id}'"
    c.execute(qry)
    data = c.fetchone()
    qryPost = "SELECT * FROM `idea` i, `startpfounder` sf WHERE i.`sfid`=sf.`sfid` ORDER BY i.`ideaid` DESC"
    c.execute(qryPost)
    post = c.fetchall()
    if request.method == "POST":
        search = request.POST["search"]
        qrySer = f"SELECT * FROM `idea` i, `startpfounder` sf WHERE i.`sfid`=sf.`sfid` AND (i.`idea` LIKE '%{search}%' OR i.`desc` LIKE '%{search}%') ORDER BY i.`ideaid` DESC"
        c.execute(qrySer)
        post = c.fetchall()
    return render(request, "sfHome.html", {"data": data, "post": post})


def sftrending(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `startpfounder` WHERE `sfid`='{id}'"
    c.execute(qry)
    data = c.fetchone()
    qry = "select ideaid,count(ideaid) as vote from tbllike where postaction='like' group by ideaid order by vote desc limit 5"
    c.execute(qry)
    pst = c.fetchall()
    post = []

    for i in pst:
        ideaid = i[0]
        qryPost = f"SELECT * FROM `idea` i, `startpfounder` sf WHERE i.`sfid`=sf.`sfid` AND i.ideaid='{ideaid}'"
        c.execute(qryPost)
        p = c.fetchall()
        post.extend(p)

    return render(request, "sfHome.html", {"data": data, "post": post})


def sfProfile(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `startpfounder`sf, `login` l WHERE sf.`sfid`='{id}' AND l.`uid`='{id}' AND l.`utype`='startup' "
    c.execute(qry)
    data = c.fetchone()
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        qryProUp = (
            f"UPDATE `startpfounder` SET `sfname`='{name}', `sfemail`='{email}', "
            f"`sfphone`='{phone}', `sfaddress`='{address}' WHERE `sfid`='{id}'"
        )
        c.execute(qryProUp)
        db.commit()
        qryLogUp = f"UPDATE `login` SET `password`='{password}' WHERE `uid`='{id}' AND `utype`='startup'"
        c.execute(qryLogUp)
        db.commit()
        return redirect("/sfHome")
    return render(request, "sfProfile.html", {"data": data})


def sfChangeImage(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `startpfounder` WHERE `sfid`='{id}'"
    c.execute(qry)
    data = c.fetchone()
    if request.method == "POST":
        img = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        qryUp = f"UPDATE `startpfounder` SET `sfdocument`='{uploaded_file_url}' WHERE `sfid`='{id}'"
        c.execute(qryUp)
        db.commit()
        return redirect("/sfHome")
    return render(request, "sfChangeImage.html", {"data": data})


def sfPost(request):
    id = request.session["id"]
    if request.method == "POST":
        idea = request.POST["idea"]
        description = request.POST["description"]
        qry = (
            "INSERT INTO `idea`(`sfid`,`idea`,`desc`,`date`) VALUES "
            f"('{id}','{idea}','{description}',(select sysdate()))"
        )
        c.execute(qry)
        db.commit()
    return render(request, "sfPost.html")


def sfViewSelfPost(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `idea` WHERE `sfid`='{id}'"
    c.execute(qry)
    data = c.fetchall()
    return render(request, "sfViewSelfPost.html", {"data": data})


def sfUpdateIdea(request):
    id = request.GET["id"]
    qry = f"SELECT * FROM `idea` WHERE `ideaid`='{id}'"
    c.execute(qry)
    data = c.fetchone()
    if request.method == "POST":
        idea = request.POST["idea"]
        description = request.POST["description"]
        qry = f"UPDATE `idea` SET `idea`='{idea}', `desc`='{description}' WHERE `ideaid`='{id}'"
        c.execute(qry)
        db.commit()
        return redirect("/sfViewSelfPost")
    return render(request, "sfUpdateIdea.html", {"data": data})


def sfDeleteIdea(request):
    id = request.GET["id"]
    qry = f"DELETE FROM `idea` WHERE `ideaid`='{id}'"
    c.execute(qry)
    db.commit()
    return redirect("/sfViewSelfPost")


def sfViewIdea(request):
    id = request.GET["post"]
    request.session["post"] = id
    sfid = request.session["id"]
    qry = f"SELECT * FROM `idea` i, `startpfounder` sf WHERE `ideaid`='{id}' AND i.`sfid`=sf.`sfid`"
    c.execute(qry)
    data = c.fetchone()
    qry = f"SELECT count(*) FROM tbllike where ideaid='{id}'"
    c.execute(qry)
    d = c.fetchone()
    act = ""
    like = 0
    dislike = 0
    if d[0] > 0:
        qry = f"SELECT postaction FROM tbllike where ideaid='{id}' and sfid='{sfid}'"
        c.execute(qry)
        d = c.fetchone()
        act = d[0] if d is not None else ""
        qry = f"SELECT count(*) FROM tbllike where ideaid='{id}' and postaction='like'"
        c.execute(qry)
        d = c.fetchone()
        like = d[0]
        qry = (
            f"SELECT count(*) FROM tbllike where ideaid='{id}' and postaction='dislike'"
        )
        c.execute(qry)
        d = c.fetchone()
        dislike = d[0]

    if request.method == "POST":
        comment = request.POST["comment"]
        qryCom = f"INSERT INTO `comments`(`sfid`,`ideaid`,`comment`,`date`) VALUES ('{sfid}','{id}','{comment}',(select sysdate()))"
        c.execute(qryCom)
        db.commit()
    qryViewCom = f"SELECT * FROM `comments`c, `startpfounder` s WHERE c.`ideaid`='{id}' AND c.`sfid`=s.`sfid` ORDER BY c.`comid` DESC"
    c.execute(qryViewCom)
    comments = c.fetchall()
    print(f"{data} {comments} {act} {like} {dislike}")
    return render(
        request,
        "sfViewIdea.html",
        {
            "data": data,
            "comments": comments,
            "act": act,
            "like": like,
            "dislike": dislike,
        },
    )


def sfilikepost(request):
    act = request.GET.get("act")
    pst = request.session["post"]
    sfid = request.session["id"]
    qry = (
        f"insert into tbllike(ideaid,sfid,postaction) values('{pst}','{sfid}','{act}')"
    )
    c.execute(qry)
    db.commit()
    return HttpResponseRedirect(f"/sfViewIdea?post={pst}")


def sfViewSf(request):
    id = request.GET["sfid"]
    qry = f"SELECT * FROM `startpfounder`WHERE `sfid`='{id}'"
    c.execute(qry)
    user = c.fetchone()
    qryPost = f"SELECT * FROM `idea` WHERE `sfid`={id}"
    c.execute(qryPost)
    post = c.fetchall()
    return render(request, "sfViewSf.html", {"user": user, "post": post})


def sfViewInvestemntOffers(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `investmentinterest` ii, `idea` i, `investors` inv WHERE i.`sfid`='{id}' AND i.`ideaid`=ii.`ideaid` AND ii.`invid`=inv.`invid`"
    c.execute(qry)
    data = c.fetchall()
    return render(request, "sfViewInvestemntOffers.html", {"data": data})


def sfViewPayments(request):
    id = request.session["id"]
    qry = f"SELECT * FROM `payment` p, `investors` i WHERE p.`sfid`='{id}' AND p.`invid`=i.`invid`"
    c.execute(qry)
    data = c.fetchall()
    return render(request, "sfViewPayments.html", {"data": data})


def sfOnInvestmentOffer(request):
    ininid = request.GET["ininid"]
    status = request.GET["status"]
    qry = (
        f"UPDATE `investmentinterest` SET `status`='{status}' WHERE `ininid`='{ininid}'"
    )
    c.execute(qry)
    db.commit()
    return redirect("/sfViewInvestemntOffers")


def sfAddFeedBack(request):
    id = request.session["id"]
    if request.method == "POST":
        feedback = request.POST["feedback"]
        qry = f"INSERT INTO `feedback`(`sfid`,`feedback`,`date`) VALUES ('{id}','{feedback}',(SELECT SYSDATE()))"
        c.execute(qry)
        db.commit()
    qryFed = f"SELECT * FROM `feedback` WHERE `sfid`='{id}'"
    c.execute(qryFed)
    data = c.fetchall()
    return render(request, "sfAddFeedBack.html", {"data": data})


def sfChat(request):
    sender = request.session["email"]
    qry = f"SELECT * FROM `investors` WHERE inemail in(select uname from login where status='Active') and pin in(select pin from startpfounder where sfemail='{sender}')"
    c.execute(qry)
    data = c.fetchall()
    return render(request, "sfChat.html", {"data": data, "user": sender})


def sfChatPer(request):
    sender = request.session["email"]
    receiver = request.GET["email"]
    if request.method == "POST":
        msg = request.POST["msg"]
        qry = f"INSERT INTO `chat` (`sender`,`receiver`,`message`,`date`) VALUES('{sender}','{receiver}','{msg}',(select sysdate()))"
        c.execute(qry)
        db.commit()
    qryChat = f"SELECT * FROM chat WHERE sender='{sender}' AND receiver='{receiver}' UNION SELECT * FROM chat WHERE receiver='{sender}' AND sender='{receiver}' ORDER BY `chatid`"
    c.execute(qryChat)
    messages = c.fetchall()
    return render(request, "sfChatPer.html", {"messages": messages, "user": sender})


def sfViewMore(request):
    id = request.GET["id"]

    sfid = request.session["id"]
    qry = f"SELECT * FROM `idea` i, `startpfounder` sf WHERE `ideaid`='{id}' AND i.`sfid`=sf.`sfid`"
    c.execute(qry)
    data = c.fetchone()
    qry = f"SELECT count(*) FROM tbllike where sfid='{sfid}' and ideaid='{id}'"
    c.execute(qry)
    d = c.fetchone()
    act = ""
    like = 0
    dislike = 0
    if d[0] > 0:
        qry = f"SELECT postaction FROM tbllike where sfid='{sfid}' and ideaid='{id}'"
        c.execute(qry)
        d = c.fetchone()
        act = d[0]
        qry = f"SELECT count(*) FROM tbllike where ideaid='{id}' and postaction='like'"
        c.execute(qry)
        d = c.fetchone()
        like = d[0]
        qry = (
            f"SELECT count(*) FROM tbllike where ideaid='{id}' and postaction='dislike'"
        )
        c.execute(qry)
        d = c.fetchone()
        dislike = d[0]

    qryViewCom = f"SELECT * FROM `comments`c, `startpfounder` s WHERE c.`ideaid`='{id}' AND c.`sfid`=s.`sfid` ORDER BY c.`comid` DESC"
    c.execute(qryViewCom)
    comments = c.fetchall()
    return render(
        request,
        "sfViewMore.html",
        {
            "data": data,
            "comments": comments,
            "act": act,
            "like": like,
            "dislike": dislike,
        },
    )


def report(request):
    user_type = request.GET["type"]
    user_type = user_type if user_type is not None else "users"
    query = (
        "select inname, inemail, inphone, inaddress from investors;"
        if user_type == "police"
        else "select sfname, sfemail, sfphone, sfaddress from startpfounder;"
    )
    c.execute(query)
    peoples = c.fetchall()
    return render(request, "report.html", {"data": peoples, "title": user_type.title()})
