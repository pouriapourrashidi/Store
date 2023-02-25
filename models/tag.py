from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store_tag = db.relationship("StoreModel", back_populates="tag_store")
    # When we deifne secondary SQLAlchemy knows that it should go through item_tags to find the items related to this tag
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
