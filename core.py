# -*- coding: utf-8 -*-
import csv

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class CardPainter(object):

    class Story(object):
        def __init__(self, sid, name, imp, est, demo, notes):
            self.sid = sid
            self.name = name
            self.imp = imp
            self.est = est
            self.demo = demo
            self.notes = notes

    def __init__(self, input_path, output_path, fontname, fontpath,
                 is_landscape=False, padding=20):
        if is_landscape:
            self.canvas = canvas.Canvas(output_path, pagesize=landscape(A4))
            self.page_height, self.page_width = A4
        else:
            self.canvas = canvas.Canvas(output_path)
            self.page_width, self.page_height = A4

        self.padding = padding

        self.page = 0
        self.story_count = 0

        self.black = 0.3
        self.gray = 0.5
        self.lite_gray = 0.95
        self.white = 1

        if fontname and fontpath:
            pdfmetrics.registerFont(TTFont(fontname, fontpath))
            self.fontname = fontname
        else:
            self.fontname = 'Helvetica'

        self.load_backlog(input_path)

    def load_backlog(self, path):
        self.backlog = []
        with open(path, 'rb') as backlog_file:
            reader = csv.reader(backlog_file)
            first_line = True
            for row in reader:
                if first_line:
                    first_line = False
                    continue
                story = self.Story(row[0], row[1], row[2], row[3], row[4], row[5])
                self.backlog.append(story)
        print 'backlog:', len(self.backlog)

    def setFontSize(self, size):
        self.canvas.setFont(self.fontname, size)
