from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextAreaField
from wtforms.validators import Length, Email, EqualTo, DataRequired
from jobplus.models import db, User, CompanyDetail

class LoginForm(FlaskForm):
        email_or_name = StringField('用户名/邮箱', validators=[DataRequired()])
        password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
        remember_me = BooleanField('记住我')
        submit = SubmitField('提交')

        def validate_email_or_name(self, field):
            user = User.query.filter_by(email=field.data).first()

            if not user:
                user = User.query.filter_by(username=field.data).first()
                if not user:
                    raise ValidationError('邮箱或用户名不存在')
                if user.is_disable:
                    raise ValidationError('联系管理处理')
            '''
            u1 = User.query.filter_by(email=field.data).first()
            u2 = User.query.filter_by(username=field.data).first()
            if not u1 and not u2:
                raise ValidationError('邮箱或用户名不存在')
            elif u1.is_disable or u2.is_disable:
                raise ValidationError('联系管理处理')
            '''

        def validate_password(self, field):
            user = User.query.filter_by(username=self.email_or_name.data).first()
            if not user:
                user = User.query.filter_by(email=self.email_or_name.data).first()
            if user and not user.check_password(field.data):
                raise ValidationError('密码错误')
            self.user = user


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), Length(6, 24)])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('名字已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def create_user(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

class UserEditForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = StringField('密码')
    real_name = StringField('姓名')
    phone = StringField('手机号')
    submit = SubmitField('提交')

    def update(self, user):
        self.populate_obj(user)
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()

class CompanyEditForm(FlaskForm):
    username = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = StringField('密码')
    phone = StringField('手机号')
    site = StringField('公司网站', validators=[Length(0, 64)])
    description = StringField('一句话简介', validators=[Length(0, 64)])
    submit = SubmitField('提交')

    def update(self, company):
        company.username = self.username.data
        company.emael = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.detail:
            detail = company.detail
        else:
            detail = CompanyDetail()
            detail.user_id = company.id
        detail.site = self.site.data
        detail.description = self.description.data
        db.session.add(company)
        db.session.add(detail)
        db.seseion.commit()

class UserProfileForm(FlaskForm):
    real_name = StringField('姓名')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码（不填写保持不变）')
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume = StringField('简历')
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume = self.resume.data
        db.session.add(user)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    username = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码（不填写保持不变）')
    slug = StringField('Slug', validators=[DataRequired(), Length(3, 24)])
    location = StringField('地址', validators=[Length(0, 64)])
    site = StringField('公司网站', validators=[Length(0, 64)])
    logo = StringField('Logo')
    description = StringField('一句话描述', validators=[Length(0, 100)])
    about = TextAreaField('公司详情', validators=[Length(0, 1024)])
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phont = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self, user):
        user.username = self.username.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.company_detail:
            company_detail = user.company_detail
        else:
            company_detail = CompanyDetail()
            company_detail.user_id = user.id

        self.populate_obj(company_detail)
        db.session.add(user)
        db.session.add(company_detail)
        db.session.commit()


