from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os 
from dotenv import load_dotenv
import csv
from io import StringIO
from flask import Response 

def _loadEnvFiles():
    load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['UPLOAD_FOLDER'] = 'static/files'


# صفحة تسجيل الدخول
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # بيانات تسجيل الدخول الصحيحة
        valid_email = "sederfleet@seder.sa"
        valid_password = "Seder@123456"

        # التحقق من البريد الإلكتروني وكلمة المرور
        if email == valid_email and password == valid_password:
            return redirect("/home")
        else:
            return render_template("Login.html", error="Invalid email or password!")

    return render_template("Login.html")

@app.route('/user')
def user():
    # استرداد البيانات من الجلسة أو قاعدة البيانات
    user_info = {
        "email": "sederfleet@seder.sa",
        "role": "Admin"
    }
    return render_template("User.html", user=user_info)

# الصفحة الرئيسية
@app.route("/home")
def home():
    return render_template("HOME.html")


@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/AEE')
def AEE():
      return render_template('AEE.html')


@app.route('/AEE/asssest', methods=['GET', 'POST'])
def asssest():
    message = None  # لعرض رسالة في حال وجود خطأ
    if request.method == 'POST':
        if 'export' in request.form:  # التركيز على تصدير البيانات فقط
            # جلب البيانات من النموذج
            department = request.form.get('department')
            project_name = request.form.get('project_name')
            plate = request.form.get('plate')
            chassis_number = request.form.get('chassis_number')
            sequence_number = request.form.get('sequence_number')
            vehicle_type = request.form.get('vehicle_type')
            eq_make = request.form.get('eq_make')
            eq_model = request.form.get('eq_model')
            model_year = request.form.get('model_year')
            color = request.form.get('color')
            status = request.form.get('status')
            asset_owner = request.form.get('asset_owner')
            license_expiry_date = request.form.get('license_expiry_date')
            mpvi_expiry_date = request.form.get('mpvi_expiry_date')
            seats = request.form.get('seats')
            eq_location = request.form.get('eq_location')
            op_card_expiry_date = request.form.get('op_card_expiry_date')
            insurance_expiry_date = request.form.get('insurance_expiry_date')
            gps = request.form.get('gps')
            fuel_type = request.form.get('fuel_type')
            fuel_chips = request.form.get('fuel_chips')
            chips_provider = request.form.get('chips_provider')
            transport_type = request.form.get('transport_type')
            username = request.form.get('username')
            user_id = request.form.get('user_id')
            asset_value = request.form.get('asset_value')
            substructures_value = request.form.get('substructures_value')

            # التحقق من تعبئة الحقول المطلوبة
            if not all([department, project_name, plate, chassis_number, sequence_number, vehicle_type, eq_make, eq_model, model_year, color, status, asset_owner, license_expiry_date, mpvi_expiry_date, seats, eq_location, op_card_expiry_date, insurance_expiry_date, gps, fuel_type, fuel_chips, chips_provider, transport_type, username, user_id, asset_value, substructures_value]):
                message = "الرجاء تعبئة جميع الحقول!"
                return render_template("asssest.html", message=message)

            # إنشاء ملف CSV عند التصدير
            csv_data = StringIO()
            csv_writer = csv.writer(csv_data)

            # كتابة العناوين
            csv_writer.writerow([
                'Department', 'Project Name', 'Plate', 'Chassis Number', 'Sequence Number', 'Vehicle Type',
                'EQ.Make', 'EQ.Model', 'Model Year', 'Color', 'Status', 'Asset Owner', 'License Expiry Date',
                'MPVI Expiry Date', 'Seats', 'EQ.Location', 'OP.Card Expiry Date', 'Insurance Expiry Date', 'GPS',
                'Fuel Type', 'Fuel Chips', 'Chips Provider', 'Transport Type', 'Username', 'User ID', 'Asset Value',
                'Substructures Value'
            ])

            # كتابة البيانات
            csv_writer.writerow([
                department, project_name, plate, chassis_number, sequence_number, vehicle_type,
                eq_make, eq_model, model_year, color, status, asset_owner, license_expiry_date,
                mpvi_expiry_date, seats, eq_location, op_card_expiry_date, insurance_expiry_date, gps,
                fuel_type, fuel_chips, chips_provider, transport_type, username, user_id, asset_value,
                substructures_value
            ])

            csv_data.seek(0)

            # إعداد الاستجابة لتنزيل الملف
            response = Response(csv_data.getvalue(), mimetype='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=export_data.csv'
            return response

    return render_template("asssest.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
def assest():

    if request.method == "POST":
        data = request.form.to_dict()
        
        if data:  #  وضع شرط معين هنا
            return redirect(url_for('AEE'))
        
        # إذا لم يتحقق الشرط، قم بعرض الصفحة نفسها مع رسالة أو شيء آخر
        return render_template('AEE.html', error="Error in submitted data")

    # إذا كان الطلب GET، فقط اعرض الصفحة
    return render_template('assest.html')

@app.route('/AEE', endpoint='AEE_endpoint')

def aee():
    return render_template('AEE.html')




@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file:
            print(app.config['UPLOAD_FOLDER'])
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File has been uploaded successfully."
    return render_template('upload_one_click.html')



@app.route('/Accidents')
def Accidents():
      return render_template('Accidents.html')

@app.route("/Accidents/dashboard")
def dashboard():
    return render_template("dashboard.html")



@app.route('/Accidents/Thirdparty', methods=['GET', 'POST'])
def Thirdparty():
    message = None  # لعرض الرسالة عند حدوث خطأ
    if request.method == 'POST':
        if 'export' in request.form:  # التركيز فقط على تصدير البيانات
            # جلب البيانات من النموذج
            chassis_number = request.form.get('chassis_number')
            location = request.form.get('location')
            accident_number = request.form.get('accident_number')
            mistake_percent = request.form.get('mistake_percent')
            accident_date = request.form.get('accident_date')
            description = request.form.get('description')
            status = request.form.get('status')
            responding_authority = request.form.get('responding_authority')
            attachment = request.form.get('attachment')

            # التحقق من تعبئة جميع الحقول
            if not all([chassis_number, location, accident_number, mistake_percent, accident_date, description, status, responding_authority, attachment]):
                message = "الرجاء تعبئة جميع الحقول!"
                return render_template("thirdparty.html", message=message)

            # إنشاء ملف CSV عند الضغط على Export
            csv_data = StringIO()
            csv_writer = csv.writer(csv_data)
            csv_writer.writerow(['Chassis Number', 'Location', 'Accident Number', 'Mistake Percent', 'Accident Date', 'Description', 'Status', 'Responding Authority', 'Attachment'])
            csv_writer.writerow([chassis_number, location, accident_number, mistake_percent, accident_date, description, status, responding_authority, attachment])
            csv_data.seek(0)

            # إعداد الاستجابة لتنزيل الملف
            response = Response(csv_data.getvalue(), mimetype='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=thirdparty_data.csv'
            return response

    return render_template("thirdparty.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/Accidents/Comprehensive')
def Comprehensive():
    message = None  # لعرض الرسالة عند حدوث خطأ
    if request.method == 'POST':
        if 'export' in request.form:  # التركيز فقط على تصدير البيانات
            # جلب البيانات من النموذج
            chassis_number = request.form.get('chassis_number')
            location = request.form.get('location')
            accident_number = request.form.get('accident_number')
            mistake_percent = request.form.get('mistake_percent')
            accident_date = request.form.get('accident_date')
            description = request.form.get('description')
            status = request.form.get('status')
            responding_authority = request.form.get('responding_authority')
            attachment = request.form.get('attachment')

            # التحقق من تعبئة جميع الحقول
            if not all([chassis_number, location, accident_number, mistake_percent, accident_date, description, status, responding_authority, attachment]):
                message = "الرجاء تعبئة جميع الحقول!"
                return render_template("Comprehensive.html", message=message)

            # إنشاء ملف CSV عند الضغط على Export
            csv_data = StringIO()
            csv_writer = csv.writer(csv_data)
            csv_writer.writerow(['Chassis Number', 'Location', 'Accident Number', 'Mistake Percent', 'Accident Date', 'Description', 'Status', 'Responding Authority', 'Attachment'])
            csv_writer.writerow([chassis_number, location, accident_number, mistake_percent, accident_date, description, status, responding_authority, attachment])
            csv_data.seek(0)

            # إعداد الاستجابة لتنزيل الملف
            response = Response(csv_data.getvalue(), mimetype='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=thirdparty_data.csv'
            return response

    return render_template("Comprehensive.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)







@app.route('/Accidents/Thirdparty/ThirdpartyAdd', methods=['GET', 'POST'])
def ThirdpartyAdd():

    if request.method == "POST":
        data = request.form.to_dict()
        
        # إذا أردت عمل تحقق على البيانات مثلاً:
        if data:  # يمكنك وضع شرط معين هنا
            return redirect(url_for('Thirdparty'))
        
        # إذا لم يتحقق الشرط، قم بعرض الصفحة نفسها مع رسالة أو شيء آخر
        return render_template('ThirdpartyAdd.html', error="Error in submitted data")

    # إذا كان الطلب GET، فقط اعرض الصفحة
    return render_template('ThirdpartyAdd.html')

@app.route('/Thirdparty', endpoint='Thirdparty_endpoint')
def th():
    return render_template('Thirdparty.html')







@app.route('/Accidents/Comprehensive/ComprehinsiveAdd', methods=['GET', 'POST'])
def ComprehinsiveAdd():

    if request.method == "POST":
        data = request.form.to_dict()
        
        # إذا أردت عمل تحقق على البيانات مثلاً:
        if data:  # يمكنك وضع شرط معين هنا
            return redirect(url_for('Comprehensive'))
        
        # إذا لم يتحقق الشرط، قم بعرض الصفحة نفسها مع رسالة أو شيء آخر
        return render_template('ComprehinsiveAdd.html', error="Error in submitted data")

    # إذا كان الطلب GET، فقط اعرض الصفحة
    return render_template('ComprehinsiveAdd.html')

@app.route('/Comprehensive', endpoint='Comprehensive_endpoint')
def co():
    return render_template('Comprehensive.html')









@app.route('/Regisrtation')
def Regisrtation():
      return render_template('Regisrtation.html')

@app.route("/Regisrtation/dashboard_route")
def dashboard_route():
    return render_template("dashboard.html")



@app.route("/Regisrtation/Insurance", methods=['GET', 'POST'])
def Insurance():
    if request.method == 'POST' and 'export' in request.form:
        # جلب البيانات من النموذج
        insurance_number = request.form.get('insurance_number')
        chassis_number = request.form.get('chassis_number')
        status = request.form.get('status')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        deductible = request.form.get('deductible')
        depreciation = request.form.get('depreciation')
        attachment = request.form.get('attachment')

        # التحقق من تعبئة جميع الحقول
        if not all([insurance_number, chassis_number, status, start_date, end_date, deductible, depreciation, attachment]):
            return "الرجاء تعبئة جميع الحقول!"

        # إنشاء ملف CSV
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(['Insurance Number', 'Chassis Number', 'Status', 'Start Date', 'End Date', 'Deductible', 'Depreciation', 'Attachment'])
        csv_writer.writerow([insurance_number, chassis_number, status, start_date, end_date, deductible, depreciation, attachment])
        csv_data.seek(0)

        # إعداد الاستجابة لتنزيل الملف
        response = Response(csv_data.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=insurance_data.csv'
        return response

    return render_template("insurance.html")


@app.route('/Regisrtation/Insurance/InsuranceAdd', methods=['GET', 'POST'])
def InsuranceAdd():

    if request.method == "POST":
        data = request.form.to_dict()
        
        # إذا أردت عمل تحقق على البيانات مثلاً:
        if data:  # يمكنك وضع شرط معين هنا
            return redirect(url_for('Insurance'))
        
        # إذا لم يتحقق الشرط، قم بعرض الصفحة نفسها مع رسالة أو شيء آخر
        return render_template('InsuranceAdd.html', error="Error in submitted data")

    # إذا كان الطلب GET، فقط اعرض الصفحة
    return render_template('InsuranceAdd.html')

@app.route('/Insurance', endpoint='Insurance_endpoint')
def Insurance():
    return render_template('Insurance.html')



@app.route("/Regisrtation/Insurance/dashboard_route1")
def dashboard_route1():
    return render_template("dashboard.html")



@app.route("/Regisrtation/OperationCards", methods=['GET', 'POST'])
def OperationCards():
    if request.method == 'POST' and 'export' in request.form:
        # جلب البيانات من النموذج
        chassis_number = request.form.get('chassis_number')
        issue_date = request.form.get('issue_date')
        expiration_date = request.form.get('expiration_date')
        card_number = request.form.get('card_number')
        status = request.form.get('status')
        attachment = request.form.get('attachment')

        # التحقق من تعبئة جميع الحقول
        if not all([chassis_number, issue_date, expiration_date, card_number, status, attachment]):
            return "الرجاء تعبئة جميع الحقول!"

        # إنشاء ملف CSV
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(['Chassis Number', 'Issue Date', 'Expiration Date', 'Card Number', 'Status', 'Attachment'])
        csv_writer.writerow([chassis_number, issue_date, expiration_date, card_number, status, attachment])
        csv_data.seek(0)

        # إعداد الاستجابة لتنزيل الملف
        response = Response(csv_data.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=operations_cards_data.csv'
        return response

    return render_template("operationcards.html")

@app.route('/Regisrtation/OperationCards/OCAdd', methods=['GET', 'POST'])
def OCAdd():

    if request.method == "POST":
        data = request.form.to_dict()
        
        # إذا أردت عمل تحقق على البيانات مثلاً:
        if data:  # يمكنك وضع شرط معين هنا
            return redirect(url_for('OperationCards'))
        
        # إذا لم يتحقق الشرط، قم بعرض الصفحة نفسها مع رسالة أو شيء آخر
        return render_template('OCAdd.html', error="Error in submitted data")

    # إذا كان الطلب GET، فقط اعرض الصفحة
    return render_template('OCAdd.html')

@app.route('/OperationCards', endpoint='operation_cards_endpoint')
def operation_cards():
    return render_template('OperationCards.html')



@app.route("/Regisrtation/OperationCards/dashboard_route2")
def dashboard_route2():
    return render_template("dashboard.html")



@app.route("/License", methods=['GET', 'POST'])
def License():
    if request.method == 'POST' and 'export' in request.form:
        # جلب البيانات من النموذج
        license_type = request.form.get('license_type')
        issue_date = request.form.get('issue_date')
        status = request.form.get('status')
        attachment = request.form.get('attachment')

        # التحقق من تعبئة جميع الحقول
        if not all([license_type, issue_date, status, attachment]):
            return "الرجاء تعبئة جميع الحقول!"

        # إنشاء ملف CSV
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(['License Type', 'Issue Date', 'Status', 'Attachment'])
        csv_writer.writerow([license_type, issue_date, status, attachment])
        csv_data.seek(0)

        # إعداد الاستجابة لتنزيل الملف
        response = Response(csv_data.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=license_data.csv'
        return response

    return render_template("license.html")

@app.route('/Regisrtation/License/LicenseAdd', methods=['GET', 'POST'])
def LicenseAdd():

    if request.method == "POST":
        data = request.form.to_dict()
        
        # إذا أردت عمل تحقق على البيانات مثلاً:
        if data:  # يمكنك وضع شرط معين هنا
            return redirect(url_for('License'))
        
        # إذا لم يتحقق الشرط، قم بعرض الصفحة نفسها مع رسالة أو شيء آخر
        return render_template('LicenseAdd.html', error="Error in submitted data")

    # إذا كان الطلب GET، فقط اعرض الصفحة
    return render_template('LicenseAdd.html')

@app.route('/License', endpoint='License_endpoint')
def operation_cards():
    return render_template('License.html')



@app.route("/Regisrtation/License/dashboard_route3")
def dashboard_route3():
    return render_template("dashboard.html")


@app.route('/Regisrtation/MPVI')
def MPVI():
      return render_template('MPVI.html')

@app.route('/Regisrtation/MPVI/MPVIAdd', methods=['GET', 'POST'])
def MPVIAdd():

    if request.method == "POST":
        data = request.form.to_dict()
        
        # إذا أردت عمل تحقق على البيانات مثلاً:
        if data:  # يمكنك وضع شرط معين هنا
            return redirect(url_for('MPVI'))
        
        # إذا لم يتحقق الشرط، قم بعرض الصفحة نفسها مع رسالة أو شيء آخر
        return render_template('MPVIAdd.html', error="Error in submitted data")

    # إذا كان الطلب GET، فقط اعرض الصفحة
    return render_template('MPVIAdd.html')

@app.route('/MPVI', endpoint='MPVI_endpoint')
def MPVI():
    return render_template('MPVI.html')



@app.route("/Regisrtation/MPVI/dashboard_route4")
def dashboard_route4():
    return render_template("dashboard.html")


    

@app.route("/Violations", methods=['GET', 'POST'])
def Violations():
    message = None  # لعرض الرسالة عند الضغط على زر Submit أو وجود خطأ
    if request.method == 'POST':
        # عند الضغط على زر Submit أو Export
        if 'submit' in request.form or 'export' in request.form:
            # جلب البيانات من النموذج
            violations_number = request.form.get('violations_number')
            driver_id = request.form.get('driver_id')
            chassis_number = request.form.get('chassis_number')
            violations_date = request.form.get('violations_date')
            sector = request.form.get('sector')
            project = request.form.get('project')
            plate_no = request.form.get('plate_no')
            violations_type = request.form.get('violations_type')
            violations_time = request.form.get('violations_time')
            violation_value = request.form.get('violation_value')
            location = request.form.get('location')

            # التحقق من تعبئة جميع الحقول
            if not all([violations_number, driver_id, chassis_number, violations_date, sector, project, plate_no, violations_type, violations_time, violation_value, location]):
                message = "الرجاء تعبئة جميع الحقول!"
                return render_template("violations.html", message=message)

            if 'submit' in request.form:
                # عند الضغط على زر Submit
                message = "تم ارسال البيانات بنجاح!"
           
            if 'export' in request.form:
                # عند الضغط على زر Export
                # إنشاء ملف CSV
                csv_data = StringIO()
                csv_writer = csv.writer(csv_data)
                csv_writer.writerow(['Violations number', 'Driver id number', 'Chassis Number', 'Violations Date', 'Sector', 'Project', 'PlateNo', 'Violations type', 'Violations time', 'Violation value', 'Location'])
                csv_writer.writerow([violations_number, driver_id, chassis_number, violations_date, sector, project, plate_no, violations_type, violations_time, violation_value, location])
                csv_data.seek(0)

                # إعداد الاستجابة لتنزيل الملف
                response = Response(csv_data.getvalue(), mimetype='text/csv')
                response.headers['Content-Disposition'] = 'attachment; filename=violations_data.csv'
                return response

    return render_template("violations.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
    

@app.route("/Fuel", methods=['GET', 'POST'])
def Fuel():
    message = None  # لعرض الرسالة عند الضغط على زر Submit
    if request.method == 'POST':
        if 'submit' in request.form:
            # عند الضغط على زر Submit
            message = "تم الضغط على زر Submit!"
        elif 'export' in request.form:
            # عند الضغط على زر Export
            try:
                # استرجاع البيانات من النموذج
                Date = request.form.get('Date', '')
                plateNo = request.form.get('plateNo', '')
                type_ = request.form.get('type', '')
                product = request.form.get('product', '')
                liters = request.form.get('liters', '')
                amount = request.form.get('amount', '')
                vehicle = request.form.get('vehicle', '')
                division = request.form.get('division', '')
                branch = request.form.get('branch', '')
                dept = request.form.get('dept', '')

                # التحقق من أن جميع الحقول تم تعبئتها
                if not (Date and plateNo and type_ and product and liters and amount and vehicle and division and branch and dept):
                    message = "يرجى ملء جميع الحقول"
                    return render_template("Fuel.html", message=message)

                # إنشاء ملف CSV في الذاكرة
                csv_data = StringIO()
                csv_writer = csv.writer(csv_data)
                csv_writer.writerow(['Date', 'plateno', 'type', 'product', 'liters', 'amount', 'vehicle', 'division', 'branch', 'dept'])
                csv_writer.writerow([Date, plateNo, type_, product, liters, amount, vehicle, division, branch, dept])
                csv_data.seek(0)

                # إعداد الاستجابة لتنزيل الملف
                response = Response(csv_data.getvalue(), mimetype='text/csv')
                response.headers['Content-Disposition'] = 'attachment; filename=fuel_data.csv'
                return response

            except Exception as e:
                # إظهار رسالة الخطأ في حالة حدوث مشكلة أثناء المعالجة
                message = f"حدث خطأ: {e}"
                return render_template("Fuel.html", message=message)

    return render_template("Fuel.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/woadd", methods=['GET', 'POST'])
def woadd():
       return render_template("woadd.html")
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/workshop", methods=['GET', 'POST'])
def WorkShop():
    message = None  # لعرض الرسالة عند الضغط على زر Submit
    if request.method == 'POST':
        if 'submit' in request.form:
            # الحصول على البيانات المدخلة من المستخدم
            plate = request.form.get('plate', '')
            sector = request.form.get('sector', '')
            invoice_no = request.form.get('invoice_no', '')
            total_amount = request.form.get('total_amount', '')
            date = request.form.get('date', '')
            supplier = request.form.get('supplier', '')

            # التحقق من وجود بيانات كاملة
            if not all([plate, sector, invoice_no, total_amount, date, supplier]):
                message = "يرجى تعبئة جميع الحقول!"
            else:
                message = "تم الضغط على زر Submit بنجاح!"

        elif 'export' in request.form:
            # عند الضغط على زر Export
            plate = request.form.get('plate', '')
            sector = request.form.get('sector', '')
            invoice_no = request.form.get('invoice_no', '')
            total_amount = request.form.get('total_amount', '')
            date = request.form.get('date', '')
            supplier = request.form.get('supplier', '')

            # إذا كانت البيانات غير مكتملة
            if not all([plate, sector, invoice_no, total_amount, date, supplier]):
                message = "يرجى تعبئة جميع الحقول قبل التصدير!"
            else:
                # إنشاء ملف CSV في الذاكرة
                csv_data = StringIO()
                csv_writer = csv.writer(csv_data)
                csv_writer.writerow(['Plate', 'Sector', 'InvoicesNo', 'Total Amount', 'Date', 'Supplier'])
                csv_writer.writerow([plate, sector, invoice_no, total_amount, date, supplier])
                csv_data.seek(0)

                # إعداد الاستجابة لتنزيل الملف
                response = Response(csv_data.getvalue(), mimetype='text/csv')
                response.headers['Content-Disposition'] = 'attachment; filename=workshop_data.csv'
                return response

    return render_template("workshop.html", message=message)
