from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog_portfolio import db
from flask_blog_portfolio.models import Post, Comment, Like, Category, Hashtag
from flask_blog_portfolio.posts.forms import PostForm, CommentForm, LikeForm
from flask_blog_portfolio.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/allpost", methods=['GET', 'POST'])
@login_required
def allpost(post_id=None):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    like_form = LikeForm()
    like_count = Like.query.filter_by(post_id=post_id).count()

    return render_template('allpost.html', posts=posts, like_form=like_form, like_count=like_count)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    categories = Category.query.all()
    hashtags = Hashtag.query.all()
    form = PostForm()
    picture_name = None

    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)

        post = Post(title=form.title.data, content=form.content.data, author=current_user, image_file=picture_name,
                    category_id=request.form['category'])

        hashtags_id = request.form.getlist('hashtags[]')
        hashtags_new = request.form.getlist('hashtags_new[]')

        for i in range(len(hashtags_new)):
            if len(hashtags_new[i]) > 0:
                hastag = Hashtag(name=hashtags_new[i])
                db.session.add(hastag)
                db.session.commit()
                hashtags_id.append(hastag.id)

        for i in hashtags_id:
            hash = Hashtag.query.filter_by(id=int(i)).all()
            post.hashtags.extend(hash)

        db.session.add(post)
        db.session.commit()

        flash('Ваш пост создан!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('create_post.html', title='Новая статья', form=form, image_file=picture_name,
                           legend='Новая статья', categories=categories, hashtags=hashtags)


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    like_form = LikeForm()
    like_count = Like.query.filter_by(post_id=post_id).count()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.comment.data, post_id=post_id, username=current_user.username)
        db.session.add(comment)
        db.session.commit()
        flash('Ваш комментарий добавлен!', 'success')
        return redirect(f'/post/{post_id}')

    return render_template('post.html', title=post.title, post=post, form=form, like_form=like_form,
                           like_count=like_count)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file

        db.session.commit()
        flash('Ваш пост обновлен!', 'success')

        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

        image_file = url_for('static', filename='posts_pics/' + post.image_file)

    return render_template('create_post.html', title='Обновление поста', image_file=image_file,
                           form=form, legend='Обновление поста')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('posts.allpost'))


@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.username != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Ваш комментарий был удален!', 'success')

    return redirect(url_for('posts.post', post_id=comment.post_id))


@posts.route('/post/<string:post_id>/like', methods=('POST',))
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author == current_user:
        flash('Вы не можете поставить лайк т.к. пост создали Вы сами', 'warning')
    elif Like.query.filter_by(user_id=current_user.id, post_id=post_id).count():
        Like.query.filter_by(user_id=current_user.id, post_id=post_id).delete()
        db.session.commit()
        flash('Вам больше не нравится этот пост.', 'success')
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        flash('Вам нравится этот пост.', 'success')

    return redirect(url_for('posts.post', post_id=post_id))


@posts.route("/favorites", methods=['GET', 'POST'])
@login_required
def favorites():
    posts = Post.query.all()
    like = Like.query.filter_by(user_id=current_user.id).all()
    print(like)
    count = Like.query.filter_by(user_id=current_user.id).count()
    print(count)
    favorite_posts = []
    for post in posts:
        if post.id in like:
            favorite_posts.append(post)
    print(posts)
    print(favorite_posts)

    return render_template('favorites.html', title='Избранное', posts=favorite_posts, like=like, count=count)
