from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    # it gives us an object related to the foreign key above and back_populates give item list associated with
    # each store.
    store_item = db.relationship("StoreModel", back_populates="item_store")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
