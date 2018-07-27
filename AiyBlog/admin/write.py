import time

from flask import Blueprint
from flask import render_template,request,url_for,redirect
from AiyBlog import db
from AiyBlog.models import aiyblog_metas,aiyblog_contents,aiyblog_relationships

write = Blueprint(__name__,"write",url_prefix="/admin/write")

@write.route('/post',methods=["GET","POST"])
def post():

    categories = aiyblog_metas.query.filter_by(type="category").all()
    tags = aiyblog_metas.query.filter_by(type="tag").all()
    if request.method == "POST":
        index=[]
        cgs = []
        for c in categories:
            index.append(c.mid)
        for x in index:
            try:
                cgs.append(request.form["category[%s]"%(x)])
            except:
                pass
        title = request.form["title"] or "未命名文章"
        text = request.form["markdown"]
        status = request.form["visibility"]
        raw_tags = request.form["tags"]
        new_tags = tags.replace('，',',').split(',')

        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        # some oper
        content = aiyblog_contents(title=title,created=int(time.time()),text=text,type="post",\
                                   status=status,allowComment=allowComments)
        db.session.add(content)
        db.session.commit()
        # 先拿到cid,然后再找到对应的mid关系
        cid = content.cid
        for mid in cgs:
            relationship = aiyblog_relationships(cid=cid,mid=mid)
            db.session.add(relationship)
            db.session.commit()

        return redirect(url_for("AiyBlog.admin.write.post"))

    return render_template("admin/write/post.html",cat=categories)

@write.route('/page',methods=["GET","POST"])
def page():

    if request.method == "POST":
        title = request.form["title"] or "未命名页面"
        slug = request.form["slug"]
        text = request.form["markdown"]
        order = request.form["order"]
        status = request.form["visibility"]
        try:
            allowComments = request.form["allowComments"]
        except:
            allowComments = "off"
        page = aiyblog_contents(title=title,slug=slug,text=text,type="page",status=status,\
                                allowComment=allowComments,order=order
                                )
        db.session.add(page)
        db.session.commit()
        return redirect(url_for("AiyBlog.admin.write.page"))

    return render_template("admin/write/page.html")
