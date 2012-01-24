# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('entries_tag', (
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True, db_index=True)),
        ))
        db.send_create_signal('entries', ['Tag'])

        # Adding model 'Entry'
        db.create_table('entries_entry', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('entries', ['Entry'])

        # Adding M2M table for field tags on 'Entry'
        db.create_table('entries_entry_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['entries.entry'], null=False)),
            ('tag', models.ForeignKey(orm['entries.tag'], null=False))
        ))
        db.create_unique('entries_entry_tags', ['entry_id', 'tag_id'])


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('entries_tag')

        # Deleting model 'Entry'
        db.delete_table('entries_entry')

        # Removing M2M table for field tags on 'Entry'
        db.delete_table('entries_entry_tags')


    models = {
        'entries.entry': {
            'Meta': {'object_name': 'Entry'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['entries.Tag']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'entries.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['entries']
