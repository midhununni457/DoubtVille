from webapp import app

if __name__ == '__main__':
    app.run(debug=True)

    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     adm_no1 = request.form.get('adm_no1')
    #     adm_no2 = request.form.get('adm_no2')
    #
    #     email_exists = User.query.filter_by(email=email).first()
    #     adm_no_exists = User.query.filter_by(adm_no=adm_no1).first()
    #
    #     if '@' in email:
    #         if 'bhavanseroor.ac.in' not in email.split('@'):
    #             flash('Please use email id provided by the school', category='error')
    #     elif '@' not in email:
    #         flash('Invalid email id', category='error')
    #     elif len(adm_no1) != 4 and 5:
    #         flash('Invalid admission number', category='error')
    #     elif adm_no1 != adm_no2:
    #         flash("Admission numbers don't match", category='error')
    #     elif email_exists:
    #         flash('There is already an account with this email', category='error')
    #     elif adm_no_exists:
    #         flash('There is already an account with this admission number', category='error')