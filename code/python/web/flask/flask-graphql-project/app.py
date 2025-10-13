# Imports
from flask import Flask
# app initialization
app = Flask(__name__)
app.debug = True
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Modules
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    posts = db.relationship('Post', backref='author')
    
    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    __tablename__ = 'posts'
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    def __repr__(self):
        return '<Post %r>' % self.title

# Imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

# Schema Objects
class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )
class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        username = graphene.String(required=True)
    post = graphene.Field(lambda: PostObject)
    def mutate(self, info, title, body, username):
        user = User.query.filter_by(username=username).first()
        post = Post(title=title, body=body)
        if user is not None:
            post.author = user
        db.session.add(post)
        db.session.commit()
        return CreatePost(post=post)
class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)

# Routes
@app.route('/')
def index():
    return '<p> Hello World</p>'

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

"""
to query, open browser on
http://127.0.0.1:5000/graphql

{
  allPosts{
    edges{
      node{
        title
        body
        author{
          username
        }
      }
    }
  }
}

To modify
mutation {
  createPost(username:"johndoe", title:"Hello 2", body:"Hello body 2"){
    post{
      title
      body
      author{
        username
      }
    }
  }
}
"""



def mockSetup():
    print('mockSetup() called')
    db.create_all()
    john = User(username='yosi')
    #post = Post()
    #post.title = "Hello World"
    #post.body = "This is the first post"
    #post.author = john
    #db.session.add(post)
    db.session.add(john)
    #db.session.query(User).delete()
    db.session.commit()
    #User.query.all()
    #    #[<User 'johndoe'>]
    #Post.query.all()
    #[<Post 'Hello World'>

if __name__ == '__main__':
     #mockSetup()
     app.run()
