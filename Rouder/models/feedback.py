class Feedback(BaseModel):
    id        = AutoField()
    user_from = ForeignKeyField(User, backref='sent_feedbacks')
    user_to   = ForeignKeyField(User, backref='received_feedbacks')
    liked     = BooleanField()
    created   = DateTimeField(default=datetime.datetime.now)
