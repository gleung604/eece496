# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Attendance.score'
        db.delete_column('eece496_attendance', 'score')

        # Adding field 'Attendance.individual_score'
        db.add_column('eece496_attendance', 'individual_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Attendance.group_score'
        db.add_column('eece496_attendance', 'group_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Attendance.score'
        db.add_column('eece496_attendance', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Attendance.individual_score'
        db.delete_column('eece496_attendance', 'individual_score')

        # Deleting field 'Attendance.group_score'
        db.delete_column('eece496_attendance', 'group_score')


    models = {
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'group_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Student']"}),
            'ta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.TA']"}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        'eece496.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eece496.Student']", 'through': "orm['eece496.Attendance']", 'symmetrical': 'False'}),
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