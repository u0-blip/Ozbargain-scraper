import json
import redis
from models import db, User
from basic_app import app
from index_view import query_data
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user

rdb = redis.Redis(port=6379, db=0)

@app.route('/get_posts', methods=['POST'])
@login_required
def get_posts():
    items = rdb.get('items')
    if items != None:
        user = db.session.query(User).filter(User.id == current_user.id).first()
        queries = user.queries
        items = json.loads(items)
        filtered_items = []

        for item in items:
            description_list = [ele.strip().lower() for ele in item['text'].split(' ')]

            for q in queries:
                if str(q.query).lower() in description_list:
                    filtered_items.append(item)

        return json.dumps(filtered_items)
    else:
        return 'None'