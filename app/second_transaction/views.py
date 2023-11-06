import base64
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from . import transaction
from .cloud import *
import datetime
from .forms import PublishCarForm
from .. import db
from ..decorators import permission_required
from ..models import Transaction, Permission


@transaction.route('/new_transaction', methods=['GET', 'POST'])
def new_transaction():
    form = PublishCarForm()
    if form.validate_on_submit():
        name = form.name.data
        describe = form.describe.data
        link = form.link.data
        mode = form.mode.data
        chat = form.chat.data
        if name == "" or describe == "" or link == "" or mode == "" or chat == "":
            flash("Item information cannot be empty")
            return render_template('transaction/new_transaction.html')
        img = form.photo.data.read()
        img_bytes = base64.b64encode(img)
        img_bytes = str(img_bytes, 'utf-8')
        trans = Transaction(car_name=name,
                            car_describe=describe,
                            link=link,
                            transaction_mode=mode,
                            contact=chat,
                            picture=img_bytes,
                            seller_id=current_user.id,
                            seller=current_user
                            )
        db.session.add(trans)
        db.session.commit()
        try:
            new_transaction_cloud(datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M:%S'), name, describe, link, mode, 0, chat, current_user.id)
        except:
            pass
        flash('Your transaction request has been sent!')
        return redirect(url_for('main.index_transaction'))
    return render_template('transaction/new_transaction.html', form=form)


@transaction.route('/sold/<item_id>')
def sold_item(item_id):
    transactions = Transaction.query.filter_by(id=item_id).first()
    transactions.is_sold = True
    db.session.add(transactions)
    db.session.commit()
    try:
        sold_item_cloud(item_id)
    except:
        pass
    return redirect(url_for('main.user', username=current_user.username))


@transaction.route('/collect/<transaction_id>')
@login_required
@permission_required(Permission.FOLLOW)
def collect(transaction_id):
    transactions = Transaction.query.filter_by(id=transaction_id).first()
    if transactions is None:
        flash('Invalid transaction.')
        return redirect(url_for('main.index_transaction'))
    if current_user.is_collecting(transactions):
        flash('You are already collecting this post.')
        return redirect(url_for('main.index_transaction'))
    current_user.collect(transactions)
    transactions.collect(current_user)
    transactions.recent_activity = datetime.datetime.utcnow()
    db.session.commit()
    try:
        collect_cloud(current_user.id, transaction_id,
                      datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%d %H:%M:%S'))
    except:
        pass

    flash('You are now collecting this post')
    return redirect(url_for('main.index_transaction'))


@transaction.route('/not_collect/<transaction_id>')
@permission_required(Permission.FOLLOW)
def not_collect(transaction_id):
    transactions = Transaction.query.filter_by(id=transaction_id).first()
    if transactions is None:
        flash('Invalid transaction.')
        return redirect(url_for('main.index_transaction'))
    if not current_user.is_collecting(transactions):
        flash('You are not collecting this post.')
        return redirect(url_for('main.index_transaction'))
    current_user.not_collect(transactions)
    transactions.not_collect(current_user)
    db.session.commit()
    try:
        not_collect_cloud(current_user.id)
    except:
        pass
    flash('You are not collecting this post')
    return redirect(url_for('main.index_transaction'))


@transaction.route('/delete_transaction/<int:item_id>')
@login_required
def delete_transaction(item_id):
    transaction=Transaction.query.get_or_404(item_id)
    if current_user == transaction.seller:
        db.session.delete(transaction)
        db.session.commit()
        try:
            delete_transaction_cloud(item_id)
        except:
            pass
        flash('The second_transaction has been deleted.')
        return redirect(url_for('main.user', username=transaction.seller.username))
    else:
        flash('你没有删评论权限')
        return redirect(url_for('main.user', username=transaction.seller.username))
