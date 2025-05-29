from ariadne import QueryType, MutationType, ObjectType
from .models import db, Post, User
from .auth import register_user, login_user, get_current_user
from datetime import datetime

# GraphQL type resolvers
query = QueryType()
mutation = MutationType()
post = ObjectType("Post")

# -----------------------
# CUSTOM FIELD RESOLVERS
# -----------------------

@post.field("createdAt")
def resolve_created_at(post_obj, *_):
    return post_obj.created_at.isoformat()

# -----------------------
# QUERY RESOLVERS
# -----------------------

@query.field("posts")
def resolve_posts(_, info):
    return Post.query.all()

@query.field("post")
def resolve_post(_, info, id):
    return Post.query.get(id)

# -----------------------
# MUTATION RESOLVERS
# -----------------------

@mutation.field("createPost")
def resolve_create_post(_, info, title, content):
    user = get_current_user()
    if not user:
        raise Exception("Authentication required")

    new_post = Post(
        title=title,
        content=content,
        author=user,
        created_at=datetime.utcnow()
    )
    db.session.add(new_post)
    db.session.commit()
    return new_post

@mutation.field("register")
def resolve_register(_, info, username, password):
    user = register_user(username, password)
    return user

@mutation.field("login")
def resolve_login(_, info, username, password):
    token = login_user(username, password)
    return {"token": token}

# -----------------------
# EXPORT ALL RESOLVERS
# -----------------------

resolvers = [query, mutation, post]
