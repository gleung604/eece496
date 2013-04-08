# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'TA', fields ['number']
        db.create_unique('eece496_ta', ['number'])


    def backwards(self, orm):
        # Removing unique constraint on 'TA', fields ['number']
        db.delete_unique('eece496_ta', ['number'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'absent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Evaluation']"}),
            'excused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Student']"})
        },
        'eece496.cogs': {
            'Meta': {'object_name': 'COGS'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Course']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'eece496.course': {
            'Meta': {'object_name': 'Course'},
            'course_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'eece496.evaluation': {
            'Meta': {'object_name': 'Evaluation'},
            'evaluatee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'evaluatee_set'", 'null': 'True', 'to': "orm['eece496.Attendance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Evaluation']", 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'evaluation_set'", 'to': "orm['eece496.Student']", 'through': "orm['eece496.Attendance']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'ta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.TA']"}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'volunteer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'eece496.group': {
            'Meta': {'object_name': 'Group'},
            'group_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'eece496.session': {
            'Meta': {'object_name': 'Session'},
            'cogs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.COGS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.SessionTime']"})
        },
        'eece496.sessiontime': {
            'Meta': {'object_name': 'SessionTime'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['eece496']