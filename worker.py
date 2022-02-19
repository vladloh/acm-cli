#file 

import requests
import os
import pickle
import codecs
import re

class Worker:
    ok = 'You are'
#    path = '{}/unic/algo_proga/'.format(os.getenv("HOME"))
    def __init__(self, login, password, path):
        self.url = 'http://acm.math.spbu.ru/tsweb/index'
        self.session = requests.Session()
        self.login = login
        self.password = password
        self.path = path
        self.session_path = self.path + '/' + self.login + '_session.mem'

    def save_session(self):
        with open(self.session_path, 'w') as file:
            print(codecs.encode(pickle.dumps(self.session), "base64").decode(), file = file)

    def post(self, url, **kwargs):
        res = self.session.post(url, **kwargs)
        self.save_session()
        return res


    def get_template(self):
        if os.path.isfile(self.path + '/' + 'template.cpp'):
            with open(self.path + '/' + 'template.cpp', 'r') as f:
                return f.read()
        else:
            return None


    def check(self):
        try:
            r = self.post(self.url)
            return self.ok in r.text
        except:
            return False


    def load_session(self):
        if os.path.isfile(self.session_path):
            with open(self.session_path, 'r') as f:
                pickled = f.read()
                return pickle.loads(codecs.decode(pickled.encode(), "base64"))
        return None


    def all_contests(self):
        self.log_in()
        res = self.post('https://acm.math.spbu.ru/tsweb/contests?mask=-1')
        data = []
        s = 'index?op=changecontest&newcontestid='
        for i in res.text.split('\n'):
            if s in i:
                try:
                    mem = i.split('\"')[1]
                    mem2 = mem.split('newcontestid=')
                    data.append(mem2[1])
                except:
                    pass
        return data


    def get_problems(self, relogin = False):
        if relogin: self.log_in()
        res = self.post('https://acm.math.spbu.ru/tsweb/summary')
        return [i.split('>')[-1] for i in re.findall(r'TR CLASS=\"\w*\"><TD>\w+', res.text)]


    def exists_contest(self, contest_id):
        return os.path.isdir(self.path + '/' + contest_id)


    def add_contest(self, contest_id):
        if self.exists_contest(contest_id):
            return
        self.change_contest(contest_id)
        problems = self.get_problems()

        pth = self.path + '/' + contest_id + '/'
        os.mkdir(pth[:-1])
        
        for problem in problems:
            with open(pth + problem + '.cpp', 'w') as f:
                f.write(self.get_template())

        print(len(problems), 'problems added!')


    def update_contests(self):
        contests = self.all_contests()
        count = 0
        for contest_id in contests:
            if not self.exists_contest(contest_id):
                print('Adding contest with id {}'.format(contest_id))
                self.add_contest(contest_id)
                count += 1
        return f'-------\n{count} contests added!\n-------'


    def change_contest(self, contest_id):
        self.post(self.url, data = {'newcontestid' : contest_id, 'op' : 'changecontest'})


    def log_in(self):
        old_session = self.load_session()
        if not old_session is None:
            self.session = old_session
            if self.check():
                return True
        self.post(self.url, data = {'team' : self.login, 'password' : self.password, 'op' : 'login'})
        return self.check()


    def submit_task_bp(self, contest_id, task, path):
        self.log_in()
        self.change_contest(contest_id)
        path = self.path  + '/' + contest_id + '/' + path
        url = 'https://acm.math.spbu.ru/tsweb/submit'
        with open(path, 'rb') as file:
            r = self.post(url, data = {'prob' : task, 'lang' : 6}, files = {'file' : file})
        return r.text


    def submit_task(self, path):
        data = path.split('/')
        contest_id = data[-2]
        path = data[-1]
        task = re.split('_|\.', path)[0]
        print("Submitting", task)
        return self.submit_task_bp(contest_id, task, path)
    


    def contest_from_path(self):
        direct = os.getcwd().split('/')[-1]
        return direct


    def get_summary(self): 

        def get_center(line): #...>x<... --> x
            return re.findall('>.*?<', line)[0][1:-1]

        self.log_in()
        contest_id = self.contest_from_path()
        if contest_id is None:
            return None
        self.change_contest(contest_id)
        res = self.post('https://acm.math.spbu.ru/tsweb/summary')
        text = res.text
        tasks = re.findall('<TR CLASS=\"\w*\">.*?</TR>', text)
        result = dict()
        for i in tasks:
            lines = re.findall('<TD>.*?</TD>', i)
            problem = get_center(lines[0])
            verdict = get_center(lines[-1])
            if verdict == "None": 
                verdict = None
            result[problem] = verdict
        return result

    def get_last_submission(self):

        def table_from_html(html):
            name = ['ID', 'Problem', 'Attempt', 'Time', 'Compiler', 'Result', 'TestN', 'Text', 'CE cause', 'Diff']
            for i in name:
                html = html.replace('<TD>{}</TD>'.format(i), '<TH>{}</TH>'.format(i))
            return html
        self.log_in()
        contest_id = self.contest_from_path()
        if contest_id is None:
            return None
        self.change_contest(contest_id)
        res = self.post('https://acm.math.spbu.ru/tsweb/allsubmits?prob=-&result=-')
        text = res.text
        tables = re.findall('<TABLE.*?</TABLE>', text)
        table = table_from_html(tables[-1])
        return table #return table in good html-table






