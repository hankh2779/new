from flask import Flask, render_template, request, redirect, url_for, session, flash
import openpyxl
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

ADMIN_PASSWORD = '1234'  # 원하는 암호로 변경

EXCEL_PATH = 'user_data.xlsx'

MISSION_CODES = {
    1: '365OK',
    2: 'PAPEROK',
    3: 'MEDIA2F',
    4: 'SMARTOK'
}

def save_to_excel(name, student_id):
    if not os.path.exists(EXCEL_PATH):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['이름', '학번'])
    else:
        wb = openpyxl.load_workbook(EXCEL_PATH)
        ws = wb.active
    ws.append([name, student_id])
    wb.save(EXCEL_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    session['admin_mode'] = False  # 새로 시작할 때 항상 OFF
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        student_id = request.form.get('student_id', '').strip()
        if name and student_id:
            save_to_excel(name, student_id)
            return redirect(url_for('intro'))
        else:
            error = "이름과 학번을 모두 입력하세요."
            return render_template('index.html', error=error, admin=False)
    return render_template('index.html', error=None, admin=False)

@app.route('/intro', methods=['GET', 'POST'])
def intro():
    session['admin_mode'] = False  # 인트로 진입 시 항상 OFF
    if request.method == 'POST':
        session['intro'] = True
        return redirect(url_for('mission1'))
    return render_template('intro.html', admin=False)

@app.route('/set_admin', methods=['GET', 'POST'])
def set_admin():
    next_page = request.args.get('next') or request.form.get('next') or url_for('index')
    if request.method == 'POST':
        password = request.form.get('admin_password', '')
        if password == ADMIN_PASSWORD:
            session['admin_mode'] = True
            flash('관리자 모드가 활성화되었습니다.')
            return redirect(next_page)
        else:
            flash('다시 시도해 주세요')
            return render_template('admin_login.html', next=next_page)
    return render_template('admin_login.html', next=next_page)


@app.route('/unset_admin', methods=['POST'])
def unset_admin():
    session['admin_mode'] = False
    flash('관리자 모드가 해제되었습니다.')
    return redirect(request.referrer or url_for('index'))

@app.route('/mission/1', methods=['GET', 'POST'])
def mission1():
    if not session.get('intro'):
        return redirect(url_for('intro'))
    error = ''
    admin = session.get('admin_mode', False)
    if request.method == 'POST':
        if admin and request.form.get('skip') == '1':
            session['mission1'] = True
            return redirect(url_for('mission2'))
        user_input = request.form.get('code', '').strip().upper()
        if user_input == MISSION_CODES[1]:
            session['mission1'] = True
            return redirect(url_for('mission2'))
        else:
            error = '코드가 올바르지 않습니다. 다시 입력하세요.'
    return render_template('mission1.html', error=error, admin=admin)

@app.route('/mission/2', methods=['GET', 'POST'])
def mission2():
    if not session.get('mission1'):
        return redirect(url_for('mission1'))
    error = ''
    admin = session.get('admin_mode', False)
    if request.method == 'POST':
        if admin and request.form.get('skip') == '1':
            session['mission2'] = True
            return redirect(url_for('mission3'))
        user_input = request.form.get('code', '').strip().upper()
        if user_input == MISSION_CODES[2]:
            session['mission2'] = True
            return redirect(url_for('mission3'))
        else:
            error = '코드가 올바르지 않습니다. 다시 입력하세요.'
    return render_template('mission2.html', error=error, admin=admin)

@app.route('/mission/3', methods=['GET', 'POST'])
def mission3():
    if not session.get('mission2'):
        return redirect(url_for('mission2'))
    error = ''
    admin = session.get('admin_mode', False)
    if request.method == 'POST':
        if admin and request.form.get('skip') == '1':
            session['mission3'] = True
            return redirect(url_for('mission4'))
        user_input = request.form.get('code', '').strip().upper()
        if user_input == MISSION_CODES[3]:
            session['mission3'] = True
            return redirect(url_for('mission4'))
        else:
            error = '코드가 올바르지 않습니다. 다시 입력하세요.'
    return render_template('mission3.html', error=error, admin=admin)

@app.route('/mission/4', methods=['GET', 'POST'])
def mission4():
    if not session.get('mission3'):
        return redirect(url_for('mission3'))
    error = ''
    admin = session.get('admin_mode', False)
    if request.method == 'POST':
        if admin and request.form.get('skip') == '1':
            session['mission4'] = True
            return redirect(url_for('mission5'))
        user_input = request.form.get('code', '').strip().upper()
        if user_input == MISSION_CODES[4]:
            session['mission4'] = True
            return redirect(url_for('mission5'))
        else:
            error = '코드가 올바르지 않습니다. 다시 입력하세요.'
    return render_template('mission4.html', error=error, admin=admin)

@app.route('/mission/5', methods=['GET', 'POST'])
def mission5():
    if not session.get('mission4'):
        return redirect(url_for('mission4'))
    error = ''
    admin = session.get('admin_mode', False)
    if request.method == 'POST':
        if admin and request.form.get('skip') == '1':
            session['mission5'] = True
            return redirect(url_for('epilogue'))
        user_input = request.form.get('code', '').strip()
        answer = set(user_input.replace(',', ' ').split())
        if answer == {'2', '3'}:
            session['mission5'] = True
            return redirect(url_for('epilogue'))
        else:
            error = '정답이 아닙니다. 다시 선택하세요.'
    return render_template('mission5.html', error=error, admin=admin)

@app.route('/epilogue')
def epilogue():
    if not all(session.get(f'mission{i}') for i in range(1, 6)):
        return redirect(url_for('index'))
    return render_template('epilogue.html', admin=session.get('admin_mode', False))

if __name__ == '__main__':
    app.run(debug=True)
