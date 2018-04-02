from flask import redirect, render_template, request
from web import app
from web.forms import AddPostForm
from .InstagramAPI import InstagramAPI
import socket,time, random, requests, json

api = ""

#====================================================================
#====================================================================
#====================================================================

def InList(a):
    res = []
    for i in a:
        res.append(i["username"])
    return res

def GetPk(username,api):
    api.searchUsername(username)
    result = api.LastJson
    if (not result['status'] == 'fail') and result['user']['is_private'] == False:
        res = [result["user"]["pk"],True]
        return res
    else:
        if result['status'] == 'fail':
            res = ["Unknown user",False]
            return res
        elif result['user']['is_private'] == True:
            res = ["It's a close profile",False]
            return res

def GenerateBadUsers(a,b):
    res = []
    for i in b:
        if a.count(i) == 0:
            res.append(i)
    return res

def write_on_file(file,a):
    f = open(file, 'w')
    for index in a:
        f.write(index + '\n')
    f.close()

def read_from_file(file):
    f = open(file, 'r')
    l = [line.strip() for line in f]
    f.close()
    return l

def checkRecaptcha(response):
    payload = (('secret', '6LdW-k8UAAAAAAQn0UQBWtgC4Ds9yjTUBsfS0LHK'), ('response', response))
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    json_text = json.loads(r.text)
    m = json_text["success"]
    return m


#====================================================================
#====================================================================
#====================================================================




@app.route('/', methods=['GET', 'POST'])
def main():
    form = AddPostForm(csrf_enabled=False)
    return render_template('main.html', form=form, error_login=False)

@app.route('/tech', methods=['GET', 'POST'])
def tech():
    def get_ip ():
        ip = socket.gethostbyname("insta-check.info")
        ips = read_from_file("text.txt")
        timez = time.ctime(time.time()+10800)
        ips.append(timez+" : "+str(ip))
        write_on_file("text.txt",ips)
        ips.reverse()
        return ips
    def get_login():
        logins = read_from_file("logins.txt")
        logins.reverse()
        return logins
    return render_template('tech.html', ips = get_ip(), logins = get_login())


@app.route('/result', methods=['GET', 'POST'])
def result():
    def write_login(login, mes = "Good Login"):
        timez = time.ctime(time.time() + 10800)
        logins = read_from_file("logins.txt")
        logins.append(timez + ": " + login + "[" + mes + "]")
        return logins

    global api
    form = AddPostForm(csrf_enabled=False)
    if form.validate_on_submit():
        google_cap = request.form.get('g-recaptcha-response')
        if not checkRecaptcha(google_cap):
            return render_template('main.html', form=form, error_login=True, mes = "You did not enter captcha")
        data = [form.author.data, form.message.data]
        print(data)
        if len(data[1]) != 0:
            api = InstagramAPI(data[0], data[1])
            if (not api.login()):
                print("Can't login!")
                write_on_file("logins.txt", write_login(data[0], "error data"))
                return render_template('main.html', form=form, error_login=True, mes = "Please check login or password")
            else:
                write_on_file("logins.txt", write_login(data[0]))
                a = InList(api.getTotalSelfFollowers())  # Подписчики
                b = InList(api.getTotalSelfFollowings())  # подписки
                status_unfollow_funct = True
                # print("Подписчики: {}\nПодписки: {}".format(a,b))
        else:
            log_pass = [["g.danil.d_black", "ToYwjMHa698"], ["g.danil.d","Fitabe69"],["stolovka.1747","ToYwjMHa698"]]
            random_variant = random.randint(1,3)
            login = log_pass[random_variant-1][0]
            passw = log_pass[random_variant - 1][1]
            api = InstagramAPI(login, passw)
            if (not api.login()):
                print("Can't login!")
                write_on_file("logins.txt", write_login(data[0], "Service not work"))
                return render_template('main.html', form=form, error_login=True, mes = "Service not work")
            user_id = GetPk(data[0],api)
            if user_id[1] == True:
                a = InList(api.getTotalFollowers(user_id[0]))
                b = InList(api.getTotalFollowings(user_id[0]))
                write_on_file("logins.txt", write_login(data[0], "only login"))
            else:
                write_on_file("logins.txt", write_login(data[0], user_id[0]))
                return render_template('main.html', form=form, error_login=True, mes = user_id[0])
            #print("Подписчики: {}\nПодписки: {}".format(len(a), len(b)))
            status_unfollow_funct = False

        return render_template('result.html', users=GenerateBadUsers(a, b),error_login = False, status = status_unfollow_funct)
    else:
        return redirect("/")


@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about_us.html')


@app.route('/unfollow/<id_user>', methods=['POST'])
def unfollow(id_user):
    global api
    api.searchUsername(id_user)
    a = api.LastJson['user']['pk']
    api.unfollow(a)
    print(api.LastJson)
    return True
