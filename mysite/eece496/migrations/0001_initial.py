# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TA'
        db.create_table('eece496_ta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('eece496', ['TA'])

        # Adding model 'Student'
        db.create_table('eece496_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('student_number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('group', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('program', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('eece496', ['Student'])

        # Adding model 'Session'
        db.create_table('eece496_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('eece496', ['Session'])

        # Adding model 'Attendance'
        db.create_table('eece496_attendance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.TA'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Student'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Session'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('eece496', ['Attendance'])


    def backwards(self, orm):
        # Deleting model 'TA'
        db.delete_table('eece496_ta')

        # Deleting model 'Student'
        db.delete_table('eece496_student')

        # Deleting model 'Session'
        db.delete_table('eece496_session')

        # Deleting model 'Attendance'
        db.delete_table('eece496_attendance')


    models = {
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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