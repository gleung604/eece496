# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Attendance.time'
        db.delete_column('eece496_attendance', 'time')

        # Adding field 'Attendance.start'
        db.add_column('eece496_attendance', 'start',
                      self.gf('django.db.models.fields.TimeField')(default='00:00:00'),
                      keep_default=False)

        # Adding field 'Attendance.end'
        db.add_column('eece496_attendance', 'end',
                      self.gf('django.db.models.fields.TimeField')(default='00:00:00'),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Attendance.time'
        db.add_column('eece496_attendance', 'time',
                      self.gf('django.db.models.fields.TimeField')(default='00:00:00'),
                      keep_default=False)

        # Deleting field 'Attendance.start'
        db.delete_column('eece496_attendance', 'start')

        # Deleting field 'Attendance.end'
        db.delete_column('eece496_attendance', 'end')


    models = {
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'end': ('django.db.models.fields.TimeField', [], {}),
            'group_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Student']"}),
            'ta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.TA']"})
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