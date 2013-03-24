# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('eece496_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_id', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('eece496', ['Group'])

        # Adding model 'Evaluation'
        db.create_table('eece496_evaluation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Session'])),
            ('ta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.TA'])),
            ('group_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('eece496', ['Evaluation'])

        # Deleting field 'Attendance.group_score'
        db.delete_column('eece496_attendance', 'group_score')

        # Deleting field 'Attendance.end'
        db.delete_column('eece496_attendance', 'end')

        # Deleting field 'Attendance.start'
        db.delete_column('eece496_attendance', 'start')

        # Deleting field 'Attendance.ta'
        db.delete_column('eece496_attendance', 'ta_id')


        # Renaming column for 'Student.group' to match new field type.
        db.rename_column('eece496_student', 'group', 'group_id')
        # Changing field 'Student.group'
        db.alter_column('eece496_student', 'group_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eece496.Group']))
        # Adding index on 'Student', fields ['group']
        db.create_index('eece496_student', ['group_id'])


    def backwards(self, orm):
        # Removing index on 'Student', fields ['group']
        db.delete_index('eece496_student', ['group_id'])

        # Deleting model 'Group'
        db.delete_table('eece496_group')

        # Deleting model 'Evaluation'
        db.delete_table('eece496_evaluation')

        # Adding field 'Attendance.group_score'
        db.add_column('eece496_attendance', 'group_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Attendance.end'
        db.add_column('eece496_attendance', 'end',
                      self.gf('django.db.models.fields.TimeField')(default='00:00:00'),
                      keep_default=False)

        # Adding field 'Attendance.start'
        db.add_column('eece496_attendance', 'start',
                      self.gf('django.db.models.fields.TimeField')(default='00:00:00'),
                      keep_default=False)

        # Adding field 'Attendance.ta'
        db.add_column('eece496_attendance', 'ta',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['eece496.TA']),
                      keep_default=False)


        # Renaming column for 'Student.group' to match new field type.
        db.rename_column('eece496_student', 'group_id', 'group')
        # Changing field 'Student.group'
        db.alter_column('eece496_student', 'group', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'eece496.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Student']"})
        },
        'eece496.evaluation': {
            'Meta': {'object_name': 'Evaluation'},
            'end': ('django.db.models.fields.TimeField', [], {}),
            'group_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eece496.Session']"}),
            'start': ('django.db.models.fields.TimeField', [], {}),
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
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eece496.Student']", 'through': "orm['eece496.Attendance']", 'symmetrical': 'False'}),
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