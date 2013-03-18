# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Session.status'
        db.delete_column('eece496_session', 'status')

        # Adding field 'Attendance.status'
        db.add_column('eece496_attendance', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Session.status'
        db.add_column('eece496_session', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Attendance.status'
        db.delete_column('eece496_attendance', 'status')


    models = {
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Student']"})
        },
        'eece496.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eece496.Student']", 'through': "orm['eece496.Attendance']", 'symmetrical': 'False'}),
            'ta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.TA']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'eece496.student': {
            'Meta': {'object_name': 'Student'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'group': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'program': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'student_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'eece496.ta': {
            'Meta': {'object_name': 'TA'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['eece496']