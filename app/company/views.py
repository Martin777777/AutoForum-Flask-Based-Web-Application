import base64

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
import datetime
from . import company
from .. import db
from ..decorators import permission_required
from ..models import Company, User, Activity, Permission
from ..email import send_email
from .forms import RegisterCompanyForm, PublishActivityForm
from .cloud import *

@company.route('/register', methods=['GET', 'POST'])
def register_company():
    form = RegisterCompanyForm()
    if form.validate_on_submit():
        email_find = User.query.filter_by(email=form.email.data).first()
        if email_find is not None:
            flash("Your email has been registered, please change your email")
            return render_template('company/company_register.html', form=form)
        username_find = User.query.filter_by(username=form.name.data).first()
        if username_find is not None:
            flash("Your company name has been registered, please change your username")
            return render_template('company/company_register.html', form=form)
        company = Company(name=form.name.data,
                          phone=form.phone.data,
                          email=form.email.data,
                          manager=form.manager.data)
        db.session.add(company)
        db.session.commit()
        try:
            register_company_cloud(0, form.name.data, form.manager.data, form.phone.data, form.email.data)
        except:
            pass
        token = company.generate_confirmation_token()
        send_email('1360412598@qq.com', 'Register Firm',
                   'mail_company/To_administrator', company=company, token=token)
        flash('A register firm-account email has been sent to administrator.')
        return redirect(url_for('auth.login'))
    return render_template('company/company_register.html', form=form)


@company.route('/send_result/<oid>', methods=['GET', 'POST'])
def send_result(oid):
    return render_template('company/send_result.html', oid=oid)


@company.route('/register_success/<oid>', methods=['GET'])
def register_success(oid):
    firm = Company.query.filter_by(id=oid).first()
    manager = User.query.filter_by(username=firm.manager).first()
    manager.role_id = 2
    db.session.add(manager)
    db.session.commit()
    try:
        register_successful_cloud(oid)
    except:
        pass
    # 注册时发送邮箱认证
    token = firm.generate_confirmation_token()
    send_email(firm.email, 'Register Company Success',
               'mail_company/success_register', user=manager, token=token, firm=firm)
    flash('A register_success email has been sent to company by email.')
    return redirect(url_for('auth.login'))


@company.route('/register_fail/<oid>', methods=['GET'])
def result_fail(oid):
    firm = Company.query.filter_by(id=oid).first()
    token = firm.generate_confirmation_token()
    send_email(firm.email, 'Register Company Fail',
               'mail_company/fail_register', token=token)
    flash('A register_fail email has been sent to company by email.')
    return redirect(url_for('auth.login'))


@company.route('/new_activity', methods=['GET', 'POST'])
def company_activity():
    form = PublishActivityForm()
    if form.validate_on_submit():
        str_time = form.time.data
        name = form.name.data
        place = form.place.data
        describe = form.describe.data
        organizer = form.organizer.data
        if name == "" or place == "" or str_time == "" or describe == "" or organizer == "":
            flash("Activity information cannot be empty")
            return render_template('company/new_activity.html')
        img = form.photo.data.read()
        img_bytes = base64.b64encode(img)
        img_bytes = str(img_bytes, 'utf-8')
        acti = Activity(activity_name=name,
                        activity_time=str_time,
                        activity_place=place,
                        activity_describe=describe,
                        Organizer=organizer,
                        announcer_id=current_user.id,
                        photo=img_bytes
                        )
        db.session.add(acti)
        db.session.commit()
        try:
            new_activity_cloud(name, datetime.datetime.strftime(str_time, '%Y-%m-%d %H:%M:%S'), place, describe, organizer, current_user.id)
        except:
            pass
        flash('Your Activity Announcement has been released!')
        return redirect(url_for('main.index_activity'))
    return render_template('company/new_activity.html', form=form)


@company.route('/want/<activity_id>')
@login_required
@permission_required(Permission.FOLLOW)
def want(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity is None:
        flash('Invalid activity.')
        return redirect(url_for('main.index_activity'))
    if current_user.is_wanting(activity):
        flash('You are already wanting this post.')
        return redirect(url_for('main.index_activity'))
    current_user.want(activity)
    activity.want(current_user)
    db.session.commit()
    try:
        new_want_cloud(current_user.id, activity.id, datetime.datetime.strftime(activity.timestamp, '%Y-%m-%d %H:%M:%S'))
    except:
        pass
    flash('You are now wanting this post')
    return redirect(url_for('main.index_activity'))


@company.route('/not_want/<activity_id>')
@login_required
@permission_required(Permission.FOLLOW)
def not_want(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    if activity is None:
        flash('Invalid activity.')
        return redirect(url_for('main.index_activity'))
    if not current_user.is_wanting(activity):
        flash('You are not wanting this post.')
        return redirect(url_for('main.index_activity'))
    current_user.not_want(activity)
    activity.not_want(current_user)
    db.session.commit()
    try:
        not_want_cloud(current_user.id)
    except:
        pass
    flash('You are not wanting this post')
    return redirect(url_for('main.index_activity'))


@company.route('/delete_transaction/<int:activity_id>')
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if current_user == activity.announcer:
        db.session.delete(activity)
        db.session.commit()
        try:
            delete_activity_cloud(activity_id)
        except:
            pass
        # flash('你没有删评论权限')
        flash('The activity has been deleted.')
        return redirect(url_for('main.user', username=activity.announcer.username))
    else:
        flash('你没有删评论权限')
        return redirect(url_for('main.user', username=activity.announcer.username))
