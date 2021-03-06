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

        # Adding model 'Group'
        db.create_table('eece496_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_id', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('eece496', ['Group'])

        # Adding model 'Student'
        db.create_table('eece496_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('student_number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Group'])),
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

        # Adding model 'Evaluation'
        db.create_table('eece496_evaluation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Session'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('ta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.TA'])),
        ))
        db.send_create_signal('eece496', ['Evaluation'])

        # Adding model 'Attendance'
        db.create_table('eece496_attendance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Student'])),
            ('evaluation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Evaluation'])),
            ('group_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('individual_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('eece496', ['Attendance'])


    def backwards(self, orm):
        # Deleting model 'TA'
        db.delete_table('eece496_ta')

        # Deleting model 'Group'
        db.delete_table('eece496_group')

        # Deleting model 'Student'
        db.delete_table('eece496_student')

        # Deleting model 'Session'
        db.delete_table('eece496_session')

        # Deleting model 'Evaluation'
        db.delete_table('eece496_evaluation')

        # Deleting model 'Attendance'
        db.delete_table('eece496_attendance')


    models = {
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Evaluation']"}),
            'group_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Student']"})
        },
        'eece496.evaluation': {
            'Meta': {'object_name': 'Evaluation'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eece496.Student']", 'through': "orm['eece496.Attendance']", 'symmetrical': 'False'}),
            'ta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.TA']"})
        },
        'eece496.group': {
            'Meta': {'object_name': 'Group'},
            'group_id': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'eece496.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'eece496.student': {
            'Meta': {'object_name': 'Student'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Group']"}),
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