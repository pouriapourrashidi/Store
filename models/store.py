from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    # Lazy says that whenever you load something from storemodel don't load items until I say that.
    item_store = db.relationship("ItemModel", back_populates="store_item", lazy="dynamic", cascade = "all, delete")

    tag_store = db.relationship("TagModel", back_populates="store_tag",  lazy="dynamic")