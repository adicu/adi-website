from app import db
from datetime import datetime

now = datetime.now

class Tag(db.Document):

	# MongoEngine ORM metadata
	meta = {
		'indexes': [],
		'ordering': []
	}

	date_created = db.DateTimeField(default=now, required=True)
	data_modified = db.DateTimeField(default=now, required=True)
	tagname = db.StringField(unique=True, max_length=255,required=True)

	def clean(self):
		self.date_modified = now()

	@classmethod
	def get_or_create_tags(klass, tagnames):
		tagsList = []
		for tagname in tagnames:
			try:
				tagsList.append(klass.objects().get(tagname=tagname))
			except db.DoesNotExist:
				tag = Tag(tagname=tagname)
				tag.save()
				tagsList.append(tag)
		return tagsList


	def __unicode__(self):
		return self.tagname

	def __repr__(self):
		return self.tagname