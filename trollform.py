from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def form():
    return render_template('form.html')
@app.route('/send', methods=['POST'])
def send_message():
    message = request.form.get('message') or ''
    if len(message.strip()):
        print(f'[Жалоба]: {message}')
    else:
    return 'Спасибо! Ваша жалоба принята.'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
