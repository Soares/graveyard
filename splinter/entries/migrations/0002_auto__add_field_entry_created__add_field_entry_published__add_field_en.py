# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entry.created'
        db.add_column('entries_entry', 'created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.date(2010, 6, 6), blank=True), keep_default=False)

        # Adding field 'Entry.published'
        db.add_column('entries_entry', 'published', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Entry.updated'
        db.add_column('entries_entry', 'updated', self.gf('django.db.models.fields.DateField')(auto_now=True, default=datetime.date(2010, 6, 6), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Entry.created'
        db.delete_column('entries_entry', 'created')

        # Deleting field 'Entry.published'
        db.delete_column('entries_entry', 'published')

        # Deleting field 'Entry.updated'
        db.delete_column('entries_entry', 'updated')


    models = {
        'entries.entry': {
            'Meta': {'object_name': 'Entry'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['entries.Tag']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'entries.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['entries']
