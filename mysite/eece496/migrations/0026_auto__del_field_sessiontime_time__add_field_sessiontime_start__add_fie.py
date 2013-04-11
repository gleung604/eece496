# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SessionTime.time'
        db.delete_column('eece496_sessiontime', 'time')

        # Adding field 'SessionTime.start'
        db.add_column('eece496_sessiontime', 'start',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 4, 11, 0, 0)),
                      keep_default=False)

        # Adding field 'SessionTime.end'
        db.add_column('eece496_sessiontime', 'end',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 4, 11, 0, 0)),
                      keep_default=False)

        # Deleting field 'Session.time'
        db.delete_column('eece496_session', 'time_id')

        # Adding field 'Session.block'
        db.add_column('eece496_session', 'block',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['eece496.SessionTime']),
                      keep_default=False)

        # Deleting field 'Evaluation.time'
        db.delete_column('eece496_evaluation', 'time')

        # Adding field 'Evaluation.start'
        db.add_column('eece496_evaluation', 'start',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 4, 11, 0, 0)),
                      keep_default=False)

        # Adding field 'Evaluation.end'
        db.add_column('eece496_evaluation', 'end',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 4, 11, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SessionTime.time'
        db.add_column('eece496_sessiontime', 'time',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Deleting field 'SessionTime.start'
        db.delete_column('eece496_sessiontime', 'start')

        # Deleting field 'SessionTime.end'
        db.delete_column('eece496_sessiontime', 'end')

        # Adding field 'Session.time'
        db.add_column('eece496_session', 'time',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['eece496.SessionTime']),
                      keep_default=False)

        # Deleting field 'Session.block'
        db.delete_column('eece496_session', 'block_id')

        # Adding field 'Evaluation.time'
        db.add_column('eece496_evaluation', 'time',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Deleting field 'Evaluation.start'
        db.delete_column('eece496_evaluation', 'start')

        # Deleting field 'Evaluation.end'
        db.delete_column('eece496_evaluation', 'end')


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
            'date': ('django.db.models.fields.DateField', [], {}),
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
            'end': ('django.db.models.fields.TimeField', [], {}),
            'evaluatee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'evaluatee_set'", 'null': 'True', 'to': "orm['eece496.Attendance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Evaluation']", 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'evaluation_set'", 'to': "orm['eece496.Student']", 'through': "orm['eece496.Attendance']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'ta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.TA']"}),
            'volunteer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'eece496.group': {
            'Meta': {'object_name': 'Group'},
            'group_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'eece496.session': {
            'Meta': {'object_name': 'Session'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.SessionTime']"}),
            'cogs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.COGS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'eece496.sessiontime': {
            'Meta': {'object_name': 'SessionTime'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {})
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