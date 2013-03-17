# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TA.name'
        db.delete_column('eece496_ta', 'name')

        # Adding field 'TA.first_name'
        db.add_column('eece496_ta', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='asdf', max_length=50),
                      keep_default=False)

        # Adding field 'TA.last_name'
        db.add_column('eece496_ta', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='assdf', max_length=50),
                      keep_default=False)

        # Deleting field 'Student.name'
        db.delete_column('eece496_student', 'name')

        # Adding field 'Student.first_name'
        db.add_column('eece496_student', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='sadssdsds', max_length=50),
                      keep_default=False)

        # Adding field 'Student.last_name'
        db.add_column('eece496_student', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='dsdssds', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'TA.name'
        db.add_column('eece496_ta', 'name',
                      self.gf('django.db.models.fields.CharField')(default='asdf', max_length=50),
                      keep_default=False)

        # Deleting field 'TA.first_name'
        db.delete_column('eece496_ta', 'first_name')

        # Deleting field 'TA.last_name'
        db.delete_column('eece496_ta', 'last_name')

        # Adding field 'Student.name'
        db.add_column('eece496_student', 'name',
                      self.gf('django.db.models.fields.CharField')(default='sadss', max_length=50),
                      keep_default=False)

        # Deleting field 'Student.first_name'
        db.delete_column('eece496_student', 'first_name')

        # Deleting field 'Student.last_name'
        db.delete_column('eece496_student', 'last_name')


    models = {
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
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
            'program': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eece496.ta': {
            'Meta': {'object_name': 'TA'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['eece496']